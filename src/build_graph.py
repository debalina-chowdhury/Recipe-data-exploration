import ast
import operator
import itertools
import numpy as np
import pandas as pd
import pyvis as pv
import matplotlib.pyplot as plt
from utils import read_dict_from_json, save_dict_to_json


file_path = 'data/ingredient_graph.csv'
df = pd.read_csv(file_path, index_col=0)
h_food2index = read_dict_from_json('data/h_food2index.json')
h_index2food = read_dict_from_json('data/h_index2food.json')

all_connection_dict = {}


def tuple2string(t):
    """
    convert a tuple to a string
    """
    return '{}_{}'.format(t[0], t[1])

def string2tuple(s):
    """
    convert a string to a tuple
    """
    return tuple(s.split('_'))


def build_connection(ing_list):
    """
    all effective ingredient in a dish will be connected
    :param ing_list: list of ingredients
    :return: a list of two-element tuples
    """
    assert isinstance(ing_list, list)

    ing_idx_list = []
    for i in ing_list:
        if i in h_food2index:
            ing_idx_list.append(h_food2index[i])

    if len(ing_idx_list) < 2: return []
    # add every two item index in the list to a two-element tuple
    connection_lists = list(itertools.combinations(ing_idx_list, 2))
    return connection_lists

def build_connection_dict():
    for idx, row in df.iterrows():
        if isinstance(row['ingredients'], str) and row['ingredients'].startswith('[') and row['ingredients'].endswith(']'):
            food_ingredient = ast.literal_eval(row['ingredients'])
            assert isinstance(food_ingredient, list), 'ingredient is not a list'
            connected_ing = build_connection(food_ingredient)
            for pair in connected_ing:
                pair_s = tuple2string(pair)
                if pair_s in all_connection_dict:
                    all_connection_dict[pair_s] += 1
                else:
                    all_connection_dict[pair_s] = 1

# save_dict_to_json(all_connection_dict, 'data/all_connection_dict.json')

all_connection_dict = read_dict_from_json('data/all_connection_dict.json')
all_connection_list = list(all_connection_dict.keys())
ing_connection_list = [string2tuple(pair) for pair in all_connection_list]
idx_connection_list = list(all_connection_dict.values())

sorted_connection_dict = dict(sorted(all_connection_dict.items(), key=operator.itemgetter(1), reverse=True)) 
save_dict_to_json(sorted_connection_dict, 'data/sorted_all_connection_dict.json')

# plt.plot(list(sorted_connection_dict.values()))
# plt.savefig('data/ingredient_connection_count.png')
# plt.show()



# for pair, freq in all_connection_dict.items():
#     ing_pair = string2tuple(pair)



# label_list = list(h_index2food.values())
