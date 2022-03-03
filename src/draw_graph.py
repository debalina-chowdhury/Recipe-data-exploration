import pdb
import ast
import operator
import itertools
import numpy as np
import pandas as pd
import pyvis as pv
from utils import read_dict_from_json, save_dict_to_json

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

def get_connection_weight(i, j):
    """
    get the weight of the connection between i and j
    :param i: the first node (int)
    :param j: the second node (int)
    :return: (i, j, weight)
    """
    assert i != j
    assert isinstance(i, int)
    assert isinstance(j, int)
    freq = all_connection_dict['{}_{}'.format(i, j)]
    return (i, j, np.log(freq))


index2food = read_dict_from_json('data/h_index2food.json')
# all_idx_list, all_food_list = list(index2food.keys()), list(index2food.values())
all_connection_dict = read_dict_from_json('data/sorted_all_connection_dict.json')
all_connection_list = list(all_connection_dict.keys())
idx_connection_list = [string2tuple(pair) for pair in all_connection_list[500:700]]
idx_connection_list = [get_connection_weight(int(x1), int(x2)) for x1, x2 in idx_connection_list]
# print(idx_connection_list)


x = set()
for pair in idx_connection_list:
    if pair[0] not in x:
        x.add(pair[0])
    if pair[1] not in x:
        x.add(pair[1]) 

all_idx_list = list(x)
all_food_list = [index2food[str(idx)] for idx in all_idx_list]


from pyvis.network import Network
import numpy as np

net = Network(height="800px", width="1200px")
net.add_nodes(all_idx_list, label=all_food_list)
net.add_edges(idx_connection_list)
net.show_buttons(filter_=['physics'])

net.show('food_connection.html')
