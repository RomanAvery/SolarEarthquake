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

# Load NOAA volcano data
volcano_data = pd.read_csv('data/volcano-events-2022-01-19_12-16-42_+1300.tsv', sep='\t', header=0)

# Rename date columns so we can get a datetime
volcano_data.rename(columns = {'Year':'year', 'Mo':'month', 'Dy':'day'}, inplace = True)

# Create datetime objects
volcano_data['date'] = pd.to_datetime(volcano_data[['year','month','day']])

"""
For each volcano event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, elevation, and type
"""


# Lists of variables and properties we want
event_vals = ['date', 'Latitude', 'Longitude', 'Elevation (m)', 'Type']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

out_data = create_merged_df(omni2, volcano_data, event_vals, calc_vals, calc_props, hours_before)

out_data.to_csv('data/merge-noaa_volcano.csv')
