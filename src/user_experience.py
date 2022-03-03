#import libraries
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import re
from collections import Counter
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS
import numpy as np

##User experience exploration

def plot_user_rating(Merged_data):
    '''
    This function helps in visualizing trend of average user ratings given to the recipes
    param Merged_data: a pandas DataFrame
    return: None
    '''
    assert isinstance(Merged_data,pd.DataFrame), "Please provide valid Dataframe"
    user_rating=Merged_data.groupby(['user_id'])['rating'].mean().sort_values(ascending=True).reset_index(name='user_average_rating')
    user_rating['user_category']=pd.cut(user_rating['user_average_rating'],5, labels=['0.0-1.0', '1.0-2.0', '2.0-3.0', '3.0-4.0','4.0-5.0'])
    user_rating=user_rating.groupby('user_category')['user_id'].count().reset_index(name='user_count')
    user_rating.plot.bar(x='user_category',y='user_count',rot=50)

def plot_yearwise_highest_n_unique_recipes(Merged_data):
    '''
    This function help in visualizing yearwise trend of 
    top 3 highest number of unique recipes cooked by 3 users in a year
    param Merged_data: a pandas DataFrame
    return: None
    '''
    assert isinstance(Merged_data,pd.DataFrame), "Please provide valid DataFrame"
    recipe_user_interaction=Merged_data.groupby(['year','user_id'])['id'].nunique().reset_index(name='yearwise_user_recipe')
    recipe_user_interaction=recipe_user_interaction[['year','user_id','yearwise_user_recipe']].sort_values(by=['year','yearwise_user_recipe'], ascending=False)
    recipe_user_interaction=recipe_user_interaction.groupby('year').head(3).reset_index()
    recipe_user_interaction.pop('index')
    recipe_user_interaction.pop('user_id')
    recipe_user_interaction=recipe_user_interaction.groupby('year')['yearwise_user_recipe'].agg(lambda x: list(x)).reset_index(name='yearwise_list')
    dict1={}
    for i in range(len(recipe_user_interaction)):
        dict1[recipe_user_interaction.year[i]]=recipe_user_interaction.yearwise_list[i]
    recipe_user_interaction2=pd.DataFrame.from_dict(dict1)
    recipe_user_interaction2=recipe_user_interaction2.transpose()
    recipe_user_interaction2.rename({0:'#unique recipes for user with #highest unique recipes',
                      1:'#unique recipes for user with #2nd highest unique recipes',
                      2:'#unique recipes for user with #3rd highest unique recipes'}, axis=1, inplace=True)
    recipe_user_interaction2.plot.bar(rot=50)

def preprocess(text):
    '''
    This function converts all characters into lowercase, removes the punctuations and removes stopwords from a text
    param text: a string
    return: a preprocessed string
    '''
    assert isinstance(text,str)
    text=text.lower()
    text=re.sub(r'[^\w\s]', '', text)
    stop_words=set(stopwords.words('english'))
    stop_words.update(['recipe','ingredient','salt','water',
                       'use','used','made','make','instead',
                       'still','another','added','add','thank',
                       'ingredients','thanks','review','reviews',
                          'cook','cooking','time'])
    text= ' '.join([w for w in text.split(' ') if w not in stop_words])
    return text


def high_rating_recipes_wordcloud(Merged_data):
    '''This function develops a wordcloud of the recipes with highest number of top ratings for each year
    param Merged_data: a pandas DataFrame
    return: None
    '''
    high_rating_recipes=Merged_data[Merged_data['rating']==5].groupby(['year','id','name','ingredients'])['rating'].count().reset_index(name='highest_rating_count')
    high_rating_recipes=high_rating_recipes.sort_values(by=['year','highest_rating_count'], ascending=False)
    high_rating_recipes=high_rating_recipes[['year','name','ingredients','highest_rating_count']].groupby(['year']).head(1).reset_index()
    high_rating_recipes.pop('index')
    high_rating_recipes.pop('ingredients')
    df_reviews=Merged_data[Merged_data['rating']==5]
    df_reviews=df_reviews.dropna()
    df_reviews=df_reviews[['year','id','name','review']].groupby(['year','name'])['review'].apply(' '.join).reset_index()    #.transform(lambda x: ' '.join(x))  #.apply(' '.join).reset_index()
    df_reviews['review']=df_reviews['review'].apply(preprocess)
    high_rating_recipes=pd.merge(high_rating_recipes,df_reviews, on=['year','name'])
    high_rating_recipes_reviews=''
    for i in high_rating_recipes['review']:
        high_rating_recipes_reviews+=i+' '
    high_rating_recipes_reviews
    wordcloud = WordCloud(width = 800, height = 800,
                    background_color ='white',
                    min_font_size = 10).generate(low_rating_recipes_reviews)
    # plot the WordCloud image                      
    plt.figure(figsize = (6, 6), facecolor = None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad = 0)
    plt.show()