import numpy as np
from utils import read_dict_from_json, save_dict_to_json

high_freq_ingredient = read_dict_from_json('data/high_freq_food_dict.json')

h_food2index = {}
h_index2food = {}

for idx, ingredient in enumerate(high_freq_ingredient.keys()):
    h_food2index[ingredient] = idx
    h_index2food[idx] = ingredient

save_dict_to_json(h_food2index, 'data/h_food2index.json')
save_dict_to_json(h_index2food, 'data/h_index2food.json')