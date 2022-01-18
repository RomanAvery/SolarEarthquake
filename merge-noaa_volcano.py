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
    omni2.to_pickle('data/omni2.pickle')
    
print('Starting merge')

hours_before = 24

# Load NOAA volcano data
volcano_data = pd.read_csv('data/volcano-events-2022-01-19_12-16-42_+1300.tsv', sep='\t', header=0)

# Rename date columns so we can get a datetime
volcano_data.rename(columns = {'Year':'year', 'Mo':'month', 'Dy':'day'}, inplace = True)

# Create datetime objects
volcano_data['date'] = pd.to_datetime(volcano_data[['year','month','day']])

# Get only events from after start of OMNI2 dataset
volcano = volcano_data[7:]

"""
For each volcano event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, elevation, and type
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
event_vals = ['date', 'Latitude', 'Longitude', 'Elevation (m)', 'Type']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

print('Starting events')
count_t = 0

rows = []

for index, row in volcano.iterrows():
    end_date = row['date']
    
    if end_date == pd.NaT:
        continue
    
    start_date = end_date - datetime.timedelta(hours = hours_before)
    
    if count_t % 100 == 0:
        print('Event #{}'.format(count_t))
    count_t += 1
    
    calc_row = calculate_range(omni2, row, event_vals, calc_vals, calc_props, start_date, end_date)
    rows.append(calc_row)
    

#print('Creating column names')
#out_columns = get_columns(event_vals, calc_vals, calc_props)
    
# Adding to DataFrame
print('Creating DataFrame')
out_data = pd.DataFrame(rows)
    
out_data.to_csv('data/merge-noaa_volcano.csv')
