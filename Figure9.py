#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:59:22 2023

@author: Alice Wells

Plotting script for Figure 9 in Wells et al., 2023

Aerosol extinction coefficient vertical profile averaged longitudinally and 
over 30–90° N. Averaged daily CALIOP aerosol extinction coefficient vertical 
profiles (night retrievals only, fainter lines) with monthly average (bold blue) 
and monthly average plus/minus standard deviation (solid dashed black lines). 
UKESM1 SO2+ash (solid bold red) and SO2 only (dashed bold red) simulations with 
imposed CALIOP minimum retrieval limits and mask. Average tropopause height is 
shown by the horizontal green line and the average tropopause height +/- one 
standard deviation for 2019 is also shown in green dotted lines. 

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import calendar

# =============================================================================
# Load data
# =============================================================================

#CALIOP observations
caliop = np.load('caliop_perturbation_daily_zonal_average_extinction_532nm.npy')
#CALIOP tropopause height    
caliop_tph = np.load('calipso_daily_zonal_average_tropopause_height.npy')
#Model SO2+ash with CALIOP limits imposed
so2_ash = np.load('SO2_ash_perturbation_monthly_zonal_average_extinction_caliop_limits_532nm_1x1deg.npy')
#Model SO2only with CALIOP limits imposed
so2_only = np.load('SO2_only_perturbation_monthly_zonal_average_extinction_caliop_limits_532nm_1x1deg.npy')
#Model altitude profile
model_alts = np.load('Model_altitude.npy')

# =============================================================================
# Create the caliop model mask
# =============================================================================

#Find model points only where calipso data exists
caliop_mask = np.nanmean(caliop, axis = (1,2))
mask = np.ones( (181, 12) )
mask[np.isnan(caliop_mask)] = np.nan

#Mask the model data
so2_ash_masked = np.zeros( (181, 85, 12) )
so2_only_masked = np.zeros( (181, 85, 12) )
for i in range(85):
    so2_ash_masked[:, i, :] = so2_ash[:, i, :] * mask
    so2_only_masked[:, i, :] = so2_only[:, i, :] * mask

# =============================================================================
# Calculate area average
# =============================================================================

latitude = range(-90, 91)
#Latitude weighting
weighting = np.cos(np.deg2rad(latitude))

#Average over 30-90N using weighted averaged based on latitude
caliop_area_average = np.ma.average(np.ma.masked_invalid(caliop[120:, :, :, :]), axis = 0, weights = weighting[120:])
so2_ash_area_average = np.ma.average(np.ma.masked_invalid(so2_ash_masked[120:, :, :]), axis = 0, weights = weighting[120:])
so2_only_area_average = np.ma.average(np.ma.masked_invalid(so2_only_masked[120:, :, :]), axis = 0, weights = weighting[120:])

caliop_monthly_mean = np.nanmean(caliop_area_average, axis = 1)
caliop_monthly_std = np.nanstd(caliop_area_average, axis = 1)

caliop_mean_tph = np.nanmean(caliop_tph[120:, :, :], axis = (0,1))
caliop_std_tph = np.nanstd(caliop_tph[120:, :, :], axis = (0,1))

# =============================================================================
# Define altitude profile for caliop data
# =============================================================================
    
alts1 = np.linspace(-500, 20200, 346)
alts2 = np.linspace(20380, 29740, 53)
caliop_alts = np.hstack( (alts1, alts2) )/1000

# =============================================================================
# Plotting
# =============================================================================

#Create months for plotting dates
months = calendar.month_name[6:13] + calendar.month_name[1:6]

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

fig = plt.figure(figsize = (27,20))

fig.text(0.5, 0.08, 'Aerosol extinction coefficient [$x10^{-2}$ km$^{-1}$]', ha = 'center', va = 'center', fontsize = 27, fontweight = 'bold')
fig.text(0.08, 0.5, 'Altitude [km]', ha = 'center', va = 'center', rotation = 'vertical', fontsize = 27, fontweight = 'bold')

for n in range(6):
    
    ax = plt.subplot(2, 3, n+1)
    
    ax.plot(caliop_area_average[:, :, n+1]*100000, caliop_alts, linewidth = 2, alpha = 0.4)
    ax.plot(caliop_monthly_mean[:, n+1]*100000, caliop_alts, color = 'navy', linewidth = 4, label = 'CALIOP Mean 532nm')
    ax.plot((caliop_monthly_mean[:, n+1] + caliop_monthly_std[:, n+1])*100000, caliop_alts, '--', color = 'navy', linewidth = 3, label = 'Standard Deviation')
    ax.plot((caliop_monthly_mean[:, n+1] - caliop_monthly_std[:, n+1])*100000, caliop_alts, '--', color = 'navy', linewidth = 3)

    ax.plot(so2_ash_area_average[:, n+1]*100, model_alts, color = 'r', linewidth = 4, label = 'UKESM1 SO2+ash')
    ax.plot(so2_only_area_average[:, n+1]*100, model_alts, color = 'r', linewidth = 4, linestyle = '--', label = 'UKESM1 SO2only')
    
    ax.axhline(caliop_mean_tph[n+1], color = 'g', linewidth = 3, linestyle = '-', alpha = 0.7, label = 'Mean Tropopause Height')
    ax.axhline(caliop_mean_tph[n+1] + caliop_std_tph[n+1], color = 'g', linewidth = 3, linestyle = ':', alpha = 0.7, label = 'Std Tropopause Height')
    ax.axhline(caliop_mean_tph[n+1] - caliop_std_tph[n+1], color = 'g', linewidth = 3, linestyle = ':', alpha = 0.7)

    ax.set_title(months[n+1], fontweight = 'bold')
    ax.set_xlim([-0.2, 1])
    ax.set_ylim([5, 20])
    ax.grid(which = 'minor', axis = 'y', alpha = 0.2)
    ax.grid(which = 'minor', axis = 'x', alpha = 0.2)
    
plt.savefig('Figure9.png', dpi = 300)   
plt.show()


