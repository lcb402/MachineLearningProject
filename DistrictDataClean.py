import pandas as pd
from datetime import *

'''
Author: Nora Barry

This module contains methods used to load and clean the District Courts dataset.

'''

def read_csv(file_name):
    df = pd.read_csv(file_name)
    print df.shape
    return df

def drop_cols(df, lst_of_cols):
    '''Enter list of columns to keep in the dataframe.'''
    df = df.drop(lst_of_cols, 1)
    return df

def drop_nas(df, lst_of_cols):
    #Drop NaNs according to certain columns, namely date and target variable senttot0
    df = df.dropna(how = 'any', subset = cols)
    return df


def convert_dates(df, col_name):
    #Convert Stata dates to datetime
    dates = []
    start_date = datetime(1960, 1, 1, 0, 0)
    for num in df[col_name]:
        num_days = timedelta(days = int(num))
        date_time = start_date + num_days
        dates.append(date_time.date())
    df['date_for_merge'] = dates
    df['date_for_merge'] = [str(df['date_for_merge'][i]) for i in range(df.shape[0])]
    
    
def create_baseline_target(df):
    '''Create a feature in {-1, 1} that indicates whether the sentence falls in lower half or upper half of guideline range. We use this feature as our target variable for baseline model.'''
    rangept = []
    for i in range(df.shape[0]):
        median = (df['glmax'][i] - df['glmin'][i])/2.0
        if df['senttot0'][i] > median:
            rangept.append(1)
        else:
            rangept.append(-1)
    df['Y'] = rangept
    
    
def prep_for_merge(df):
    #Rename courthouse column to city to match weather data
    df = df.rename(columns={'courthouse':'city'})
    return df


