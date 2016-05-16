from sklearn import cross_validation
from sklearn import preprocessing
import numpy as np

'''
Author: Evelina Bakhturina

This module contains methods used to remove outliers, normalize and split the merged District Courts, Weather and Sports dataset.

'''

def create_final_target(df):
    #if glmax=glmin, we can't divide by zero when creating new target
    df['glmax-glmin'] = df['glmax'] - df['glmin']
    df = df[df['glmax-glmin'] != 0]

    #Create new target variable
    df['new_Y'] = (df['Y'] - (df['glmax'] + df['glmin'])/2.0)/df['glmax-glmin'] 

    #Drop outliers in our new target variable. See Ipython notebook Outliers where we plot our target variable 
    df = df[df['new_Y'] <= 100]
    df = df[df['new_Y'] >= -200]
    df = df[df.glmax <= 1200]
    df = df[df.glmin <= 1200]

    df.insert(0, 'Y', df['new_Y'])
    df= data.drop(['Y', 'glmax-glmin', 'new_Y', 'glmin', 'glmax'], 1)
    
    

def split_data(data):
    '''Splits the data into training and test sets (0.7/0.3)'''
    #Convert 'int64' into float; otherwise, sklearn throws a warning message
    columns = data.columns.values
    non_float = []
    for col in columns:
        if data[col].dtype != np.float64:
            non_float.append(col)
    for col in non_float:
        data[col] = data[col].astype(float)
        
    #Split the data
    split = cross_validation.ShuffleSplit(data.shape[0], n_iter=1, train_size = 0.7, test_size=.3, random_state = 1)

    for train, test in split:
        train_index = train
        test_index = test
    data_train = data.ix[train_index,:]
    data_test = data.ix[test_index,:]
    data_train.reset_index(drop=True, inplace=True)
    data_test.reset_index(drop=True, inplace=True)
    return data_train, data_test
    
    
def normalize(data_train, data_test):
    '''Transforms features by scaling each feature to (0,1) range.'''
    min_max_scaler = preprocessing.MinMaxScaler()
    data_train.ix[:,1:] = min_max_scaler.fit_transform(data_train.ix[:,1:])
    data_test.ix[:,1:] = min_max_scaler.transform(data_test.ix[:,1:]) 
    return data_train, data_test






