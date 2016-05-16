from DistrictDataClean import *
from FeatureGeneration import *
from WeatherDataClean import *
from District_WeatherMerge import *
from Normalization_and_Split import *
from SportsCleanAndMerge import *
import os


cols_to_drop = ['Unnamed: 0', 'ussc_fy','groupedprogramcategory','senttot','prisonordered','amtfinec', 'amttotal','fine','departure','govdeparture','hsdeparture_gl','hsdeparture_x','hsdep0','hsdeparture','normed_sentence','gunmin3',
 'offcodc1','offcodc2','offcodc3','offcodc4','anyprison','logfine','logprison','date_source','crime', 'pooffice','offtype2']

weather_cols_to_keep = ['logsun_min', 'logprcp_mm','logtemp_min','cloud_pct', 'year', 'month', 'day','city']


#Clean District Courts Data
df = read_csv('initial_data.csv')
df = drop_cols(df, cols_to_drop )
df = drop_nas(df, ['senttot0', 'date'])
convert_dates(df, 'date')
create_baseline_target(df)
df = prep_for_merge(df)


#Generate New Features for District Dataset
df = clean_categorical_variables(df,['district','monrace','newrace','crimetype','state'])
alter_cat_vars(df, ['neweduc'])
df = drop_life_death(df)


#Clean Weather Data
weather = read_csv('weather_by_city.csv')
weather = drop_nas(weather)
weather = keep_cols(weather, weather_cols_to_keep)
convert_dates(weather)
weather = prep_for_merge(weather)


#Merge District and Weather
metadata = read_csv('Weather_District_Metadata.csv')
lost_cities = find_lost_cities(weather, df)
weather = alter_lost_cities(weather, df, metadata, lost_cities)
merged = perform_merge(weather, df)


#Merge District and Weather With Sports
merged = os.system('SportsCleanAndMerge.py')

#Save Dataframe for Baseline Model
merged = drop_cols(merged, ['date_for_merge', 'city'])
save_data(merged, 'baseline_1.csv')

#Create New Target and Remove Outliers
create_final_target(merged)
save_data(merged, 'Final_Data.csv')

#Split and Normalize Data
data_train, data_test = split_data(merged)
data_train, data_test = normalize(data_train, data_test)
save_data(data_train, 'Final_Data_Train_2.csv')
save_data(data_test, 'Final_Data_Test_2.csv')


