# ICRF-TOOLS
Several simple code for ICRF
# ICRF_parameters.py
This file contains several important constants that are widely used in the code. Please download it before using other codes. It contains:  
```python
c  = 299792458          #Light speed [m/s]  
e0 = 8.854187817e-12    #Vacuum Permittivity [F/m]  
u0 = 4*np.pi*1e-7     #Permeability of vacuum [H/m]  
q0 = 1.60217733e-19;    #Elementary positive charge [C]  
m0 = 1.6726231e-27;     #Atomic mass unit [kg]  
```

# Res_Freq.py
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

# Load.py 
By using fun_load_touchstone, one can converts `.sNp` files into complex S-matrices per frequency point.
It will return:
- `f`: 1D frequency array in `Hz`
- `S`: list of complex S-matrices of shape `(nports, nports)`, one per frequency

**Core reconstruction (magnitude + angle → complex):**

$$
S_{ij} = |S_{ij}|\, e^{j\theta_{ij}},\quad \theta_{ij}\ \text{in degrees}
$$

**Minimal usage:**

    import numpy as np
    from fun_load_touchstone import fun_load_touchstone

    f, S = fun_load_touchstone("input/example/smatrix_aug-like.s4p")  # f in Hz
    S11 = np.array([Sm[0,0] for Sm in S])  # complex S11 over frequency

**Note:** expects `S MA` (magnitude, angle in degrees). For `S DB` or `S RI`, extend the parsing and convert accordingly.

# smith_chart.py


<p align="center">
<img src="smith_chart_ex1.png" alt="示例图片" width="400">
</p>
<p align="center">
<img src="smith_chart_ex2.png" alt="示例图片" width="600">
</p>
<p align="center">
<img src="smith_chart_ex3.png" alt="示例图片" width="600">
</p>









