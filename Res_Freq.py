#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:54:55 2025

@author: Lara HIJAZI
"""
### cleaning in spyder
#get_ipython().magic('reset -f')
#get_ipython().magic('clear')
###
globals().clear()
import numpy as np
import matplotlib.pyplot as plt
from ICRF_parameters import Const

plt.close('all')     #close all figures

import matplotlib as mpl
mpl.rcParams.update({
    'image.cmap':     'viridis',   #viridis,plasma,inferno,magma,cividis
    'font.size': 16,         # base font size for text
    'axes.titlesize': 16,    # title font size
    'axes.labelsize': 20,    # x/y label font size
    'xtick.labelsize': 16,   # x-axis tick label size
    'ytick.labelsize': 16,   # y-axis tick label size
    'legend.fontsize': 16,
    'figure.titlesize':15,
    'contour.linewidth': 2,
    'xtick.direction':'in',
    'ytick.direction':'in',
    'xtick.top':True,
    'xtick.bottom':True,
    'ytick.left':True,
    'ytick.right':True
})

# Setup

# -------- Machine selector --------
machine = "CFEDR"   # "WEST", "JET", or "CFEDR"
N = 2  # harmonic number



# --- Device geometry & magnetic field ---
#RB0 (m) magnetic-axis major radius (R_axis; plasma axis after Shafranov shift)
#R0  (m) geometric major radius (R_geo)
#a   (m) minor radius of the plasma cross-section
#B0  (T) toroidal magnetic field evaluated at R = R0

if machine == "WEST":
    RB0, R0, a, B0 = 2.5, 2.5, 0.5, 3.657
elif machine == "JET":
    RB0, R0, a, B0 = 2.96, 2.96, 0.96, 3.7
elif machine == "CFEDR":
    RB0, R0, a, B0 = 8.25, 7.8, 2.5, 6.3
else:
    raise ValueError("Unknown machine")



# Radius grid
R = np.linspace(R0 - a, R0 + a, 200)

    
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

plt.plot(R, f_H, label="H")
plt.plot(R, f_D, label="D")
plt.plot(R, f_T, label="T")
plt.plot(R, f_He, label="$^3$He")
plt.plot(R, f_Li, label="$^7$Li")


# Reference position & label
use_axis = not np.isclose(RB0, R0)
ref_pos  = RB0 if use_axis else R0
plt.axvline(ref_pos, linestyle='--', color='k',
            label=("Magnetic Axis" if use_axis else "Major Radius"))

plt.xlim(R0 - a, R0 + a)
plt.xlabel("Resonance Position (m)")
plt.ylabel("ICRF Frequency (MHz)")

harmonic_str = "Fundamental" if N == 1 else "Second Harmonic"
plt.title(f"{machine}\n{harmonic_str} Frequency vs Resonance Position")

plt.legend(fontsize=13)
plt.show()

# Safe index via closest point (no equality assumptions)
idx_ref = int(np.argmin(np.abs(R - ref_pos)))

outline = (f"At magnetic axis = {ref_pos:.2f} (m),"
           if use_axis else
           f"At major radius = {ref_pos:.2f} (m),")
which_harm = "Fundamental" if N == 1 else "Second harmonic"

print(f"""
{outline}

{which_harm} resonance frequency:
H   = {f_H[idx_ref]:.1f} (MHz)
D   = {f_D[idx_ref]:.1f} (MHz)
T   = {f_T[idx_ref]:.1f} (MHz)
He3 = {f_He[idx_ref]:.1f} (MHz)
Li7 = {f_Li[idx_ref]:.1f} (MHz)
""")