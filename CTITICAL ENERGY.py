#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 14:27:07 2025

@author: YJ281217
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
from scipy.optimize import root_scalar


def f1(Ne,Zi,Xi,Ai):
    fv = Ne*Xi*Zi**2/(Ne*Ai)
    return fv

X_H = 0.05
X_D = 0.50

X_T = 1-X_D-X_H

Z_D = 1
a_D = 2
Z_T = 1
a_T = 3
Z_H = 1
a_H = 1

Te = 10e3
Ne = 1.5e20
Af = a_D 

Ec = 14.8*Te*Af*(  f1(Ne,Z_T,X_T,a_T)
                 + f1(Ne,Z_D,X_D,a_D)
                 + f1(Ne,Z_H,X_T,a_H))**(2/3)

print(Ec/1e3)


#%% REDISTRUBUTION
# Define the integrand: 1 / (1 + y^(3/2))

def integrand(y):
    return 1 / (1 + y**1.5)

# Compute p_i(E0), the fraction of energy transferred to ions
# x = E0 / E_crit (normalized fast particle energy)
def p_i(x):
    if x == 0:
        return 1.0  # Avoid division by zero
    integral_result, _ = quad(integrand, 0, x)
    return (1 / x) * integral_result



# Create array of normalized energy values E0/E_crit from 0.01 to 10
x_vals = np.linspace(0.01, 10, 300)

# Compute power fractions for ions and electrons
fi_vals = np.array([p_i(x) for x in x_vals])   # F_i: power to ions
fe_vals = 1 - fi_vals                          # F_e: power to electrons

# Solve Fi(x) = 0.5
def equation_to_solve(x):
    return p_i(x) - 0.5

sol = root_scalar(equation_to_solve, bracket=[1, 5], method='brentq')
intersection_x = sol.root  # x where Fi = Fe = 0.5

# Plot the results
plt.figure(figsize=(8, 6))
plt.plot(x_vals, fi_vals, label=r'$F_i$', color='blue', linewidth=2)            # Power to ions
plt.plot(x_vals, fe_vals, label=r'$F_e$', color='green', linestyle='--', linewidth=2)  # Power to electrons

# Add vertical reference line at x = 2 and text annotations
plt.axvline(x=2, color='black', linestyle=':', linewidth=1)
plt.text(0.6, 0.82, 'Power\ntransfer\nmainly to ions', ha='center', va='center', fontsize=10, color='blue')
plt.text(6, 0.82, 'Power transfer\nmainly to electrons', ha='center', va='center', fontsize=10, color='green')

# Step 2: Plot the vertical line at the intersection point
plt.axvline(x=intersection_x, color='red', linestyle='--', linewidth=2, label='Fi = Fe')
# Step 3: Optional annotation
plt.text(intersection_x + 0.3, 0.52, f'Intersection\nx = {intersection_x:.2f}', color='red', fontsize=10)

# Axis labels and title
plt.xlabel(r'$E_0/E_{\mathrm{crit}}$', fontsize=12)
plt.ylabel('Power redistribution fractions', fontsize=12)
plt.title('Fast Particle Power Transfer to Ions vs Electrons', fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xlim([0,10])
plt.ylim([0,1])
plt.show()


