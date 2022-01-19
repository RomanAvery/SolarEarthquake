#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 18:02:05 2022

@author: roman
"""

import datetime
import pandas as pd
from os.path import exists

def load_omni2_cache():
    if exists('data/omni2.pickle'):
        print('Loading cached data')
        omni2 = pd.read_pickle('data/omni2.pickle')
        
    else:
        print('Generating data')
        from load_omni2_data import omni2
        omni2.to_pickle('data/omni2.pickle')
        
    return omni2

def get_columns(initial_vars, wanted_vars, wanted_props):
    columns = []
    
    # Add initial 
    for var in initial_vars:
        columns.append(var)
        
    # For each wanted variable, add a column with each needed property
    for var in wanted_vars:
        for prop in wanted_props:
            columns.append(var + '-' + prop)
    
    # Return columns
    return columns

def calculate_range(omni2, event, event_vals, vals, props, start, end):
    data_slice = omni2.loc[(omni2['Date'] >= start) & (omni2['Date'] <= end)]
    
    new_data = {}
    
    for val in event_vals:
        new_data[val] = event[val]
    
    # Calculate for each needed variable
    for val in vals:
        new_data[val + '-MEAN'] = data_slice[val].mean()
        new_data[val + '-MAX'] = data_slice[val].max()
        new_data[val + '-DELTA'] = data_slice[val].max() - data_slice[val].min()
        new_data[val + '-SD'] = data_slice[val].std()
    
    return new_data

def create_merged_df(omni2, event_data, event_vals, calc_vals, calc_props, hours_before):
    print('Starting events')
    
    count_t = 0
    rows = []
    
    for index, row in event_data.iterrows():
        end_date = row['date']
        
        # If date isn't correct, skip this one
        if end_date == pd.NaT:
            continue
        
        start_date = end_date - datetime.timedelta(hours = hours_before)
        
        if count_t % 100 == 0:
            print('Event #{}'.format(count_t))
        count_t += 1
        
        calc_row = calculate_range(omni2, row, event_vals, calc_vals, calc_props, start_date, end_date)
        rows.append(calc_row)
    
    print('Creating DataFrame')
    return pd.DataFrame(rows)