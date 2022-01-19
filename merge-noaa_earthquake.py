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

from merge_tools import load_omni2_cache, get_columns, calculate_range, create_merged_df

omni2 = load_omni2_cache()
    
print('Starting merge')

hours_before = 24

# Load NOAA earthquake data
earthquake_data = pd.read_csv('data/earthquakes-2022-01-19_12-19-32_+1300.tsv', sep='\t', header=0)

# Rename date columns so we can get a datetime
earthquake_data.rename(columns = {'Year':'year', 'Mo':'month', 'Dy':'day', 'Hr':'hour'}, inplace = True)

# Create datetime objects
earthquake_data['date'] = pd.to_datetime(earthquake_data[['year','month','day', 'hour']])

"""
For each volcano event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, elevation, and type
"""

# Lists of variables and properties we want
event_vals = ['date', 'Latitude', 'Longitude', 'Mag']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']


out_data = create_merged_df(omni2, earthquake_data, event_vals, calc_vals, calc_props, hours_before)
    
out_data.to_csv('data/merge-noaa_earthquake.csv')
