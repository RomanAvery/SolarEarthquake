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

from merge_tools import load_omni2_cache, get_columns, calculate_range

omni2 = load_omni2_cache()
    
print('Starting merge')

hours_before = 24

"""
For each set of 24 OMNI2 points each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, elevation, and type
"""

# Lists of variables and properties we want
event_vals = ['Date']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']


print('Starting events')

count_row = 0
count_t = 0
rows = []

for index, row in omni2.iterrows():
    if count_row % hours_before == 0:
        end_date = row['Date']
        
        # If date isn't correct, skip this one
        if end_date == pd.NaT:
            continue
        
        start_date = end_date - datetime.timedelta(hours = hours_before)
        
        if count_t % 100 == 0:
            print('Event #{}'.format(count_t))
        count_t += 1
        
        calc_row = calculate_range(omni2, row, event_vals, calc_vals, calc_props, start_date, end_date)
        rows.append(calc_row)
    
    count_row += 1

print('Creating DataFrame')
out_data = pd.DataFrame(rows)

# Generate random magnitudes based on actual normal distribution of magnitudes
out_data = out_data.assign(Mag=np.random.normal(6.07462, 1.0362, out_data.shape[0]))

out_data.to_csv('data/merge-noaa_not_earthquake.csv')
