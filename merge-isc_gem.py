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

earthquake_data = pd.read_csv('data/isc-gem-cat.csv')

# Convert date column to datetime
earthquake_data['date'] = pd.to_datetime(earthquake_data['date'])

# Get earthquake data from AFTER start of omni2 (1963-11-28)
earthquake = earthquake_data[9309:]

"""
For each earthquake event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, depth, and magnitude
"""

# Lists of variables and properties we want
event_vals = ['date', 'lat', 'lon', 'depth', 'mw']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

out_data = create_merged_df(omni2, earthquake_data, event_vals, calc_vals, calc_props, hours_before)
    
out_data.to_csv('data/merge-isc_gem.csv')