#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov  8 12:45:49 2021

@author: roman
"""

WORD  FORMAT  Fill Value         MEANING                  UNITS/COMMENTS
                               
 1      I4              Year                              1963, 1964, etc.
 2      I4              Decimal Day                       January 1 = Day 1
 3      I3              Hour                              0, 1,...,23   
 4      I5   9999      Bartels rotation number
 5      I3    99        ID for IMF spacecraft             See table
 6      I3    99        ID for SW plasma spacecraft       See table
 7      I4   999       # of points in the IMF averages 
 8      I4   999       # of points in the plasma averages 
 9     F6.1  999.9     Field Magnitude Average |B|       1/N SUM |B|, nT
10     F6.1  999.9     Magnitude of Average Field Vector sqrt(Bx^2+By^2+Bz^2) 
11     F6.1  999.9     Lat.Angle of Aver. Field Vector   Degrees (GSE coords) 
12     F6.1  999.9     Long.Angle of Aver.Field Vector   Degrees (GSE coords) 
13     F6.1  999.9     Bx GSE, GSM                       nT 
14     F6.1  999.9     By GSE                            nT 
15     F6.1  999.9     Bz GSE                            nT 
16     F6.1  999.9     By GSM                            nT
17     F6 1  999.9     Bz GSM                            nT
18     F6.1  999.9     sigma|B|            RMS Standard Deviation in average                                           magnitude (word 10), nT
19     F6.1  999.9     sigma B             RMS Standard Deviation in field
                                            vector, nT (**)
20     F6.1  999.9     sigma Bx            RMS Standard Deviation in GSE 
                                            X-component average, nT 
21     F6.1  999.9     sigma By            RMS Standard Deviation in GSE
                                            Y-component average, nT 
22     F6.1  999.9     sigma Bz            RMS Standard Deviation in GSE 
                                             Z-component average, nT 

23     F9.0  9999999.  Proton temperature                Degrees, K
24     F6.1  999.9     Proton Density                    N/cm^3 

25     F6.0  9999.     Plasma (Flow) speed               km/s
26     F6.1  999.9     Plasma Flow Long. Angle    Degrees, quasi-GSE*
27     F6.1  999.9     Plasma  Flow Lat. Angle     Degrees, GSE* 

28     F6.3  9.999     Na/Np                    Alpha/Proton ratio 
29     F6.2  99.99     Flow Pressure            P (nPa) = (1.67/10**6) * Np*V**2 * (1+ 4*Na/Np)
                                                for hours with non-fill Na/Np ratios and
                                                P (nPa) = (2.0/10**6) * Np*V**2
                                                for hours with fill values for Na/Np

30     F9.0  9999999.  sigma T                           Degrees, K
31     F6.1  999.9     sigma N                           N/cm^3
32     F6.0  9999.     sigma V                           km/s
33     F6.1  999.9     sigma phi V                       Degrees
34     F6.1  999.9     sigma theta V                     Degrees
35     F6.3  9.999     sigma-Na/Np   

36     F7.2  999.99    Electric field         -[V(km/s) * Bz (nT; GSM)] * 10**-3. (mV/m)
37     F7.2  999.99    Plasma beta            Beta = [(T*4.16/10**5) + 5.34] * Np / B**2
38     F6.1  999.9     Alfven mach number      Ma = (V * Np**0.5) / 20 * B



39     I3    99        Kp               Planetary Geomagnetic Activity Index
                                       (e.g. 3+ = 33, 6- = 57, 4 = 40, etc.)

40      I4   999        R                          Sunspot number (new version 2)
41      I6   99999     DST Index                    nT, from Kyoto 
42      I5   9999      AE-index                    nT, from Kyoto
43     F10.2 999999.99 Proton flux                 number/cmsq sec sr >1 Mev 
44     F9.2  99999.99  Proton flux                 number/cmsq sec sr >2 Mev
45     F9.2  99999.99  Proton flux                 number/cmsq sec sr >4 Mev
46     F9.2  99999.99  Proton flux                 number/cmsq sec sr >10 Mev
47     F9.2  99999.99  Proton flux                 number/cmsq sec sr >30 Mev
48     F9.2  99999.99  Proton flux                 number/cmsq sec sr >60 Mev
49      I3   0         Flag(***)                       (-1,0,1,2,3,4,5,6)     
 
50       I4   999      ap-index                     nT
51       F6.1 999.9    f10.7_index                  ( sfu = 10-22W.m-2.Hz-1)
52       F6.1 999.9    PC(N) index
53       I6   99999    AL-index, from Kyoto         nT                  
54       I6   99999    AU-index, from Kyoto         nT
55       F5.1  99.9   Magnetosonic mach number= = V/Magnetosonic_speed
                     Magnetosonic speed = [(sound speed)**2 + (Alfv speed)**2]**0.5
                     The Alfven speed = 20. * B / N**0.5 
                     The sound speed = 0.12 * [T + 1.28*10**5]**0.5 