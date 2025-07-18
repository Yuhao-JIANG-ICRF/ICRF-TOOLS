#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:54:55 2025

@author: Lara HIJAZI
"""
### cleaning in spyder
get_ipython().magic('reset -f')
get_ipython().magic('clear')
###
globals().clear()
import numpy as np
import matplotlib.pyplot as plt
from ICRF_parameters import Const

plt.close('all')     #close all figures

# Constants

# =============================================================================
# #west
# RB0 = 2.5;     #position of axis [m]
# R0 = 2.5;      #major radius [m]
# a  = 0.5;      #minor radius [m]
# B0 = 3.657;     #magnetic field [T]
# =============================================================================

# jet
RB0 = 2.96;     #position of axis [m]
R0 = 2.96;      #major radius [m]
a  = 0.96;      #minor radius [m]
B0 = 3.7;#3.7&3.4     #magnetic field [T]
# CFEDR
RB0 = 8.25;     #position of axis [m]
R0 = 7.8;      #major radius [m]
a  = 2.5;      #minor radius [m]
B0 = 6.3;#3.7&3.4     #magnetic field [T]

N = 2        # Harmonic number

# Define range of R values (from R0-a to R0+a) 
R = np.linspace(R0-a, R0+a, 200)
if not np.isclose(R, R0).any():
    R = np.sort(np.append(R, R0))
    indices = np.where(R == R0)[0]
    
RB0_value = globals().get('RB0', None)
if RB0_value is not None and RB0_value != R0 and not np.isclose(R, RB0_value).any():
    R = np.sort(np.append(R, RB0_value))
    indices = np.where(R == RB0_value)[0]
    
    
# Define the resonance frequency function
def resonance_frequency(Z, A):
    return  N* 1/(2*np.pi*1e6) * (Z * Const.q0)/(A * Const.m0) * (B0*R0) / R# MHz



# Compute f for different species
f_H = resonance_frequency(Z=1, A=1)   # Hydrogen (H)
f_D = resonance_frequency(Z=1, A=2)   # Deuterium (D)
f_T = resonance_frequency(Z=1, A=3)  # Helium (He)
f_He = resonance_frequency(Z=2, A=3)  # Helium (He)
f_Li = resonance_frequency(Z=3, A=7)  # Lithium (Li)

# Create the plot
plt.figure(figsize=(7, 5))
plt.rcParams.update({
    'lines.linewidth':2,
    'xtick.direction':'in',
    'ytick.direction':'in',
    'xtick.top':True,
    'xtick.bottom':True,
    'ytick.left':True,
    'ytick.right':True,
    'axes.grid':True, 
    'grid.linestyle': '--',  
    'grid.alpha': 0.6  
    })
plt.plot(R, f_H, label="H")
plt.plot(R, f_D, label="D")
plt.plot(R, f_T, label="T")
plt.plot(R, f_He, label="$^3$He")
plt.plot(R, f_Li, label="$^7$Li")


YL = plt.ylim()
if RB0_value is not None:
    plt.plot([RB0_value, RB0_value],[YL[0], YL[1]],'k--' ,label="Magnetic Axis")
    outline = f'At magnetic axis = {RB0_value} [m],'
else:
    plt.plot([R0, R0],[YL[0], YL[1]],'k--' ,label="Major Radius")
    outline = f'At major radius = {R0} [m],'


plt.xlim([R0-a, R0+a])
plt.ylim([YL[0], YL[1]])
# Labels and title
plt.xlabel("Resonance Position [m]", fontsize=12)
plt.ylabel("ICRF Frequency [MHz]", fontsize=12)
if N==1:
    plt.title("Fundamental Frequency vs Resonance Position", fontsize=14)
    outline = outline + '\n\n Fundamental resonance frequency:'
elif N==2:
    plt.title("Second Harmonic Frequency vs Resonance Position", fontsize=14)
    outline = outline + '\n\n second harmonic resonance frequency:'

# Formatting grid and legend
plt.legend(fontsize=11)

# Show plot
plt.show()
plt.plot(R, f_D, label="D")
plt.plot(R, f_T, label="T")
plt.plot(R, f_He, label="$^3$He")
plt.plot(R, f_Li, label="$^7$Li")

print(f'''
      {outline}
      H   = {f_H[indices].item():.1f} [MHz]
      D   = {f_D[indices].item():.1f} [MHz]
      T   = {f_T[indices].item():.1f} [MHz]
      He3 = {f_He[indices].item():.1f} [MHz]
      Li7 = {f_Li[indices].item():.1f} [MHz]
      ''')