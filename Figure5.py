#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:14:26 2023

@author: Alice Wells

Plotting script for Figure 5 in Wells et al., 2023

Daily perturbation in the sAOD averaged over 30–90° N as observed by OMPS-LP 
scaled from 510nm to 532nm (light blue) and CALIOP at 532nm (dark blue). 
The orange dashed line represents the combined OMPS-LP and CALIOP dataset at 
532nm. We remove the long-term background sAOD derived from OMPS-LP (0.0041) 
and CALIOP (0.0003) for the years 2013–2018 from those for 2019 to provide a 
stratospheric perturbation for the observations.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Load data
# =============================================================================

#OMPS sAOD
omps = np.load('omps_perturbation_daily_zonal_average_aod_532nm.npy')
#CALIOP sAOD
caliop = np.load('caliop_perturbation_daily_zonal_average_aod_532nm.npy')
#Combined sAOD dataset averaged over 30-90N
combo_area_average = np.load('combined_dataset_area_average_aod_532nm.npy')

# =============================================================================
# Area average observed data sets across 30-90N
# =============================================================================

latitude = range(-90, 91)
#Latitude weighting
weighting = np.cos(np.deg2rad(latitude))

#Average over 30-90N using weighted averages based on latitudes=
caliop_mean = np.ma.average(np.ma.masked_invalid(caliop[120:, :]), axis = 0, weights = weighting[120:])
caliop_area_average = caliop_mean.filled(fill_value=np.nan)
omps_area_average = np.ma.average(np.ma.masked_invalid(omps[120:, :]), axis = 0, weights = weighting[120:])
    
#Create array of days since eruption    
days = np.arange(-20, 346, 1)

# =============================================================================
# Plotting
# =============================================================================
    
params = {'legend.fontsize': 25,
          'axes.labelsize': 30,
          'axes.titlesize':35,
          'axes.linewidth':3,
          'axes.grid': True,
          'xtick.labelsize':25,
          'ytick.labelsize':25,
          'xtick.major.size': 8,
          'xtick.minor.size': 5,
          'xtick.minor.visible':True,
          'ytick.major.size':8,
          'ytick.minor.size':5,
          'ytick.minor.visible':True,
          'lines.linewidth': 5}

plt.rcParams.update(params)

fig, ax = plt.subplots(figsize=(20, 12))

ax.plot(days, omps_area_average, 'cornflowerblue', alpha = 1, label = 'OMPS-LP 532nm scaled')
ax.plot(days, caliop_area_average, 'darkblue', alpha = 0.8, label = 'CALIOP 532nm')
ax.plot(days, combo_area_average, 'tab:orange', linestyle = (0, (3, 3)), linewidth = 5, label = 'OMPS and CALIOP combination')

ax.grid(which = 'minor', axis = 'y', alpha = 0.2)
ax.grid(which = 'minor', axis = 'x', alpha = 0.2)

plt.xlabel('Day since eruption')
plt.ylabel('sAOD')
plt.legend()

plt.savefig('Figure5.png', dpi = 300)
plt.show()