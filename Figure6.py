#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:28:30 2023

@author: Alice Wells

Plotting script for Figure 6 in Wells et al., 2023

Monthly geographic evolution of the Northern Hemisphere sAOD from July 2019 to 
December 2019 derived from OMPS-LP Retrieved Aerosol Extinction (left) and 
CALIOP Aerosol Extinction Profile (right). We remove the long-term background 
sAOD derived from OMPS-LP and CALIOP for the years 2013–2018 from those for 
2019 to provide a stratospheric perturbation for the observations.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import copy
import calendar

import matplotlib.pyplot as plt
import matplotlib.cm as mpl_cm
import matplotlib.colors as colors
import cartopy.crs as ccrs

# =============================================================================
# Load data
# =============================================================================

#CALIOP sAOD
caliop = np.load('calipso_perturbation_monthly_latlong_aod_532nm.npy')
#OMPS sAOD
omps = np.load('omps_perturbation_monthly_latlong_aod_532nm.npy') 

# =============================================================================
# Plotting
# =============================================================================

#Create month list for plotting dates
month_list = np.arange(7, 13)

#Definte latitude and longitude coordinates
latitude = range(-90, 91)
longitude = range(-180, 181, 4)

params = {'legend.fontsize': 25,
          'axes.labelsize': 30,
          'axes.titlesize':20,
          'axes.linewidth':3,
          'axes.grid': False,
          'xtick.labelsize':20,
          'ytick.labelsize':20,
          'xtick.major.size': 8,
          'xtick.minor.size': 5,
          'xtick.minor.visible':True,
          'ytick.major.size':8,
          'ytick.minor.size':5,
          'ytick.minor.visible':False,
          'lines.linewidth': 1.5}

plt.rcParams.update(params)

fig = plt.figure(figsize = (20,20), facecolor = 'w', edgecolor = 'k')
 
col_map = copy.copy(mpl_cm.get_cmap('plasma'))
lvs = np.logspace(-2.3, -1, 12)
norm = colors.BoundaryNorm(lvs, col_map.N)

ind = 1

for i in range(6):
    
    #Centre map on Raikoke
    #OMPS
    ax = plt.subplot(7, 2, ind, projection=ccrs.PlateCarree(central_longitude = 180))
    cs = plt.contourf(longitude, latitude, omps[:, :, i+1], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
    plt.title('OMPS-LP scaled to 532nm : ' + calendar.month_name[month_list[i]] + ' 2019')
        
    ax.coastlines()
    ax.set_ylim( [0, 90] )
    ax.set_xlim( [-180, 180] )
    ax.set_yticks([15, 30, 45, 60, 75])
    
    #Plot marker on MLO
    if i == 0:
        plt.plot(24.5, 19.5, 'x', color = 'r', markersize = 15, markeredgewidth = 4)
    
    #CALIOP
    ax = plt.subplot(7, 2, ind + 1, projection=ccrs.PlateCarree(central_longitude = 180))
    cs = plt.contourf(longitude, latitude, caliop[:, :, i+1], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
    plt.title('CALIOP 532nm : ' + calendar.month_name[month_list[i]] + ' 2019')
        
    ax.coastlines()
    ax.set_ylim( [0, 90] )
    ax.set_xlim( [-180, 180] )
    ax.set_yticks([15, 30, 45, 60, 75])
    
    ind = ind + 2
    
cax = plt.axes([0.12, 0.1, 0.78, 0.040])             # Left, Bottom, Width, Height
bar = plt.colorbar(cax=cax, orientation='horizontal')
bar.set_ticks(np.logspace(-2.3, -1, 6))
bar.set_ticklabels(np.round(np.logspace(-2.3, -1, 6), 3))  
bar.set_label('Aerosol Optical Depth 550nm')
bar.ax.tick_params(labelsize = 30)
    
plt.tight_layout()
plt.savefig('Figure6.png', dpi = 300)
plt.show()   