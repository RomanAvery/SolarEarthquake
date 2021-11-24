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

def create_dataframe(initial_vars, wanted_vars, wanted_props):
    # Make empty dataframe
    data = pd.DataFrame()
    
    # Add initial 
    for var in initial_vars:
        data[var] = np.nan
        
    # For each wanted variable, add a column with each needed property
    for var in wanted_vars:
        for prop in wanted_props:
            data[var + '-' + prop] = np.nan
    
    # Return DataFrame
    return data

def calculate_range(out_data, omni2, event, event_vals, vals, props, start, end):
    data_slice = omni2.loc[(omni2['Date'] >= start) & (omni2['Date'] <= end)]
    
    new_data = {}
    
    #for val in event_vals:
    #    new_data[val] = event[val]
    new_data['date'] = event['date']
    
    # Calculate for each needed variable
    for val in vals:
        MEAN = 0.0
        MEAN_COUNT = 0
        MAX = -999999.0
        MIN = 999999.0
        DELTA = 0.0
        SD = 0.0
        
        # Iterate each row of the slice
        for index, row in data_slice.iterrows():
            # Calc mean
            MEAN += row[val]
            MEAN_COUNT += 1
            
            # Calc max
            if row[val] > MAX:
                MAX = row[val]
            
            # Calc min
            if row[val] < MIN:
                MIN = row[val]
          
        
        if MEAN_COUNT > 0:
            MEAN = MEAN / MEAN_COUNT
        else:
            MEAN = 0
            
        new_data[val + '-MEAN'] = MEAN
        
        # Calc delta
        DELTA = MAX - MIN
        new_data[val + '-DELTA'] = DELTA
        
    # Add data to the DataFrame
    out_data.append(new_data, ignore_index=True)


# Lists of variables and properties we want
event_vals = ['date', 'lat', 'long', 'depth', 'mw']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

out_data = create_dataframe(event_vals, calc_vals, calc_props)

for index, row in earthquake.iterrows():
    date = row['date']
    end_date = dp.parse(date)
    start_date = end_date - datetime.timedelta(hours = hours_before)
    
    calculate_range(out_data, omni2, row, event_vals, calc_vals, calc_props, start_date, end_date)
    
    