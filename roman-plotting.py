# -*- coding: utf-8 -*-

# Plot scatter matrix with specified columns
# pd.plotting.scatter_matrix(out_data[['mw', 'PFS-MEAN', 'PFS-MAX', 'PFS-DELTA', 'PFS-SD']], diagonal='kde')

import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd
import importlib

def reset_plots():
    sns.reset_orig()
    importlib.reload(mpl); importlib.reload(plt); importlib.reload(sns)

merge_data = pd.read_csv('data/roman-merge.csv')

#corr = merge_data.corr()
#sns.heatmap(corr, cmap="seismic", vmax=1.0, vmin=-1.0, annot=True)

data = merge_data[['mw', 'PFS-MEAN', 'PFS-MAX', 'PFS-DELTA', 'PFS-SD']]

'''
g = sns.PairGrid(data)
g.map_upper(sns.histplot)
g.map_lower(sns.kdeplot, fill=True)
g.map_diag(sns.histplot, kde=True)
'''

# Lists of variables and properties we want
event_vals = ['mw', 'depth', 'lat', 'lon']
calc_vals = ['magAFV', 'sB', 'PT', 'PD', 'PFS', 'FP', 'EF', 'Kp', 'DST']
calc_props = ['MEAN', 'MAX', 'DELTA', 'SD']

for event_val in event_vals:
    # For each magnitude, depth, latitude, and longitude
    for calc_prop in calc_props:
        # For each MEAN, MAX, DELTA, SD: do scatter plot and correlation matrix
        print("For '{}' plotting '{}'".format(event_val, calc_prop))
        
        # Start with the event property we want
        varnames = [event_val]
        
        for val in calc_vals:
            varname = val + '-' + calc_prop
            varnames.append(varname)
            
        data_slice = merge_data[varnames]
        
        # Correlation matrix
        corr = data_slice.corr()
        sns.heatmap(corr, cmap="seismic", vmax=1.0, vmin=-1.0, annot=True)
        
        # Save plot
        plt.savefig('plots/corr-{}-{}.png'.format(event_val, calc_prop))
        
        # Reset plots
        reset_plots()
        
        #matplotlib.rc_file_defaults()
        
        # Scatter plot
        '''
        g = sns.PairGrid(data_slice)
        g.map_upper(sns.histplot)
        g.map_lower(sns.kdeplot, fill=True)
        g.map_diag(sns.histplot, kde=True)
        '''
        
        # Seaborn KDE very slow for now
        pd.plotting.scatter_matrix(data_slice, alpha=0.5)
        
        # Save plot
        plt.savefig('plots/scatter-{}-{}.png'.format(event_val, calc_prop))
        
        # Reset plots
        reset_plots()
    