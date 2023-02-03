#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  1 16:03:04 2023

@author: Alice Wells

Plotting script for Figure 4 in Wells et al., 2023

Latitude-time distribution of the zonally averaged sAOD from 30–90° N. 
(a) UKESM1 SO2only masked for OMPS-LP observations, scaled from 550nm to 532nm 
(b) UKESM1 SO2only masked for CALIOP observations, sAOD calculated with values 
of aerosol extinction < 0.012 km-1, the CALIOP minimum detection limit, scaled 
to 532nm 
(c) OMPS-LP observations scaled from 869nm to 532nm 
(d) CALIOP observations at 532nm 
(e) UKESM1 SO2+ash masked for OMPS-LP observations, scaled from 550nm to 532nm 
(f) UKESM1 SO2+ash masked for CALIOP observations, sAOD calculated with values 
of aerosol extinction < 0.012 km-1, the CALIOP minimum detection limit, scaled 
to 532nm. The location of Raikoke is marked with a black cross.

"""
# =============================================================================
# Import functions
# =============================================================================

import numpy as np
import copy
import calendar
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as mpl_cm

# =============================================================================
# Load data
# =============================================================================

#Model SO2+ash with OMPS detection limits imposed
so2_ash_omps = np.load('SO2_ash_perturbation_daily_zonal_average_aod_omps_limits_532nm_1x1deg.npy')
#Model SO2only with OMPS detection limits imposed
so2_only_omps = np.load('SO2_only_perturbation_daily_zonal_average_aod_omps_limits_532nm_1x1deg.npy')
#Model SO2+ash with CALIOP detection limits imposed
so2_ash_caliop = np.load('SO2_ash_perturbation_daily_zonal_average_aod_caliop_limits_532nm_1x1deg.npy')
#Model SO2only with CALIOP detection limits imposed
so2_only_caliop = np.load('SO2_only_perturbation_daily_zonal_average_aod_caliop_limits_532nm_1x1deg.npy')

#OMPS observations
omps = np.load('omps_perturbation_daily_zonal_average_aod_532nm.npy')
#CALIOP observations
caliop = np.load('caliop_perturbation_daily_zonal_average_aod_532nm.npy')
    
# =============================================================================
# Create the omps model mask
# =============================================================================

#Find model points only where omps data exists
mask = np.ones( (181, 366) )
mask[np.isnan(omps)] = np.nan

#Mask the model data
so2_ash_omps_limits = so2_ash_omps*mask
so2_only_omps_limits = so2_only_omps*mask

# =============================================================================
# Create the calipso model mask
# =============================================================================

#Find model points only where calipso data exists
mask = np.ones( (181, 366) )
mask[np.isnan(caliop)] = np.nan

#Mask the model data
so2_ash_caliop_limits = so2_ash_caliop*mask      
so2_only_caliop_limits = so2_only_caliop*mask    

# =============================================================================
# Plotting
# =============================================================================

#Create array of days since eruption
dates = np.arange(-20, 346, 1)

#Definite latitude coordinates and ticks
latitude = range(0, 91)
lat_ticks = np.arange(45, 90, 15)
date_ticks = [-20, 10, 41, 72, 102, 133, 163, 194, 225, 254, 285, 315]

#Get months for plotting dates
months = calendar.month_name[6:13] + calendar.month_name[1:6]
for i in range(len(months)):
    months[i] = months[i][:3]

params = {'legend.fontsize': 25,
          'figure.figsize': (55, 25), #landscape
          'axes.labelsize': 60,
          'axes.titlesize': 60,
          'axes.linewidth': 5,
          'axes.grid': False,
          'xtick.labelsize':50,
          'ytick.labelsize':55,
          'xtick.major.size': 15,
          'xtick.minor.size': 5,
          'xtick.minor.visible':False,
          'ytick.major.size':15,
          'ytick.minor.size':5,
          'ytick.minor.visible':True,
          'lines.linewidth': 4} 

plt.rcParams.update(params)

col_map = copy.copy(mpl_cm.get_cmap('plasma'))
lvs = np.logspace(-3, -1, 13)
cbar_ticks = [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1]
norm = colors.BoundaryNorm(lvs, col_map.N)


fig = plt.figure(constrained_layout = True)
gs = fig.add_gridspec(3, 3, height_ratios = [20, 20, 4], width_ratios = [25, 25, 25])

#(c) OMPS
ax1 = fig.add_subplot(gs[0,1])
ax1.contourf(dates, latitude, omps[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax1.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax1.set_title('OMPS-LP scaled to 532nm', fontweight = 'bold')
ax1.set_ylabel('Latitude')
ax1.set_yticks(lat_ticks)
ax1.set_xticks(date_ticks)
ax1.set_xticklabels(months, rotation = 45)
ax1.set_ylim(30, 90)

#(d) CALIOP
ax2 = fig.add_subplot(gs[1, 1])
cb = ax2.contourf(dates, latitude, caliop[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax2.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax2.set_title('CALIOP 532nm', fontweight = 'bold')
ax2.set_ylabel('Latitude')
ax2.set_yticks(lat_ticks)
ax2.set_xticks(date_ticks)
ax2.set_xticklabels(months, rotation = 45)
ax2.set_ylim(30, 90)

#(a) Model SO2only with OMPS limits
ax3 = fig.add_subplot(gs[0, 0])
cb = ax3.contourf(dates, latitude, so2_only_omps_limits[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax3.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax3.set_title('UKESM1 SO2only OMPS-LP limits', fontweight = 'bold')
ax3.set_ylabel('Latitude')
ax3.set_yticks(lat_ticks)
ax3.set_xticks(date_ticks)
ax3.set_xticklabels(months, rotation = 45)
ax3.set_ylim(30, 90)

#(b) Model SO2only with CALIOP limits
ax4 = fig.add_subplot(gs[1, 0])
cb = ax4.contourf(dates, latitude, so2_only_caliop_limits[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax4.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax4.set_title('UKESM1 SO2only CALIOP limits', fontweight = 'bold')
ax4.set_ylabel('Latitude')
ax4.set_xticks(date_ticks)
ax4.set_xticklabels(months, rotation = 45)
ax4.set_yticks(lat_ticks)
ax4.set_ylim(30, 90)

#(e) Model SO2+ash with OMPS limits
ax5 = fig.add_subplot(gs[0, 2])
cb = ax5.contourf(dates, latitude, so2_ash_omps_limits[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax5.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax5.set_title('UKESM1 SO2+ash OMPS-LP limits', fontweight = 'bold')
ax5.set_ylabel('Latitude')
ax5.set_yticks(lat_ticks)
ax5.set_xticks(date_ticks)
ax5.set_xticklabels(months, rotation = 45)
ax5.set_ylim(30, 90)

#(f) Model SO2+ash with CALIOP limits
ax6 = fig.add_subplot(gs[1, 2])
cb = ax6.contourf(dates, latitude, so2_ash_caliop_limits[90:, :], levels = lvs, cmap = col_map, norm = norm, extend = 'both')
ax6.plot(0, 48, 'x', color = 'k', markersize = 20, markeredgewidth = 5)
ax6.set_title('UKESM1 SO2+ash CALIOP limits', fontweight = 'bold')
ax6.set_ylabel('Latitude')
ax6.set_xticks(date_ticks)
ax6.set_xticklabels(months, rotation = 45)
ax6.set_yticks(lat_ticks)
ax6.set_ylim(30, 90)

cax = fig.add_subplot(gs[-1, :])
cbar = fig.colorbar(cb, cax = cax, ticks = cbar_ticks, orientation='horizontal')
cbar.set_label('sAOD', fontsize=60)
cbar.ax.tick_params(size=0, labelsize = 50)

plt.savefig('Figure4.png', dpi = 300)
plt.show()