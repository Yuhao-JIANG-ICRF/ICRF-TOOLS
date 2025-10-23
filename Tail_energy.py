#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 09:58:43 2025

@author: YJ281217
"""
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
# parameter setup

Te = 10 #keV
Ne = 1.5*1e20 # density
Z_D = 1
A_D = 2

C_m = np.linspace(5,15,100)     # concentration scan range [%]
P_dens = np.linspace(0.1,2,100) # power density scan range [MW]


eV_to_J = 1.602e-19         # Electronvolt to joule 

eV_J = Const.eV_to_J
P_dens_W = P_dens*1e6
C_mf = C_m / 100
P_mesh, X_mesh = np.meshgrid(P_dens_W, C_mf)


E_particle = Te * 1e3 * eV_J 
# slowing-down time
tau_s = 0.012 * A_D * (Te)**1.5 / (Z_D**2 * Ne/ 1e20)

# factor xi
xi = P_mesh * tau_s / (3 * Ne*X_mesh * E_particle)

#T_eff
T_eff = Te * (xi+1)


##----------plot title--------------
def sci_tex(x, digits=1, star=True):
    """
    Return x in LaTeX-like scientific notation string for matplotlib mathtext.
    Example: 1.5e20 -> '1.5*10^{20}' (star=True) or '1.5\\times10^{20}' (star=False)
    """
    s = f"{x:.{digits}e}"       # e.g. '1.5e+20'
    m, e = s.split('e')
    e = int(e)                  # +20 -> 20, -03 -> -3
    if '.' in m:
        m = m.rstrip('0').rstrip('.')
    sep = r"*" if star else r"\times"
    return rf"{m}{sep}10^{{{e}}}"
Ne_tex = sci_tex(Ne, digits=1, star=True) 

title = rf'$N_e = {Ne_tex}\ \mathrm{{m}}^{{-3}}\ -\ T_e = {Te}\ \mathrm{{keV}}$'
#-----------PLOT--------------------
plt.figure(figsize=(8, 6))
cp = plt.contourf(P_dens, C_m, T_eff, levels=100, cmap='rainbow')
lines = plt.contour(P_dens, C_m, T_eff, levels=30, colors='black', linewidths=0.8)
#plt.clabel(lines, inline=True, fontsize=8) 
plt.colorbar(cp, label='D tail energy (keV)')
plt.xlabel(r'Power density (MW/m$^3$)')
plt.ylabel('Minority concentration (%)')
plt.title(title)
plt.tight_layout()
plt.show()



