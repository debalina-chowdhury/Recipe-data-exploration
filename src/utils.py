import os
import json
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import numpy as np
from collections import Counter

def make_plots(data,title,x='date',y='calories',z='line',time='year'):
    """Function takes a dataframe and the column names to make a plot of x v/s y. where x is datatime.
    The type of plot is specified as z. The function makes a plot of means of each year.
    """
    assert isinstance(data,pd.DataFrame)
    assert x in data.columns.values.tolist()
    assert y in data.columns.values.tolist()
    assert z in ['line','bar','box']
    sns.set()
    fig, axs = plt.subplots(figsize=(12, 4))
    if(time=='year'):
        data.groupby(data[x].dt.year)[y].mean().plot(kind=z, rot=0, ax=axs)
        plt.xticks(range(2002,2017))
        axs.set_xlim([2002,2017])
     
    elif(time=='month'):
        data.groupby(data[x].dt.month)[y].mean().plot(kind=z, rot=0, ax=axs,xticks=np.arange(0,12))
        axs.set_xticklabels(["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"])
    else:
        data.groupby(data[x].dt.day)[y].mean().plot(kind=z, rot=0, ax=axs)
    plt.title(title)
    plt.xlabel(time)
    plt.ylabel(y)

def extract_features(df,col,new_cols):
    """This function takes a dataframe df and extracts values in lists given by
    column col and places them in columns given by new_cols (values returned are numeric) and 
    returns a dataframe with the new columns
    """
    assert isinstance(df,pd.DataFrame)
    assert col in df.columns
    # checks if the column is an object (by default strings are treated as objects in pandas)
    if isinstance(df.dtypes[col],object):
        df[col] = df[col].apply(lambda x: x[1:-1].split(','))
    for i in range(len(new_cols)):
        df[new_cols[i]]=df[col].str[i]
        df[new_cols[i]]=pd.to_numeric(df[new_cols[i]])
    return(df)

def popular_ingredients(df,year):
    """
    Takes a dataframe and year and returns a counter with the counts of all ingredients consumed in the year
    """
    assert year>=df['year'].min() and year<=df['year'].max()
    assert isinstance(df,pd.DataFrame)
    df2=df[(df.year == year)]
    series=df2['ingredients']
    series=series.tolist()
    count = Counter()
    for i in range(len(series)):
        count.update(series[i])
    return(count)

def count_ingredients(df,name):
    """
    counts ingredients over all years and returns a list (normalised over the year)
    
    """
    assert isinstance(df,pd.DataFrame)
    year=df['year'].min()
    y=[]
    while year<=df['year'].max():
        denom=len(df[df['year'] == year])
        count=popular_ingredients(df,year)
        sums=0
        for key in count.keys():
            if name in key:
                sums+=count[key]
        y.append(sums/denom)
        year+=1
    return(y) 


def save_dict_to_json(item, path, overwrite=True):
    if os.path.exists(path) and overwrite is False:
        print("{} already exists".format(path))
    else:
        try:
            item = json.dumps(item, indent=4)
            with open(path, "w", encoding='utf-8') as f:
                f.write(item)
                print("success write dict to json: {}".format(path))
        except Exception as e:
            print("write error==>", e)

def read_dict_from_json(path):
    try:
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print("{} successfully loaded!".format(path))
                return data
        else:
            print("{} does not exist!".format(path))
    except Exception as e:
        print("read error==>", e)
