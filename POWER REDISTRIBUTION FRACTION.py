#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 18 14:15:36 2025

@author: YJ281217
"""

import numpy as np
import matplotlib.pyplot as plt

# 
x = np.linspace(0.01, 10, 500)  # E0 / Ec
y = (x/2.2)**2
# 
F_i = 1 / (1 + y)       # Power to ions
F_e = y / (1 + y)  # Power to electrons

# 
plt.figure(figsize=(7, 5))
plt.plot(x, F_i, 'b-', label=r'$F_i$ (ions)', linewidth=2)
plt.plot(x, F_e, 'g--', label=r'$F_e$ (electrons)', linewidth=2)

# 
#plt.axvline(x=1.55, color='gray', linestyle=':', linewidth=1)
#plt.text(1.6, 0.5, r'$E_0/E_c \approx 1.55$', fontsize=10)

plt.xlim([0,10])
plt.ylim([0,1])
plt.xlabel(r'$E_0 / E_c$', fontsize=12)
plt.ylabel('Power redistribution fractions', fontsize=12)
plt.title('Stix model: Power transfer to ions or electrons', fontsize=14)
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()