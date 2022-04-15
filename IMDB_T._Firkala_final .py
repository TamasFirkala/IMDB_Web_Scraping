#!/usr/bin/env python
# coding: utf-8

# # Collection of the necessary IMDB Top 250 data (movie_title, rating, votes)

# In[1]:


from bs4 import BeautifulSoup
import requests
import re

# Collection of the necessary data from the IMDB website

url = 'https://www.imdb.com/chart/top/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

movies = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=nv]')]

imdb = []

# Store each item into dictionary (data), then put those into a list (imdb)
for index in range(0, len(movies)):
    
    movie_string = movies[index].get_text()
    movie = (' '.join(movie_string.split()).replace('.', ''))
    movie_title = movie[len(str(index))+1:-7]
    data = {"movie_title": movie_title,
            "rating": ratings[index],
            "vote": votes[index]}
    
    imdb.append(data)

#for item in imdb:
    #print(item['movie_title'], item['rating'], item['vote'])


# In[2]:


#Storing the data in pandas dataframe

import pandas as pd

df = pd.DataFrame(imdb)
df


# In[293]:


#Selection of the first 20 movies

n = 230

df.drop(df.tail(n).index,
        inplace = True)
df


# In[ ]:





# In[107]:


#Exporting the movies in a csv file to translate their titles to English manually

df.to_csv('imdb_TF.csv')


# In[294]:


df_2 = pd.read_csv('imdb_TF_ENG.csv')
df_2


# In[109]:


#Extration of the movie titles in a list

titles = df_2['movie_title'].tolist()
titles


# ## Scraping oscar winning data using pandas from wikipedia 
# (  https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films )

# In[297]:


# pd_read_html function was applied to extract tabular data from wikipedia

df_3 = pd.read_html('https://en.wikipedia.org/wiki/List_of_Academy_Award-winning_films')[0]


# In[298]:


# Every oscar winning film of the history was collected in a dataframe 

df_3


# In[299]:


# deleting  unnecessary columns

del df_3['Year']
del df_3['Nominations']

df_3.head()


# ## Preparation of a pandas dataframe containing a column with the number of oscars won by our TOP 20 film ( the process runs from df_3 to df_8 )
# 

# In[120]:


#Checking the common oscar winning films of our TOP 20 movies and the collected using pandas .isin() function

#Oscar winning film from the TOP 20 movies:
df_4 = df_3[df_3['Film'].isin(titles)]
df_4


# In[118]:


#Extration of oscar winning film titles to a list

oscars = df_4['Film'].tolist()
oscars


# In[123]:


#Extration of "non oscar winning" movies from our TOP 20 movies (df_2) using pandas "not .isin()" function (~ means "not").

df_5 = df_2[~df_2['movie_title'].isin(oscars)]
df_5


# In[300]:


#Addition of a column 'oscars' with null values:

df_5['oscars'] = 0


# In[302]:


df_5


# In[128]:


df_4


# In[304]:


# Renaming columns in the dataframe of our oscar winning movies from TOP 20 (df_4)

df_4.rename(columns = {'Film':'movie_title'}, inplace = True)
df_4.rename(columns = {'Awards':'oscars'}, inplace = True)


# In[305]:


df_4


# In[306]:


#Addition of oscar values to our original top 20 movies (df_2) with merging the two dataframes (df_4, df_2):

df_6 = pd.merge(df_4, df_2, on="movie_title")
df_6


# In[307]:


#Changing column positions:

df_6 = df_6[['movie_title', 'rating', 'vote', 'oscars']]
df_6


# In[309]:


# Merging oscar winning and non-oscar winning movies of our TOP 20 films using the appropriate data frames (df_5 and df_6)

df_7 = df_5.append(df_6)
df_7


# In[311]:


# sorting the films according to rating

df_8 = df_7.sort_values(["rating"], ascending=False)
df_8


# In[322]:


df_8 = df_8.reset_index(drop=True)
df_8


# ## Additon of a column with rating adjusted by the number of votes

# In[323]:


#Addition of a column where the rating is corrected with the number of votes

df_8['vote_adjusted_rating'] = df_8['rating'] - ((2573229 - df_8['vote']) / 1000000 )


# In[324]:


df_8


# ## Additon of a column with rating adjusted by the number of oscars

# In[325]:


#Checking data types in df_8 dataframe

df_8.dtypes


# In[326]:


#Changing the data type in oscars column to integer

df_8['oscars'] = df_8['oscars'].astype('int')


# In[327]:


#Checking data types again

df_8.dtypes


# In[328]:


#Extration of the rating and oscars data into lists

rating = df_8['rating'].tolist()
print(rating)
awards = df_8['oscars'].tolist()
print(awards)


# In[329]:


# Generation of a list containing the rating values corrected by the number of oscars according to the required logic

import itertools

y = []

for (i, j) in zip(awards, rating):
    
        if i == 0:
            x = j
            
        if i == 1 or i == 2:
            x = j + 0.3
            
        if 3 <= i <= 5:
            x = j + 0.5
            
        if 6 <= i <= 10:
            x = j + 1
            
        if i > 10:
            x = j + 1.5
            
        y.append(x)

print(y)


# In[333]:


#Generation of a pandas dataframe from the list (y) with the oscar corrected rating values. 

df_9 = pd.DataFrame(y, columns =['oscar_adjusted_rating'])
df_9


# In[334]:


#Merging df_8 and df_9 dataframes to obtain the final dataframe with all necessary values

df_final = pd.concat([df_8, df_9], axis=1)

df_final


# In[337]:


# Setting arbitrary decimals

df_final = df_final.round(decimals = 2)
df_final


# In[338]:


#Exporting to result in a csv file

df_final.to_csv('imdb_TF_final.csv')

