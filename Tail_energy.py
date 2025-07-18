#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 09:58:43 2025

@author: YJ281217
"""

import numpy as np
import matplotlib.pyplot as plt
from ICRF_parameters import Const
# parameter setup

Te = 10 #keV
Ne = 1.5*1e20 #
Z_D = 2
a_D = 1

kb = Const.k_B
eV_J = Const.eV_to_J

P_dens = np.linspace(0.1,2,100)
P_dens_W = P_dens*1e6
C_m = np.linspace(5,15,100)
C_mf = C_m / 100

P_mesh, X_mesh = np.meshgrid(P_dens_W, C_mf)


# slowing-down time
tau_s = 0.012 * a_D * (Te)**1.5 / (Z_D**2 * Ne/ 1e20)

# factor xi
xi = P_mesh * tau_s / (3 * Ne*X_mesh * kb * Te*1e3)

#T_eff
T_eff = Te * xi

#PLOT
plt.figure(figsize=(8, 6))
cp = plt.contourf(P_dens, C_m, T_eff, levels=50, cmap='rainbow')
lines = plt.contour(P_dens, C_m, T_eff, levels=30, colors='black', linewidths=0.8)
#plt.clabel(lines, inline=True, fontsize=8) 
plt.colorbar(cp, label='D tail energy [keV]')
plt.xlabel('Power density [MW/m³]')
plt.ylabel('Minority concentration [%]')
plt.title(f'D tail energy [keV] - $N_e$ = {Ne:.1e}/m³ - $T_e$ = {Te} keV')
plt.tight_layout()
plt.show()



