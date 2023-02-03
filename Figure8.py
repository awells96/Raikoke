#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 15:10:34 2023

@author: Alice Wells

Plotting script for Figure 8 in Wells et al., 2023

Daily evolution of Ångström Exponent for OMPS-LP (blue), UKESM1 SO2only (red) 
and UKESM1 SO2+ash (dark red). Calculated using area weighted sAOD between 
30–90° N (same as Fig. 7) using 510nm and 869nm wavelengths.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# Load data
# =============================================================================

#Model data for SO2 + ash
so2_ash_550 = np.load('SO2_ash_perturbation_daily_zonal_average_aod_510nm_1x1deg.npy')
so2_ash_865 = np.load('SO2_ash_perturbation_daily_zonal_average_aod_865nm_1x1deg.npy')

#Model data for SO2 only
so2_only_550 = np.load('SO2_only_perturbation_daily_zonal_average_aod_510nm_1x1deg.npy')
so2_only_865 = np.load('SO2_only_perturbation_daily_zonal_average_aod_865nm_1x1deg.npy')
    
#Original omps data 510nm and 869nm
omps_510 = np.load('omps_perturbation_daily_zonal_average_aod_510nm.npy')
omps_869 = np.load('omps_perturbation_daily_zonal_average_aod_869nm.npy')

# =============================================================================
# Create the omps model mask
# =============================================================================

#Find model points only where omps data exists
mask510 = np.ones( (181, 366) )
mask510[np.isnan(omps_510)] = np.nan

mask869 = np.ones( (181, 366) )
mask869[np.isnan(omps_869)] = np.nan

#Mask the model data
so2_ash_550_masked = so2_ash_550*mask510
so2_ash_865_masked = so2_ash_865*mask869

so2_only_550_masked = so2_only_550*mask510
so2_only_865_masked = so2_only_865*mask510

# ============================================================================
# Calculate area averages
# =============================================================================
    
latitude = range(-90, 91)
#Latitude weighting
weighting = np.cos(np.deg2rad(latitude))
   
#Average over 30-90N using weighted averages based on latitude 
so2_ash_550_mean = np.ma.average(np.ma.masked_invalid(so2_ash_550_masked[120:, :]), axis = 0, weights = weighting[120:])
so2_ash_865_mean = np.ma.average(np.ma.masked_invalid(so2_ash_865_masked[120:, :]), axis = 0, weights = weighting[120:])

so2_only_550_mean = np.ma.average(np.ma.masked_invalid(so2_only_550_masked[120:, :]), axis = 0, weights = weighting[120:])
so2_only_865_mean = np.ma.average(np.ma.masked_invalid(so2_only_865_masked[120:, :]), axis = 0, weights = weighting[120:])

omps_510_mean = np.ma.average(np.ma.masked_invalid(omps_510[120:, :]), axis = 0, weights = weighting[120:])
omps_869_mean = np.ma.average(np.ma.masked_invalid(omps_869[120:, :]), axis = 0, weights = weighting[120:])

#Create array of days since eruption
days = np.arange(0, 346, 1)

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
          'lines.linewidth': 4}

plt.rcParams.update(params)

fig, ax = plt.subplots(figsize=(20, 12))

#Calculate the Angstrom exponent -log(aod_1/aod_2)/log(wavelength_1/wavelength_2)
AE_so2_ash = - (np.log(so2_ash_550_mean/so2_ash_865_mean))/(np.log(510/865))
AE_so2_only = - (np.log(so2_only_550_mean/so2_only_865_mean))/(np.log(510/865))
AE_omps = - (np.log(omps_510_mean/omps_869_mean))/(np.log(510/869))

#Find average AE
AE_so2_ash_mean = np.nanmean(AE_so2_ash)
AE_so2_only_mean = np.nanmean(AE_so2_only)
AE_omps_mean = np.nanmean(AE_omps)

#Plotting AE over time and average AE
ax.plot(days, AE_so2_only[20:], 'red', label = 'UKESM1 SO2only')
ax.axhline(AE_so2_only_mean, linestyle = '--', color = 'red', label = 'UKESM1 SO2only average ' + str(np.round(AE_so2_only_mean, 2)))

ax.plot(days, AE_so2_ash[20:], 'darkred', label = 'UKESM1 SO2+ash')
ax.axhline(AE_so2_ash_mean, linestyle = '--', color = 'darkred', label = 'UKESM1 SO2+ash average ' + str(np.round(AE_so2_ash_mean, 2)))

ax.plot(days[5:], AE_omps[25:], 'tab:blue', label = 'OMPS-LP')
ax.axhline(AE_omps_mean, linestyle = '--', color = 'tab:blue', label = 'OMPS-LP average ' + str(np.round(AE_omps_mean, 2)))

plt.legend()
plt.ylabel('Angstrom Exponent')
plt.xlabel('Days since eruption')
plt.ylim([-1.2, 3.2])

plt.tight_layout()
plt.savefig('Figure8.png', dpi = 300)
plt.show()
