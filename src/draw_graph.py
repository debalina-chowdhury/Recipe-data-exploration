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
print('1')
all_connection_list = list(all_connection_dict.keys())
print('2')
idx_connection_list = [string2tuple(pair) for pair in all_connection_list[:100]]
print('3')
idx_connection_list = [get_connection_weight(int(x1), int(x2)) for x1, x2 in idx_connection_list]
print('4')
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


# net.add_nodes([1, 2], label=['Alex', 'Carthy'])
# net.add_nodes([3, 4, 5, 6], 
#               label=['Michael', 'Ben', 'Oliver', 'Olivia'],
#               color=['#3da831', '#9a31a8', '#3155a8', '#eb4034'])

# net.add_edge(1, 5)
# net.add_edges([(2, 5, 10), (3, 4, 2), (1, 6), (2, 6), (3, 5)])
net.show('edges_with_weights.html')
