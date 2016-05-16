import pandas as pd
import numpy as np
import datetime

'''
Author: Nora Barry

This module contains methods used to load and clean the Weather dataset.

'''

def read_csv(file_name):
    df = pd.read_csv(file_name)
    print df.shape
    return df

def drop_nas(df):
    '''Missing values are recorded as -9999. Use this function to see what features have less than 5% missing values, and choose features from this list to use in modeling'''
    df = df.replace('-9999', np.nan)
    df = df.dropna(thresh = .95*df.shape[0], axis = 1)
    print df.shape
    return df

def keep_cols(df, lst_of_cols):
    '''Input your dataframe, and list of columns to keep. Here we decide to keep 'logsun_min', 'logprcp_mm','logtemp_min','cloud_pct', 'year', 'month', 'day','city' '''
    df = df[lst_of_cols]
    return df

def convert_dates(df):
    #Create a datetime object from columns year, month, day
    dates = []
    for i in range(1,df.shape[0]+1):
        if int(df['month'][i] < 10):
            month = str(0) + str(df['month'][i])
        else:
            month = str(df['month'][i])
        if int(df['day'][i] < 10):
        day = str(0) + str(df['day'][i])
        else:
            day = str(df['day'][i])
        date = datetime.datetime.strptime(str(df2['year'][i])+month+day,'%Y%m%d')
        dates.append(date)
    df['date_for_merge'] = dates 

    
def prep_for_merge(df):
    '''Reformat datetime objects in column date_for_merge so that they match format of district court dates'''
    dates = []
    df['date_for_merge'] = [str(df['date_for_merge'][i]) for i in range(1, df.shape[0]+1)]
    for date in df['date_for_merge']:
        date = date.split(' ')
        date = date[0]
        dates.append(date)
    df['date_for_merge'] = dates
    return df
