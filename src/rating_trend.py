import pandas as pd
import numpy as np
from statsmodels.tsa.api import ExponentialSmoothing, SimpleExpSmoothing, Holt

def aggregate_reviews(df_recipe, df_interactions, from_year=2000, to_year=2019):
    """
    returns average review ratings during the entire time period and by each year of
    each of the recipes
    
    params:
    df_recipe: pd.DataFrame: raw recipe data
    df_interactions: pd.DataFrame: raw review data
    from_year: int: start date of aggregation, inclusive
    to_year: int: end year of aggregation, exclusive
    
    returns:
    reviews: dict[int, list]: aggregated review scores by year of each recipe
    """
    reviews = dict()

    n_years = to_year - from_year
    interaction_years = [int(x[:4])-from_year for x in df_interactions["date"]]

    for rid, year, score in zip(df_interactions["recipe_id"], interaction_years, df_interactions["rating"]):
        if rid not in reviews:
            reviews[rid] = [0, 0, [0] * n_years, [0] * n_years]
        reviews[rid][0] += 1
        reviews[rid][1] += score
        reviews[rid][2][year] += 1
        reviews[rid][3][year] += score

    for rid in reviews:
        reviews[rid][1] /= reviews[rid][0]
        for i in range(n_years):
            reviews[rid][3][i] /= max(reviews[rid][2][i], 1)
            
    return reviews


def get_range(x):
    """
    returns the range of a given integer collection
    
    params:
    x: iterable: integer collection
    
    returns:
    from_value: min value, inclusive
    to_value: max value, exclusive
    """
    from_value = min(x)
    to_value = max(x) + 1
    return from_value, to_value


def get_summary(df_recipe, df_interactions, from_year=2000, to_year=2019):
    """
    get a summary collection of data of the recipe reviews
    
    params:
    df_recipe: pd.DataFrame: raw recipe data
    df_interactions: pd.DataFrame: raw review data
    from_year: int: start date of aggregation, inclusive
    to_year: int: end year of aggregation, exclusive
    
    returns:
    avg_ratings: list[int]: number of all reviews posted by each year
    count_reviews: list[float]: average rating over all recipes by each year
    """
    n_years = to_year - from_year
    yearly_scores = [[] for _ in range(n_years)]
    interaction_years = [int(x[:4])-from_year for x in df_interactions["date"]]
    
    for rid, year, score in zip(df_interactions["recipe_id"], interaction_years, df_interactions["rating"]):
        yearly_scores[year].append(float(score))
        
    avg_ratings = [np.mean(x) for x in yearly_scores]
    count_reviews = [len(x) for x in yearly_scores]
    
    return avg_ratings, count_reviews


def get_review_slope(reviews):
    """
    fit the yearly rating of each recipe over the last 10 years
    with a linear model and compute its slope
    only recipes that has at least 1 review made for each year
    during the period will be included
    
    params:
    reviews: dict[int, list]: aggregated review scores by year of each recipe
    
    returns:
    slopes: list[float]: slope of fitted rating trend, sorted in ascending order
    rids: list[id]: corresponding recipe ids that has a slope
    """
    rids = []
    slopes = []
    
    x = list(range(10))
    for rid in reviews:
        if min(reviews[rid][2][-10:]) > 0:
            data = reviews[rid][3][-10:]

            fit_model = np.polyfit(x, data, 1)
            rids.append(rid)
            slopes.append(fit_model[0])

    zipped = list(zip(rids, slopes))
    zipped.sort(key=lambda x:x[1])
    rids, slopes = [list(x) for x in zip(*zipped)]
            
    return rids, slopes


def smooth(x):
    """
    smooth a given data series with exponential smoothing
    
    params:
    x: list: input list of data
    
    returns:
    s: smoothed list of data
    """
    model = SimpleExpSmoothing(x, initialization_method="estimated").fit(smoothing_level=0.3)
    s = model.fittedvalues
    return s


def get_dict(keys, vals):
    """
    create a dictionary from given list of corresponding keys and values
    
    params:
    keys: list: 
    vals: list: 
    
    returns:
    res: dict: resulting dictionary
    """
    return dict(zip(keys, vals))


def parse_list_str(s):
    """
    create a dictionary from given list of corresponding keys and values
    
    params:
    s: list[str]: list of list-strings, all string should be parsed into list[float] of same length
    
    returns:
    ll: list[list]: resulting list of list
    """
    listlen = 7
    ll = [[] for _ in range(listlen)]
    for ss in s:
        l = [float(x) for x in ss[1:-1].split(',')]
        for j in range(listlen):
            ll[j].append(l[j])
            
    return ll