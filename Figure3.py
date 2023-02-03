#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:50:13 2023

@author: Alice Wells

Plotting script for Figure 3 in Wells et al., 2023

Daily perturbation of SO2 in Dobson Units (DU) derived from OMPS-NM lower 
stratospheric profile (blue), UKESM1 SO2only (red) SO2+ash (dark red). Data 
averaged across latitudes 30–90° N, weighted by the cosine of the corresponding 
latitude to ensure data is area weighted. We remove the long-term background SO2 
burden derived from OMPS-NM for the years 2013–2018 from those for 2019 to 
provide a stratospheric perturbation for the observations. Similarly, we remove 
the impacts of background stratospheric aerosol from the model simulations by 
subtracting the stratospheric sulfate burdens from the CNTL simulation from 
those for SO2only and SO2+ash.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import math
import copy
import matplotlib.pyplot as plt

# =============================================================================
# Load data
# =============================================================================
    
#Observations
omps = np.load('omps_perturbation_daily_latlong_so2_1x1deg.npy')
#Model SO2+ash 
so2_ash = np.load('SO2_ash_perturbation_daily_area_average_so2.npy')
#Model SO2onlu
so2_only = np.load('SO2_only_perturbation_daily_area_average_so2.npy')
 
# =============================================================================
# Calculate area average
# =============================================================================

#Create zonal mean omps
omps_lon_averaged = np.nanmean(omps, axis = 1)

latitude = range(-90, 91)
#Latitude weighting
weighting = np.cos(np.deg2rad(latitude))
#Average over 30-90N using weighted average based on latitude
omps_area_average = np.ma.average(np.ma.masked_invalid(omps_lon_averaged[120:, :]), axis = 0, weights = weighting[120:])
 
#Create array of days since eruption 
days = np.arange(-20, 102, 1)

# =============================================================================
# Calculate e-folding times
# =============================================================================

def find_nearest(array, value):
    
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    
    return idx

def e_folding_time(data):
    
    #create copy of data (start from eruption day, 20) and set nan to zero
    data_copy = copy.copy(data[20:])
    data_copy[np.isnan(data_copy)] = 0.0 
    
    #Find the x index of the maxmimum point 
    x_max = find_nearest(data_copy, np.nanmax(data_copy))
    #Find the x index of the max point / e
    x_e = x_max + find_nearest(data_copy[x_max:], (np.nanmax(data_copy) / math.e))

    e_time = x_e - x_max
    
    return e_time

#OMPS
omps_e_time = e_folding_time(omps_area_average)

#Model SO2+ash
so2_ash_e_time = e_folding_time(so2_ash)

#Model SO2only
so2_only_e_time = e_folding_time(so2_only)
# =============================================================================
# Plotting
# =============================================================================
    
params = {'legend.fontsize': 25,
          'axes.labelsize': 30,
          'axes.titlesize':35,
          'axes.linewidth':3,
          'axes.grid': True,
          'xtick.labelsize':30,
          'ytick.labelsize':30,
          'xtick.major.size': 8,
          'xtick.minor.size': 5,
          'xtick.minor.visible':True,
          'ytick.major.size':8,
          'ytick.minor.size':5,
          'ytick.minor.visible':True,
          'lines.linewidth': 6}

plt.rcParams.update(params)

fig, ax = plt.subplots(figsize=(20, 12))

#Plot area averaged column SO2 over time
ax.plot(days, omps_area_average, 'tab:blue', label = 'OMPS-NM, e folding time = ' + str(omps_e_time))
ax.plot(days, so2_only, 'red', label = 'UKESM1 SO2only, e folding time = ' + str(so2_only_e_time))
ax.plot(days, so2_ash, 'darkred', label = 'UKESM1 SO2+ash, e folding time = ' + str(so2_ash_e_time))

ax.grid(which = 'minor', axis = 'y', alpha = 0.2)
ax.grid(which = 'minor', axis = 'x', alpha = 0.2)

plt.xlabel('Day since eruption')
plt.ylabel('SO2 (Dobson Units)')
plt.legend()

plt.tight_layout()
plt.savefig('Figure3.png', dpi = 300)
plt.show()
