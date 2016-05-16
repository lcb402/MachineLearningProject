from DistrictDataClean import *
from WeatherDataClean import *

'''
Author: Nora Barry

This module contains methods used to merge the District Court and Weather datasets.

'''

def find_lost_cities(weather_df, district_df):
    #Some cities in weather data don't match with district cities. This function creates list of these cities.
    weather_not_district = []
    for city in weather_df['city'].unique():
        if city not in district_df['city'].unique():
            weather_not_district.append(city)
    return weather_not_district

def alter_lost_cities(weather_df, district_df, metadata, cities):
    '''Input weather and district courts dataframes, metadata (Weather_District_Metadata.csv), and list of cities that don't match. This function returns a new weather dataframe with cities that match up with the cities in the District Courts dataset.'''
    i = 0
    weather_df2 = weather_df.copy()
    for city in weather_df['city'].unique():
        if city in cities:
            replace = metadata[metadata['In Weather-Not District'] == city]['Weather Match']
        weather_df2.city.replace(str(city), str(replace[i]), inplace = True)
        i += 1
    return weather_df2


def perform_merge(weather_df, district_df):
    #Merge weather and district courts dataframes on date and city.
    merged = district_df.merge(weather_df, how = 'inner', on = ['date_for_merge','city'])
    print merged.shape
    return merged

