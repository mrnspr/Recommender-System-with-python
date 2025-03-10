#!/usr/bin/env python
# coding: utf-8

# ___
# # Recommender Systems with Python
# 
# Welcome to the code notebook for Recommender Systems with Python. In this lecture we will develop basic recommendation systems using Python and pandas. 
# 
# In this notebook, we will focus on providing a basic recommendation system by suggesting items that are most similar to a particular item, in this case, movies. Keep in mind, this is not a true robust recommendation system, to describe it more accurately,it just tells you what movies/items are most similar to your movie choice.
# 
# ## Import Libraries

# In[16]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# ## Get the Data

# In[17]:


df1 = pd.read_csv('u.data')
df1


# In[18]:


column_names = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv('u.data', sep='\t', names=column_names)


# In[19]:


df.head()


# Now let's get the movie titles:

# In[20]:


movie_titles = pd.read_csv("Movie_Id_Titles")
movie_titles.head()


# We can merge them together:

# In[21]:


df = pd.merge(df,movie_titles,on='item_id')
df.head()


# 
# Let's explore the data a bit and get a look at some of the best rated movies.
# 

# Let's create a ratings dataframe with average rating and number of ratings:

# In[22]:


df.groupby('title')['rating'].mean().sort_values(ascending=False).head()


# In[23]:


df.groupby('title')['rating'].count().sort_values(ascending=False).head()


# In[24]:


ratings = pd.DataFrame(df.groupby('title')['rating'].mean())
ratings.head()


# Now set the number of ratings column:

# In[25]:


ratings['num of ratings'] = pd.DataFrame(df.groupby('title')['rating'].count())
ratings.head()


# Now a few histograms:

# In[26]:


plt.figure(figsize=(10,4))
sns.histplot(data=ratings, x="num of ratings")


# In[27]:


plt.figure(figsize=(10,4))
sns.histplot(data=ratings, x="rating")


# In[28]:


sns.jointplot(x='rating',y='num of ratings',data=ratings,alpha=0.5)


# Okay! Now that we have a general idea of what the data looks like, let's move on to creating a simple recommendation system:

# ## Recommending Similar Movies

# Now let's create a matrix that has the user ids on one access and the movie title on another axis. Each cell will then consist of the rating the user gave to that movie. Note there will be a lot of NaN values, because most people have not seen most of the movies.

# In[29]:


moviemat = df.pivot_table(index='user_id',columns='title',values='rating')
moviemat.head()


# Most rated movie:

# In[30]:


ratings.sort_values('num of ratings',ascending=False).head(10)


# Let's choose two movies: starwars, a sci-fi movie. And Liar Liar, a comedy.

# In[31]:


ratings.head()


# Now let's grab the user ratings for those two movies:

# In[32]:


starwars_user_ratings = moviemat['Star Wars (1977)']
starwars_user_ratings.head()


# We can then use corrwith() method to get correlations between two pandas series:

# In[33]:


similar_to_starwars = moviemat.corrwith(starwars_user_ratings)


# Let's clean this by removing NaN values and using a DataFrame instead of a series:

# In[34]:


corr_starwars = pd.DataFrame(similar_to_starwars,columns=['Correlation'])
corr_starwars.dropna(inplace=True)
corr_starwars.head()


# Now if we sort the dataframe by correlation, we should get the most similar movies, however note that we get some results that don't really make sense. This is because there are a lot of movies only watched once by users who also watched star wars (it was the most popular movie). 

# In[35]:


corr_starwars.sort_values('Correlation',ascending=False).head(10)


# Let's fix this by filtering out movies that have less than 100 reviews (this value was chosen based off the histogram from earlier).

# In[36]:


corr_starwars = corr_starwars.join(ratings['num of ratings'])
corr_starwars.head()


# Now sort the values and notice how the titles make a lot more sense:

# In[37]:


corr_starwars[corr_starwars['num of ratings']>100].sort_values('Correlation',ascending=False).head()


# Now the same for the comedy Liar Liar:

# In[38]:


liarliar_user_ratings = moviemat['Liar Liar (1997)']


# In[39]:


similar_to_liarliar = moviemat.corrwith(liarliar_user_ratings)


# In[40]:


corr_liarliar = pd.DataFrame(similar_to_liarliar,columns=['Correlation'])
corr_liarliar.dropna(inplace=True)
corr_liarliar = corr_liarliar.join(ratings['num of ratings'])
corr_liarliar[corr_liarliar['num of ratings']>100].sort_values('Correlation',ascending=False).head()

