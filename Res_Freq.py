#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 16:54:55 2025

@author: YJ281217
"""

import numpy as np
import matplotlib.pyplot as plt

# Constants
B0 = 3.657  # Tesla
N = 1        # Harmonic number


# Define range of R0 values (from 2m to 3m)
R0_values = np.linspace(2.0, 3.0, 100)

# Define the resonance frequency function
def resonance_frequency(R0, Z, A):
    return (15.225 * B0 * N * Z*2.5) / (A * (R0_values))  # MHz

# Compute f for different species
f_H = resonance_frequency(R0_values, Z=1, A=1)   # Hydrogen (H)
f_D = resonance_frequency(R0_values, Z=1, A=2)   # Deuterium (D)
f_He = resonance_frequency(R0_values, Z=2, A=4)  # Helium (He)
f_Li = resonance_frequency(R0_values, Z=3, A=7)  # Lithium (Li)

# Create the plot
plt.figure(figsize=(7, 5))
plt.plot(R0_values, f_H, label="H 1st & D 2nd", linewidth=2)
plt.plot(R0_values, f_He, label="He", linewidth=2)
plt.plot(R0_values, f_Li, label="Li", linewidth=2)

# Labels and title
plt.xlabel("R (m)", fontsize=12)
plt.ylabel("f (MHz)", fontsize=12)
plt.title("Resonance Frequency vs Major Radius", fontsize=14)

# Formatting grid and legend
plt.grid(True, linestyle="--", alpha=0.6)
plt.legend(fontsize=11)

# Show plot
plt.show()