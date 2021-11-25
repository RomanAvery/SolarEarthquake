#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 13:31:59 2021

@author: roman
"""

import pandas as pd
import dateparser as dp
import numpy as np
import datetime
from os.path import exists

if exists('data/omni2.pickle'):
    print('Loading cached data')
    omni2 = pd.read_pickle('data/omni2.pickle')
else:
    print('Generating data')
    from load_omni2_data import omni2

hours_before = 24

earthquake_data = pd.read_csv('data/isc-gem-cat.csv')

# Get earthquake data from AFTER start of omni2 (1963-11-28)
earthquake = earthquake_data[9603:]

"""
For each earthquake event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, depth, and magnitude
"""

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


# Lists of variables and properties we want
event_vals = ['date', 'lat', 'lon', 'depth', 'mw']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

print('Starting events')
count_t = 0

rows = []

for index, row in earthquake.iterrows():
    date = row['date']
    end_date = dp.parse(date)
    start_date = end_date - datetime.timedelta(hours = hours_before)
    
    count_t += 1
    print('Event #', count_t)
    
    calc_row = calculate_range(omni2, row, event_vals, calc_vals, calc_props, start_date, end_date)
    rows.append(calc_row)
    

#print('Creating column names')
#out_columns = get_columns(event_vals, calc_vals, calc_props)
    
# Adding to DataFrame
print('Creating DataFrame')
out_data = pd.DataFrame(rows)
    