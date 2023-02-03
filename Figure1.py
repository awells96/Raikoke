#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 14 12:34:51 2022

@author: Alice Wells

Plotting script for Figure 1 in Wells et al., 2023

Geographic evolution of column integrated SO2 plume in Dobson Units (DU) 
derived from OMPS-NM lower stratospheric profile (centre) UKESM1 SO2only (left) 
and SO2+ash (right) for the period 22–30th June 2019. We remove the long-term 
background SO2 burden derived from OMPS-NM for the years 2013–2018 from those 
for 2019 to provide a stratospheric perturbation for the observations. 
Similarly, we remove the impacts of background stratospheric aerosol from the
model simulations by subtracting the stratospheric sulfate burdens from the 
CNTL simulation from those for SO2only and SO2+ash. The OMPS-LP background and 
CNTL SO2 burden are shown in Fig. S1.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import copy
import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import matplotlib.colors as colors
import cartopy.crs as ccrs

# =============================================================================
# Load data
# =============================================================================

#Observations
omps = np.load('omps_perturbation_daily_latlong_so2_1x1deg.npy') 
#Model SO2+ash
so2_ash = np.load('SO2_ash_perturbation_daily_latlong_so2_1x1deg.npy')
#Model SO2only
so2_only = np.load('SO2_only_perturbation_daily_latlong_so2_1x1deg.npy')

#Create a list of MMDD for dating figures
day_list = ['0621', '0622', '0623', '0624', '0625', '0626', '0627', '0628', '0629', '0630', '0701']

# =============================================================================
# Plotting
# =============================================================================

#Define latitude and longitude coordinates
latitude = np.arange(-90, 91)
model_longitude = np.arange(-180, 181)
obs_longitude = np.arange(0, 361)

params = {'legend.fontsize': 25,
          'axes.labelsize': 30,
          'axes.titlesize':40,
          'axes.linewidth':3,
          'axes.grid': True,
          'xtick.labelsize':30,
          'ytick.labelsize':20,
          'xtick.major.size': 8,
          'xtick.minor.size': 5,
          'xtick.minor.visible':True,
          'ytick.major.size':8,
          'ytick.minor.size':5,
          'ytick.minor.visible':False,
          'lines.linewidth': 1.5}

plt.rcParams.update(params)

fig = plt.figure(figsize = (40,21), facecolor = 'w', edgecolor = 'k')

col_map = copy.copy(mpl_cm.get_cmap('plasma'))
titanium_white = (1.0, 1.0, 1.0)
lvs_so2 = [0.03, 0.06, 0.09, 0.3, 0.6, 0.9, 3, 6, 9, 30, 60]
norm = colors.BoundaryNorm(lvs_so2, col_map.N)

ind = 1

for i in np.arange(21, 30, 2):
    
    #Centre map on Raikoke
    #SO2only
    ax = plt.subplot(6, 3, ind, projection=ccrs.PlateCarree(central_longitude = 180))
    plt.contourf(model_longitude, latitude, so2_only[:, :, i], levels = lvs_so2, cmap = col_map, norm = norm, extend = 'both')
    
    if day_list[i - 20][1] == '6':
        plt.title('UKESM1 SO2only: ' + day_list[i - 20][2:] + ' June 2019')
    else: 
        plt.title('UKESM1 SO2only: ' + day_list[i - 20][2:] + ' July 2019')
        
    ax.coastlines()
    ax.set_ylim( [30, 90] )
    ax.set_xlim( [-180, 180] ) 
    ax.set_yticks([45, 60, 75])
    
    #OMPS observations
    ax = plt.subplot(6, 3, ind + 1, projection=ccrs.PlateCarree(central_longitude = 180))
    plt.contourf(obs_longitude, latitude, omps[:, :, i], levels = lvs_so2, cmap = col_map, norm = norm, extend = 'both')
    
    if day_list[i - 20][1] == '6':
        plt.title('OMPS-NM: ' + day_list[i - 20][2:] + ' June 2019')
    else: 
        plt.title('OMPS-NM: ' + day_list[i - 20][2:] + ' July 2019')
        
    ax.coastlines()
    ax.set_ylim( [30, 90] )
    ax.set_xlim( [-180, 180] )
    ax.set_yticks([45, 60, 75])
    
    #SO2+ash
    ax = plt.subplot(6, 3, ind + 2, projection=ccrs.PlateCarree(central_longitude = 180))
    plt.contourf(model_longitude, latitude, so2_ash[:, :, i], levels = lvs_so2, cmap = col_map, norm = norm, extend = 'both')
    
    if day_list[i - 20][1] == '6':
        plt.title('UKESM1 SO2+ash: ' + day_list[i - 20][2:] + ' June 2019')
    else: 
        plt.title('UKESM1 SO2+ash: ' + day_list[i - 20][2:] + ' July 2019')
        
    ax.coastlines()
    ax.set_ylim( [30, 90] )
    ax.set_xlim( [-180, 180] ) 
    ax.set_yticks([45, 60, 75])
    
    ind = ind + 3
    
cax = plt.axes([0.12, 0.1, 0.78, 0.040])             # Left, Bottom, Width, Height
bar = plt.colorbar(cax=cax, orientation='horizontal')
bar.set_ticks(lvs_so2)
bar.set_ticklabels(lvs_so2)  

bar.set_label('Dobson Units', fontsize = 40)
bar.ax.tick_params(labelsize = 40)
    
plt.tight_layout()
plt.savefig('Figure1.png', dpi = 300)
plt.show() 
