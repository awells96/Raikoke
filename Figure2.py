#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:41:48 2023

@author: Alice Wells

Plotting script for Figure 2 in Wells et al., 2023

Contingency analysis of SO2 plume between OMPS-NM lower stratospheric profile 
and UKESM1 SO2only for the period 22nd June–1st July 2019. “Correct Negative” 
occurs at the point where both the model and observation are below 0.3 DU. 
“Hits” occur at the point where the modelled column SO2 burden is within a 
factor of two of the observations at that point to allow for timing errors. 
“Obs > Model” and “Model > Obs” occur when the modelled column SO2 burden is 
above or below the factor of two limit.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import matplotlib.colors as colors
from matplotlib.colors import ListedColormap
import cartopy.crs as ccrs

# =============================================================================
# Load data
# =============================================================================

#Contingency table data for SO2only
contingency_so2_only = np.load('SO2_only_perturbation_daily_latlong_so2_contingency_1x1deg.npy')

#Create a list of MMDD for dating figure
day_list = ['0621', '0622', '0623', '0624', '0625', '0626', '0627', '0628', 
            '0629', '0630', '0701', '0702', '0703', '0704', '0708', '0709', 
            '0710', '0711', '0712', '0713', '0714']

# =============================================================================
# Plotting
# =============================================================================

#Definte latitude and longitude coordinates
latitude = np.arange(-90, 91)
longitude = np.arange(-180, 181)

params = {'legend.fontsize': 25,
          'axes.labelsize': 30,
          'axes.titlesize':30,
          'axes.linewidth':3,
          'axes.grid': True,
          'xtick.labelsize':20,
          'ytick.labelsize':20,
          'xtick.major.size': 8,
          'xtick.minor.size': 0,
          'xtick.minor.visible':False,
          'ytick.major.size':8,
          'ytick.minor.size':5,
          'ytick.minor.visible':False,
          'lines.linewidth': 1.5}

plt.rcParams.update(params)

fig = plt.figure(figsize = (30,15), facecolor = 'w', edgecolor = 'k')

cmap = mpl_cm.get_cmap('plasma', 4) 
white = (1.0, 1.0, 1.0, 1.0)
new_colors = cmap(np.linspace(0, 1, 4))
new_colors[0, :] = white
new_cmap = ListedColormap(new_colors)

lvs_ct = [0.5, 1.5, 2.5, 3.5, 4.5]
norm_ct = colors.BoundaryNorm(lvs_ct, new_cmap.N)

ind = 1

for i in np.arange(21, 31, 1):
    
    #Centre map on Raikoke
    ax = plt.subplot(5, 2, ind, projection=ccrs.PlateCarree(central_longitude = 180))
    plt.pcolormesh(longitude, latitude, contingency_so2_only[:, :, i - 21], cmap = new_cmap, norm = norm_ct, vmin = 1, vmax = 4)
    
    if day_list[i - 20][1] == '6':
        plt.title(day_list[i - 20][2:] + ' June 2019 - SO2only')
    else: 
        plt.title(day_list[i - 20][2:] + ' July 2019 - SO2only')
        
    ax.coastlines()
    ax.set_ylim( [30, 90] )
    ax.set_xlim( [-180, 180] ) 
    ax.set_yticks([45, 60, 75])
    
    ind = ind + 1
    
cax = plt.axes([0.12, 0.06, 0.78, 0.040])             # Left, Bottom, Width, Height
bar = plt.colorbar(cax=cax, orientation='horizontal')
bar.set_ticks([1, 2, 3, 4])
bar.set_ticklabels(['Correct Negative', 'Obs > Model', 'Model > Obs', 'Hits'])  
    
plt.tight_layout()
plt.savefig('Figure2.png', dpi = 300)
plt.show() 
