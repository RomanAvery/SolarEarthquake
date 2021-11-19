#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 19 13:31:59 2021

@author: roman
"""

import pandas as pd
from load_omni2_data import omni2

hours_before = 24

"""
For each earthquake event date and each desired variable:
- calculate MEAN, MAX, MAX - MIN, STANDARD DEV within period of hours_before 
- merge into new dataframe with event timestamp, lat, long, depth, and magnitude
""


earthquake_data = pd.read_csv('data/isc-gem-cat.csv')