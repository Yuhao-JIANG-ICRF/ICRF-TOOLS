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

This program draws a Smith chart on the complex plane and places one or more S-parameters (complex reflection coefficient $\Gamma$) at their corresponding locations. It supports 1) points, 2) polylines, and 3) arrows to show how the locus evolves with frequency.

The chart is drawn in the $\Gamma$-plane (reflection-coefficient plane). Starting from the normalized impedance $z = Z/Z_0$, the relationship with the reflection coefficient is

$$
\Gamma = \frac{z-1}{z+1}, \qquad
z = \frac{1+\Gamma}{1-\Gamma}.
$$

For S-parameters given by magnitude and phase, the complex form is

$$
S = |S|\,e^{j\theta},
$$

where $\theta$ may be in radians or degrees. If your Touchstone reader returns degrees, convert to radians before using trigonometric functions; this program expects complex $S$ directly.

The resistance and reactance families on the Smith chart satisfy the following geometry.

- **Constant resistance** $r=\text{const}$: center and radius in the Γ-plane
- 
  $$
  x_c=\frac{r}{1+r}, \qquad R=\frac{1}{1+r},
  $$
  
  with circle equation $(x-x_c)^2+y^2=R^2$.

- **Constant reactance** $x=\text{const}$: center and radius
- 
  $$
  x_c=1,\qquad y_c=\frac{1}{x},\qquad R=\frac{1}{|x|},
  $$
  
  with circle equation $(x-1)^2+(y-y_c)^2=R^2$.

The program draws these resistance and reactance families and clips them to the unit circle.

## Code structure and core interface

The core function is:
```python
smith_Smatrix(S, num=1, display_mode='points_and_arrows')



<p align="center"><b>Smith chart display modes</b></p>
<div align="center">
  <table width="100%">
    <tr>
      <td align="center" width="33%">
        <img src="images/smith_chart_ex1.png" alt="(a) Points + arrows" width="95%"><br>
        <sub>(a) Points + arrows</sub>
      </td>
      <td align="center" width="33%">
        <img src="images/smith_chart_ex2.png" alt="(b) Line with end arrow" width="95%"><br>
        <sub>(b) Line with end arrow</sub>
      </td>
      <td align="center" width="33%">
        <img src="images/smith_chart_ex3.png" alt="(c) Points only" width="95%"><br>
        <sub>(c) Points only</sub>
      </td>
    </tr>
  </table>
</div>




