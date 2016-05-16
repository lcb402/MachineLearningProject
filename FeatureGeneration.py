import pandas as pd
from datetime import *
import numpy as np
import math

'''
Authors: Nora Barry and Evelina Bakhturina

This module contains methods used to create dummy variables for the categorical features in the District Courts dataset.

'''

def find_categoricals(df):
    '''Find the categorical variables in the dataframe.'''
    cols = df.columns
    num_cols = df._get_numeric_data().columns
    cat_vars = list(set(cols) - set(num_cols))
    return cat_vars

def make_dummy_variables(dataframe, features):
    #Input dataframe, and list of features returned by find_categoricals create dummy columns
    uniques = dataframe[feature].unique()
    lst = list(uniques)
    for x in lst:
        if isinstance(x,float) and math.isnan(x):
            lst.remove(x)
    if np.nan in lst:
        lst.remove(np.nan)
    uniques = sorted(lst)
    dummies = pd.get_dummies(dataframe[feature])
    colnames = ['{}_{}'.format(str(feature), str(x)) for x in uniques]
    dummies.columns = colnames
    dummies.drop(colnames[-1], axis=1, inplace=True)
    return dummies

def clean_categorical_vars(dataframe, list_of_cat_vars):
    '''Append the original dataframe with output of make_dummy_variables. This function also adds a binary column for each feature that has missing values. This binary column is 1 if value is missing.'''
    for column in dataframe.columns:
        if (np.any(dataframe[column].isnull())):
            dataframe[column + "_mv"] = dataframe[column].isnull().astype(int)
    for var in list_of_cat_vars:
        dummies = make_dummy_variables(dataframe, var)
        dataframe = pd.concat([dataframe, dummies], axis=1)
        dataframe = dataframe.drop(var, axis=1)
    return dataframe

def alter_cat_vars(df, lst_of_cols):
    '''Use this function to create dummy variables for sequential categorical vars, namely 'neweduc' (education level). We use this to indicate that if a defendent completed college, he/she also completed HS'''
    for col in lst_of_cols:
        max_value = max(df[col])
        uniq = df[col].unique()
        uniq[::-1].sort()
        for num in uniq:
            if num == max_value:
                df[col + "_" + str(max_value)] = (df[col] == max_value).astype(int)
            elif num != uniq[-1]:
                df[col + "_" + str(num)] = ((df[col] == num) + df[col + "_" + str(max_value)]).astype(int)
                

def drop_life_death(df):
    #Here we drop all instances where the court case ended in either a life or death sentence, so we avoid outliers in data
    df = df[df['life'] == 0]
    df = df[df['death'] == 0]
    return df

def save_data(df, filename):
    #Save data as csv 
    df.to_csv(filename)
                
