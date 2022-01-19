#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:40:42 2021

@author: roman

"""

import pandas as pd
import numpy as np
from datetime import datetime

#omni2_info = pd.read_table('data/omni2_info.tsv', float_precision='high')

# Proton flux flag rounding up so not replaced to np.nan, still not fixed
omni2_info = pd.read_csv('data/omni2_info.tsv', sep='\t', float_precision='high')

columns = {
    "Yr": 1,  # 1, Year
    "DD": 2,  # 2, Decimal Day
    "Hr": 3,  # 3, Hour
    "BRN": 4,  # 4, Bartels rotation number
    "IDIMF": 5,  # 5, ID for IMF spacecraft
    "IDSW": 6,  # 6, ID for SW plasma spacecraft
    "#IMF": 7,  # 7, # of points in the IMF averages
    "#PA": 8,  # 8, # of points in the plasma averages
    "FMA": 9,  # 9, Field Magnitude Average |B|
    "magAFV": 10,  # 10, Magnitude of Average Field Vector --
    "latAFV": 11,  # 11, Lat.Angle of Aver. Field Vector
    "longAFV": 12,  # 12, Long.Angle of Aver. Field Vector
    "BxGSE": 13,  # 13, Bx GSE, GSM
    "ByGSE": 14,  # 14, By GSE
    "BzGSE": 15,  #15, Bz GSE
    "ByGSM": 16,  # 16, By GSM
    "BzGSM": 17,  # 17, Bz GSM
    "sMagB": 18,  # 18, sigma |B|
    "sB": 19,  # 19, sigma B  --
    "sBx": 20,  # 20, sigma Bx
    "sBy": 21,  # 21, sigma By"
    "sBz": 22,  # 22, sigma Bz
    "PT": 23,  # 23, Proton temperature  --
    "PD": 24,   # 24, Proton density  --
    "PFS": 25,  # 25, Plasma (Flow) speed  --
    "longPFA": 26,  # 26, Plasma Flow Long. Angle
    "latPFA": 27,  # 27, Plasma Flow Lat. Angle
    "NaNp": 28,  # 28, Na/Np
    "sT": 29,  # 29, sigma T
    "sN": 30,  # 30, sigma N
    "sV": 31,  # 31, sigma V
    "sPV": 32,  # 32, sigma phi V
    "sTV": 33,  # 33, sigma theta V
    "sNaNp": 34,  # 34, sigma-Na/Np
    "FP": 35,  # 35, Flow Pressure  --
    "EF": 36,  # 36, Electric field  --
    "PB": 37,  # 37, Plasma beta
    "AMN": 38,  # 38, Alfven mach number
    "MMN": 39,  # 39, Magnetosonic mach number
    "QI": 40,  # 40, Proton Quasy-Invariant
    "Kp": 41,   # 41, Planetary geomagnetic activity index (Kp)  --
    "R": 42,   # 42, Sunspot number (R)
    "DST": 43,  # 43, DST Index  --
    "ap": 44,  # 44, ap-index
    "f10.7": 45,  # 45, f10.7_index
    "AE": 46,  # 46, AE-index
    "AL": 47,  # 47, AL-index, from Kyoto
    "AU": 48,  # 48, AU-index, from Kyoto
    "PCN": 49,  # 49, PC(N) index
    "LyAlp": 50,  # 50, Solar Lyman-alpha intensity
    "PF1": 51,  # 51, Proton flux >1 MeV
    "PF2": 52,  # 52, Proton flux >2 MeV
    "PF4": 53,  # 53, Proton flux >4 MeV
    "PF10": 54,  # 54, Proton flux >10 MeV
    "PF30": 55,  # 55, Proton flux >30 MeV
    "PF60": 56,  # 56, Proton flux >60 MeV
    "F": 57,  # 57, Flag(***)  
}

#Work-around for a bug where names parameter(line 77) does not accept columns.keys() as a valid input
colnames = []
for pair in columns:
    colnames.append(pair)

#Date-time format as input for date_parser parameter
custom_date_parser = lambda x: datetime.strptime(x, "%Y %j %H")

omni2 = pd.read_table('data/omni2_all_years.dat', sep='\s+', names=colnames, dtype={"Yr": "object", "DD": "object", "Hr": "object"}, parse_dates={"Date": ["Yr", "DD", "Hr"]}, keep_date_col=True, dayfirst=True, date_parser=custom_date_parser)


columns["Date"] = 0
# Replace bad flags with np.nan
for column in omni2:
    # Get value to fill
    columnKey = columns[column]
    fillValue = omni2_info['FILL_VALUE'][columnKey]
    
   # print('Column name: {}, fill value: {}'.format(column, fillValue));
    
    # Now replace fillValue with nan
    omni2.loc[omni2[column] == fillValue,column] = np.nan
 
##Test Functions##

#print(omni2[2000:2003])
#omni2.head().plot(x="Date", y=['Kp', 'R'])
#omni2.to_csv("data/omni2_full.txt", sep='\t')
