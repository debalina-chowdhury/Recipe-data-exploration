# Import Libs
# In[]
# import necessary libs
import os
import ast
import json
import math
from unittest.util import sorted_list_difference
import numpy
import string
import random
import string
import operator
import pandas as pd
import matplotlib.pyplot as plt
from utils import make_plots,extract_features

# In[]
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

# Import data
# In[]
# data_recipes=pd.read_csv('data/RAW_recipes.csv', index_col=1, usecols=['id','name','ingredients']) 
# data_recipes.to_csv('data/ingredient_graph.csv')


# # data_interactions=pd.read_csv('data/RAW_interactions.csv')  
# print(data_recipes.head())

# df[['calories','total fat (PDV)','sugar (PDV)','sodium (PDV)',
# 'protein (PDV)','saturated fat (PDV)','carbohydrates (PDV)']] \
#     = df.nutrition.str.split(",",expand=True) 

# df['calories'] =  df['calories'].apply(lambda x: x.replace('[','')) 
# df['carbohydrates (PDV)'] =  df['carbohydrates (PDV)'].apply(lambda x: x.replace(']','')) 

# In[]
# analysis on ingredients 

def ingredient_stat(data):
    """
    count ingredient and build connections
    :param data: dataframe of ingredients
    :return: graph
    """

    # count ingredient
    ingredients = data['ingredients'].tolist()
    food_dict = {}
    for ingredient in ingredients:
        if isinstance(ingredient, str) and ingredient.startswith('[') and ingredient.endswith(']'):
            list_data = ast.literal_eval(ingredient)
            for item in list_data:
                if item in food_dict:
                    food_dict[item] += 1
                else:
                    food_dict[item] = 1
    sorted_food_dict = dict(sorted(food_dict.items(), key=operator.itemgetter(1), reverse=True)) 
    return sorted_food_dict


def select_high_freq(data, high_freq_dict):
    """
    select high frequency ingredients
    """

    pass


def build_graph(ingredients):
    """
    build graph of ingredients
    """
    for ingredient in ingredients:
        pass



if __name__ == '__main__':
    # data = pd.read_csv('data/ingredient_graph.csv', index_col=0)
    # food_dict = ingredient_stat(data)
    # save_dict_to_json(food_dict, 'data/ingredient_graph.json')
    # food_dict = read_dict_from_json('data/ingredient_graph.json')

    # high_freq_food_dict = {}
    # for food, freq in food_dict.items():
    #     if freq >= 15:
    #         high_freq_food_dict[food] = freq
    # save_dict_to_json(high_freq_food_dict, 'data/high_freq_food_dict.json')
    # print(type(food_dict))
    # plt.plot(list(food_dict.values()))
    # plt.savefig('data/ingredient_freq.png')
    # plt.show()

    graph = pd.read_csv('data/ingredient_graph.csv', index_col=0)
    


