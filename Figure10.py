#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:08:06 2023

@author: Alice Wells

Plotting script for Figure 10 in Wells et al., 2023

Aerosol extinction coefficient vertical profile averaged longitudinally. 
Averaged monthly CALIOP (centre) aerosol extinction coefficient vertical 
profiles (night retrievals only) with monthly average tropopause height 
(solid black). UKESM1 SO2 only (left) and SO2+ash (right) simulations with 
imposed CALIOP minimum retrieval limits and mask. 

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import calendar
import matplotlib.colors as colors
import matplotlib.cm as mpl_cm

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
model_alts[0] = 0
#Model tropopause height
model_tph = np.load('Model_monthly_zonal_average_tropopause_height.npy')

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

masked_tph = model_tph * mask 

# =============================================================================
# Define altitude profile
# =============================================================================
    
alts1 = np.linspace(-500, 20200, 346)
alts2 = np.linspace(20380, 29740, 53)
caliop_alts = np.hstack( (alts1, alts2) )/1000
   
#Define latitude coordinates
latitude = range(-90, 91)
#Create months for plotting dates
months = calendar.month_name[6:13] + calendar.month_name[1:6]

#Calculate monthly average for CALIOP
caliop_monthly_mean = np.nanmean(caliop[:, :, :, :], axis = 2)
caliop_monthly_tph = np.nanmean(caliop_tph, axis = 1)

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

fig = plt.figure(figsize = (37, 38))
gs = fig.add_gridspec(6, 4, width_ratios = [25, 25, 25, 5])

fig.text(0.5, 0.08, 'Latitude', ha = 'center', va = 'center', fontsize = 35, fontweight = 'bold')
fig.text(0.08, 0.5, 'Altitude [km]', ha = 'center', va = 'center', rotation = 'vertical', fontsize = 35, fontweight = 'bold')

col_map = mpl_cm.get_cmap('plasma')
lvs = np.linspace(0, 1.2, 13)
norm = colors.BoundaryNorm(lvs, col_map.N)

i = 1

for n in range(6):
    
    ax1 = fig.add_subplot(gs[n, 0])
    ax1.contourf(latitude, model_alts, np.transpose(so2_only_masked[:, :, n+1]*100), cmap = col_map, levels = lvs, norm = norm, extend = 'both')
    ax1.plot(latitude, masked_tph[:, n+1]/1000, linewidth = 4, color = 'k')

    ax1.set_xlim([25, 85])
    ax1.set_ylim([5, 20])
    ax1.grid(which = 'minor', axis = 'y', alpha = 0.2)
    ax1.grid(which = 'minor', axis = 'x', alpha = 0.2)
    ax1.set_title('UKESM1 SO2only ' + months[n+1], fontweight = 'bold', fontsize = 25)
    
    ax2 = fig.add_subplot(gs[n, 1])
    ax2.contourf(latitude, caliop_alts, np.transpose(caliop_monthly_mean[:, :, n+1]*100000), cmap = col_map, levels = lvs, norm = norm, extend = 'both')
    ax2.plot(latitude, caliop_monthly_tph[:, n+1], linewidth = 4, color = 'k')   
    
    ax2.set_xlim([25, 85])
    ax2.set_ylim([5, 20])
    ax2.grid(which = 'minor', axis = 'y', alpha = 0.2)
    ax2.grid(which = 'minor', axis = 'x', alpha = 0.2) 
    ax2.set_title('CALIOP ' + months[n+1], fontweight = 'bold', fontsize = 25)
    
    ax3 = fig.add_subplot(gs[n, 2])
    cb = ax3.contourf(latitude, model_alts, np.transpose(so2_ash_masked[:, :, n+1]*100), cmap = col_map, levels = lvs, norm = norm, extend = 'both')
    ax3.plot(latitude, masked_tph[:, n+1]/1000, linewidth = 4, color = 'k')
    
    ax3.set_xlim([25, 85])
    ax3.set_ylim([5, 20])
    ax3.grid(which = 'minor', axis = 'y', alpha = 0.2)
    ax3.grid(which = 'minor', axis = 'x', alpha = 0.2)
    ax3.set_title('UKESM1 SO2+ash ' + months[n+1], fontweight = 'bold', fontsize = 25)
    
    cax = fig.add_subplot(gs[:, -1])
    plt.colorbar(cb, cax=cax, orientation = 'vertical', label = 'Aerosol extinction coefficient [$x10^{-2}$ km$^{-1}$]')
    
    i = i + 4

plt.savefig('Figure10.png', dpi = 300)
plt.show()