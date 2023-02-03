#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:44:47 2023

@author: Alice Wells

Plotting script for Figure 7 in Wells et al., 2023

Daily perturbation of sAOD at 532nm averaged over 30–90° N. Daily OMPS-LP and 
CALIOP combined dataset sAOD (blue), UKESM1 SO2only with observational limits 
applied (red) and without limits applied (red dashed) and UKESM1 SO2+ash with 
observational limits applied (dark red) and without limits applied (dark red 
dashed). We remove the long-term background sAOD derived from OMPS-LP and 
CALIOP for the years 2013–2018 from those for 2019 to provide a stratospheric 
perturbation for the observations. Similarly, we remove the impacts of 
background stratospheric aerosol from the model simulations by subtracting the 
sAOD from the CNTL simulation from those for SO2only and SO2+ash.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Load data
# =============================================================================

#Model SO2+ash
so2_ash = np.load('SO2_ash_perturbation_daily_zonal_average_aod_532nm_1x1deg.npy')
#Model SO2only 
so2_only = np.load('SO2_only_perturbation_daily_zonal_average_aod_532nm_1x1deg.npy')
#Model SO2+ash with OMPS detection limits
so2_ash_omps = np.load('SO2_ash_perturbation_daily_zonal_average_aod_omps_limits_532nm_1x1deg.npy')
#Model SO2only with OMPS detection limits
so2_only_omps = np.load('SO2_only_perturbation_daily_zonal_average_aod_omps_limits_532nm_1x1deg.npy')
#Model SO2+ash with CALIOP detection limits
so2_ash_caliop = np.load('SO2_ash_perturbation_daily_zonal_average_aod_caliop_limits_532nm_1x1deg.npy')
#Model SO2only with CALIOP detection limits
so2_only_caliop = np.load('SO2_only_perturbation_daily_zonal_average_aod_caliop_limits_532nm_1x1deg.npy')

#CALIOP observations
caliop = np.load('caliop_perturbation_daily_zonal_average_aod_532nm.npy')
#OMPS observations
omps = np.load('omps_perturbation_daily_zonal_average_aod_532nm.npy')
#Combined sAOD dataset averaged over 30-90N
combo_area_average = np.load('combined_dataset_area_average_aod_532nm.npy')

# =============================================================================
# Create the combined dataset mask
# =============================================================================

#Find model points only where calipso and omps data exists
calipso_mask = np.ones( (181, 147) )
calipso_mask[np.isnan(caliop[:, :147])] = np.nan
omps_mask = np.ones( (181, 219) )
omps_mask[np.isnan(omps[:, 147:])] = np.nan

#Mask the model data SO2+ash
so2_ash_masked = np.zeros( (181, 366) )
so2_ash_masked[:] = np.nan
so2_ash_masked[:, :147] = so2_ash_caliop[:, :147] * calipso_mask
so2_ash_masked[:, 147:] = so2_ash_omps[:, 147:] * omps_mask

#Mask the model data SO2only
so2_only_masked = np.zeros( (181, 366) )
so2_only_masked[:] = np.nan
so2_only_masked[:, :147] = so2_only_caliop[:, :147] * calipso_mask
so2_only_masked[:, 147:] = so2_only_omps[:, 147:] * omps_mask

# =============================================================================
# Calculate area averages
# =============================================================================
    
latitude = range(-90, 91)
#Latitude weighting
weighting = np.cos(np.deg2rad(latitude))

#Average over 30-90N using weighted averages based on latitude
#Models with masks
so2_ash_masked_mean = np.ma.average(np.ma.masked_invalid(so2_ash_masked[120:, :]), axis = 0, weights = weighting[120:])
so2_only_masked_mean = np.ma.average(np.ma.masked_invalid(so2_only_masked[120:, :]), axis = 0, weights = weighting[120:])
#Models without masks
so2_ash_mean = np.ma.average(np.ma.masked_invalid(so2_ash[120:, :]), axis = 0, weights = weighting[120:])
so2_only_mean = np.ma.average(np.ma.masked_invalid(so2_only[120:, :]), axis = 0, weights = weighting[120:])

# =============================================================================
# Plotting
# =============================================================================

#Create array of days since eruption
days = np.arange(-20, 346, 1)
    
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

plt.plot(days, so2_ash_mean, 'darkred', label = 'UKESM1 SO2+ash without limits')
plt.plot(days, so2_ash_masked_mean, 'darkred', alpha = 0.7, linestyle = '--', label = 'UKESM1 SO2+ash with limits')

plt.plot(days, so2_only_mean, 'red', label = 'UKESM1 SO2only without limits')
plt.plot(days, so2_only_masked_mean, 'red',alpha = 0.7,  linestyle = '--', label = 'UKESM1 SO2only with limits')

plt.plot(days, combo_area_average, 'tab:blue', alpha = 1, label = 'OMPS and CALIOP combination')

ax.grid(which = 'minor', axis = 'y', alpha = 0.2)
ax.grid(which = 'minor', axis = 'x', alpha = 0.2)

plt.xlabel('Day since eruption')
plt.ylabel('sAOD')
plt.legend()

plt.tight_layout()
plt.savefig('Figure7.png', dpi = 600)
plt.show()