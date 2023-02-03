#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 17:13:00 2023

@author: Alice Wells

Plotting script for Figure 11 in Wells et al., 2023

The sAOD for July at 550nm for a) Sarychev Peak derived from HadGEM2 and b) 
Raikoke derived from UKESM1. The cloud-free radiative forcing at the top of 
the atmosphere (Wm-2) for c) Sarychev Peak derived from HadGEM2 and d) Raikoke 
derived from UKESM1.

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

#Sarychev radiative forcing
S_rad = np.load('Sarychev_HADGEM_radiative_forcing.npy')
#Raikoke-only SO2+ash radiative forcing
R_so2_ash_rad = np.load('Raikoke_only_SO2_ash_radiative_forcing.npy')
#Raikoke-only SO2only radiative forcing
R_so2_only_rad = np.load('Raikoke_only_SO2_only_radiative_forcing.npy')

#Sarychev AOD
S_aod = np.load('Sarychev_HADGEM_AOD.npy')
#Raikoke-only SO2+ash AOD
R_so2_ash_aod = np.load('Raikoke_only_SO2_ash_AOD.npy')
#Raikoke-only SO2only AOD
R_so2_aod = np.load('Raikoke_only_SO2_only_AOD.npy')

#Define latitude and longitude coordinates for Sarychev and Raikoke
S_latitude = np.arange(-90, 91, 1.25)
R_latitude = np.arange(-89.375, 90.625, 1.25)

S_longitude = np.arange(-180, 180, 1.875)
R_longitude = np.arange(-179.0625, 180.9375, 1.875)

# =============================================================================
# Plotting
# =============================================================================

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

fig = plt.figure(figsize = (25, 10), facecolor = 'w', edgecolor = 'k')

cmap_rad = copy.copy(mpl_cm.get_cmap('coolwarm'))
lvs_rad = [-5, -2, -1, -0.5, -0.2, 0.2, 0.5, 1, 2, 5]
norm_rad = colors.BoundaryNorm(lvs_rad, cmap_rad.N)

cmap_aod = copy.copy(mpl_cm.get_cmap('plasma'))
lvs_aod = [0.002, 0.004, 0.006, 0.008, 0.02, 0.04, 0.06, 0.08, 0.2, 0.4]
norm_aod = colors.BoundaryNorm(lvs_aod, cmap_aod.N)

gs = fig.add_gridspec(3, 2, height_ratios = [10, 10, 1], width_ratios = [20, 20])

# =============================================================================
# AOD
# =============================================================================
ax1 = fig.add_subplot(gs[0, 0], projection=ccrs.PlateCarree(180))
cs = plt.contourf(S_longitude, S_latitude, S_aod[:, :, 1], levels = lvs_aod, cmap = cmap_aod, norm = norm_aod, extend = 'both')  
plt.title('Sarychev July 2009 AOD')
        
ax1.coastlines()
ax1.set_xlim( [-180, 180] )
ax1.set_ylim( [0, 90] )

ax2 = fig.add_subplot(gs[1, 0], projection=ccrs.PlateCarree(central_longitude = 180))
cs = plt.contourf(R_longitude, R_latitude, R_so2_ash_aod[:, :, 2], levels = lvs_aod, cmap = cmap_aod, norm = norm_aod, extend = 'both')
plt.title('Raikoke August 2019 AOD')
        
ax2.coastlines()
ax2.set_xlim( [-180, 180] )
ax2.set_ylim( [0, 90] )

cax = fig.add_subplot(gs[-1, 0])          
bar = plt.colorbar(cax=cax, orientation='horizontal')
bar.set_ticklabels(np.round(lvs_aod, 4))  
bar.set_label('Aerosol Optical Depth 550nm')
bar.ax.tick_params(labelsize = 20)

# =============================================================================
# Radiative fdrcing
# =============================================================================
ax3 = fig.add_subplot(gs[0, 1], projection=ccrs.PlateCarree(central_longitude = 180))
cs = plt.contourf(S_longitude, S_latitude, S_rad[:, :, 1] , levels = lvs_rad, cmap = cmap_rad, norm = norm_rad, extend = 'both')
plt.title('Sarychev July 2009 RF')
        
ax3.coastlines()
ax3.set_xlim( [-180, 180] )
ax3.set_ylim( [0, 90] )

ax4 = fig.add_subplot(gs[1, 1], projection=ccrs.PlateCarree(central_longitude = 180))
cs = plt.contourf(R_longitude, R_latitude, R_so2_ash_rad[:, :, 2], levels = lvs_rad, cmap = cmap_rad, norm = norm_rad, extend = 'both')
plt.title('Raikoke August 2019 RF')
        
ax4.coastlines()
ax4.set_xlim( [-180, 180] )
ax4.set_ylim( [0, 90] )

cax1 = fig.add_subplot(gs[-1, 1])          
bar1 = plt.colorbar(cax=cax1, orientation='horizontal')
bar1.set_ticklabels([-5, -2, -1, -0.5, -0.2, 0.2, 0.5, 1, 2, 5])  
bar1.set_label('Radiative Forcing (Wm-2)')
bar1.ax.tick_params(labelsize = 20)

plt.tight_layout()
plt.savefig('Figure11.png', dpi = 300)
plt.show()   
