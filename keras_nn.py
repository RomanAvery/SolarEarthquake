#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 20:12:26 2022

@author: roman

Packages:
    - keras
    - tensorflow
    - joblib
    - pandas
    - numpy
    - scikit-learn
    - threadpoolctl
"""

from numpy import mean
from numpy import std
from numpy import asarray
from sklearn.datasets import make_regression
from sklearn.model_selection import RepeatedKFold
from keras.models import Sequential
from keras.layers import Dense
import pandas as pd

"""
    From https://machinelearningmastery.com/deep-learning-models-for-multi-output-regression/
"""

data = pd.read_csv('data/merge-isc_gem.csv', delimiter=',')
    
# Drop rows with NaN
data = data.dropna()

# get the dataset
def get_dataset():
    sample = data.sample(n=1000)
    X = sample[['magAFV-MEAN', 'sB-MEAN', 'PT-MEAN', 'PD-MEAN', 'PFS-MEAN', 'FP-MEAN', 'EF-MEAN', 'Kp-MEAN', 'DST-MEAN']].values
    y = sample[['lat', 'lon', 'mw']].values
    #X, y = make_regression(n_samples=1000, n_features=10, n_informative=5, n_targets=3, random_state=2)
    return X, y

# get the model
def get_model(n_inputs, n_outputs):
    model = Sequential()
    model.add(Dense(20, input_dim=n_inputs, kernel_initializer='he_uniform', activation='relu'))
    model.add(Dense(n_outputs))
    model.compile(loss='mae', optimizer='adam')
    return model

# evaluate a model using repeated k-fold cross-validation
def evaluate_model(X, y):
    results = list()
    n_inputs, n_outputs = X.shape[1], y.shape[1]
    # define evaluation procedure
    cv = RepeatedKFold(n_splits=10, n_repeats=3, random_state=1)
    
    print('Start training')
    
    # enumerate folds
    for train_ix, test_ix in cv.split(X):
        # prepare data
        X_train, X_test = X[train_ix], X[test_ix]
        y_train, y_test = y[train_ix], y[test_ix]
        # define model
        model = get_model(n_inputs, n_outputs)
        # fit model
        model.fit(X_train, y_train, verbose=0, epochs=100)
        # evaluate model on test set
        mae = model.evaluate(X_test, y_test, verbose=0)
        # store result
        print('>%.3f' % mae)
        results.append(mae)
    return model, results

# load dataset
X, y = get_dataset()
# evaluate model
model, results = evaluate_model(X, y)
# summarize performance
print('MAE: %.3f (%.3f)' % (mean(results), std(results)))

print('Predictions')

x_test, y_test = get_dataset()

h tscore = model.evaluate(x_test, y_test, verbose = 1) 

print('Test loss:', score[0]) 
print('Test accuracy:', score[1])

'''
sample = data.sample(n=10)
for index, row in sample.iterrows():
    newX = row[
        ['magAFV-MEAN', 
         'sB-MEAN', 
         'PT-MEAN', 
         'PD-MEAN', 
         'PFS-MEAN', 
         'FP-MEAN', 
         'EF-MEAN', 
         'Kp-MEAN', 
         'DST-MEAN']
        ].values.astype('float32')
    
    
    
    yhat = model.predict(newX)
    full_row = data.iloc[index]
    print(f'Predicted mw: {str(yhat[2])}, actual mw: {str(full_row["mw"])}')
'''