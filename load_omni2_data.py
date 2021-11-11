#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 14:40:42 2021

@author: roman

"""

import pandas as pd
import numpy as np
from load_omni2_info import omni2_info

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
    "magAFV": 10,  # 10, Magnitude of Average Field Vector
    "latAFV": 11,  # 11, Lat.Angle of Aver. Field Vector
    "longAFV": 12,  # 12, Long.Angle of Aver. Field Vector
    "BxGSE": 13,  # 13, Bx GSE, GSM
    "ByGSE": 14,  # 14, By GSE
    "BzGSE": 15,  #15, Bz GSE
    "ByGSM": 16,  # 16, By GSM
    "BzGSM": 17,  # 17, Bz GSM
    "sMagB": 18,  # 18, sigma |B|
    "sB": 19,  # 19, sigma B
    "sBx": 20,  # 20, sigma Bx
    "sBy": 21,  # 21, sigma By"
    "sBz": 22,  # 22, sigma Bz
    "PT": 23,  # 23, Proton temperature
    "PD": 24,   # 24, Proton density
    "PFS": 25,  # 25, Plasma (Flow) speed
    "longPFA": 26,  # 26, Plasma Flow Long. Angle
    "latPFA": 27,  # 27, Plasma Flow Lat. Angle
    "NaNp": 28,  # 28, Na/Np
    "FP": 29,  # 29, Flow Pressure
    "sT": 30,  # 30, sigma T
    "sN": 31,  # 31, sigma N
    "sV": 32,  # 32, sigma V
    "sPV": 33,  # 33, sigma phi V
    "sTV": 34,  # 34, sigma theta V
    "sNaNp": 35,  # 35, sigma-Na/Np
    "EF": 36,  # 36, Electric field
    "PB": 37,  # 37, Plasma beta
    "AMN": 38,  # 38, Alfven mach number
    "Kp": 39,   # 39, Planetary geomagnetic activity index (Kp)
    "R": 40,   # 40, Sunspot number (R)
    "DST": 41,  # 41, DST Index
    "AE": 42,  # 42, AE-index
    "PF1": 43,  # 43, Proton flux >1 MeV
    "PF2": 44,  # 44, Proton flux >2 MeV
    "PF4": 45,  # 45, Proton flux >4 MeV
    "PF10": 46,  # 46, Proton flux >10 MeV
    "PF30": 47,  # 47, Proton flux >30 MeV
    "PF60": 48,  # 48, Proton flux >60 MeV
    "F": 49,  # 49, Flag(***)
    "ap": 50,  # 50, ap-index
    "f10.7": 51,  # 51, f10.7_index
    "PCN": 52,  # 52, PC(N) index
    "AL": 53,  # 53, AL-index, from Kyoto
    "AU": 54,  # 54, AU-index, from Kyoto
    "MMN": 55,  # 55, Magnetosonic mach number
}

omni2 = pd.read_table('data/omni2_all_years.dat.txt', sep='\s+', names=columns.keys())

# Replace bad flags with np.nan
for column in omni2:
    # Get value to fill
    columnKey = columns[column] - 1
    fillValue = omni2_info['FILL_VALUE'][columnKey]
    
    print('Column name: {}, fill value: {}'.format(column, fillValue));
    
    # Now replace fillValue with nan
    omni2.loc[omni2[column] == fillValue,column] = np.nan
    
#omni2.head().plot(x="Yr", y=['Kp', 'R'])
