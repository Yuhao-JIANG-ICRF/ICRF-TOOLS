# ICRF-TOOLS
Several simple code for ICRF
# ICRF_parameters
This file contains several important constants that are widely used in the code. Please download it before using other codes. It contains:  
```python
c  = 299792458          #Light speed [m/s]  
e0 = 8.854187817e-12    #Vacuum Permittivity [F/m]  
u0 = 4*np.pi*1e-7     #Permeability of vacuum [H/m]  
q0 = 1.60217733e-19;    #Elementary positive charge [C]  
m0 = 1.6726231e-27;     #Atomic mass unit [kg]  
```

# Res_Freq ---Author: Lara Hijazi
This tool calculates the ICRF resonance frequency as a function of the plasma’s radial position, providing both graphical outputs and precise frequency values at the Rajor radius and magnetic axis. Based on following equations:

$$
B(R) = \frac{B_0*R_0}{R}
$$

$$
\omega_i = 2\pi f = \frac{Zq*B}{Am_p}
$$

Therefore:

$$
f = \frac{1}{2\pi}\frac{Zq*B_0R_0}{A\,m_p}\frac{1}{R}
$$

By input the parameters major radius (position of axis), minor radius, magnetic field and harmonic number. One can get following results:
<p align="center">
<img src="images/Res_Freq_ex1.png" alt="示例图片" width="400">
</p>
<p align="center">
<img src="images/Res_Freq_ex2.png" alt="示例图片" width="600">
</p>

# Smith Chart
