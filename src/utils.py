from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd

def make_plots(data,title,x='date',y='calories',z='line',time='year'):
    """Function takes a dataframe and the column names to make a plot of x v/s y. where x is datatime.
    The type of plot is specified as z. The function makes a plot of means of each year.
    """
    assert isinstance(data,pd.DataFrame)
    assert x in data.columns.values.tolist()
    assert y in data.columns.values.tolist()
    assert z in ['line','bar']
    fig, axs = plt.subplots(figsize=(12, 4))
    if(time=='year'):
        data.groupby(data[x].dt.year)[y].mean().plot(
    kind=z, rot=0, ax=axs)
    elif(time=='month'):
        data.groupby(data[x].dt.month)[y].mean().plot(
    kind=z, rot=0, ax=axs)
    else:
        data.groupby(data[x].dt.day)[y].mean().plot(
    kind=z, rot=0, ax=axs)
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
