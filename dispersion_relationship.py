# -*- coding: utf-8 -*-
"""

"""
globals().clear()
import numpy as np
import matplotlib.pyplot as plt
from ICRF_parameters import Const, omega_ce, omega_ci, omega_pe, omega_pi, vth_e, vth_i, rho_e, lambda_D
plt.close('all')     #close all figures

# ---------------- 参数区 ----------------
npts = 1000

f   = 62e6              # RF frequency [Hz]
kpar = 11.0             # Parallel wavenumber k_parallel [m^-1]
B0  = 6.15              # Magnetic field B0 [T]
Te  = 10.0              # Electron temperature [eV] (scale-only; does not enter S/D/P)
Ti  = 10.0              # Ion temperature [eV] (scale-only; applied uniformly to all ions)

# density
Ne_min = 1.0e13         
Ne_max = 1.0e20

# Ion composition:
#   'xi' are relative weights; they are normalized to true fractions r_i = n_i / n_e
#   so that charge neutrality holds: sum_i (Z_i * r_i) = 1.
ions = [
    {"name": "D",  "A": 2.0, "Z": 1.0, "xi": 0.95},  # D
    {"name": "H",  "A": 1.0, "Z": 1.0, "xi": 0.05},  # H
    # {"name": "He", "A": 4.0, "Z": 2.0, "xi": 0.0}, # example
]


Ne     = 10.0 ** np.linspace(np.log10(Ne_min), np.log10(Ne_max), npts)
x      = Ne           
xlab   = r'$n_e$ [m$^{-3}$]'


# =========================
# Precompute basics
# =========================
pi = np.pi
c0 = Const.c
om = 2.0 * pi * f
k0 = om / c0
k02 = k0**2

# Electron terms
Oce = omega_ce(B0)        # scalar [rad/s]
ope = omega_pe(Ne)         # array [rad/s]

# Charge-neutral normalization: xi -> r_i = n_i/n_e
sumZxi = sum(sp["Z"] * sp["xi"] for sp in ions)
scale  = 1.0 / (sumZxi if sumZxi != 0 else 1.0)
for sp in ions:
    sp["xi_eff"] = sp["xi"] * scale         # ensures sum Z*xi_eff = 1
    sp["Ni"]     = sp["xi_eff"] * Ne        # ion density array [m^-3]
    sp["Oci"]    = omega_ci(B0, Z=sp["Z"], A=sp["A"])        # scalar [rad/s]
    sp["opi"]    = omega_pi(sp["Ni"], Z=sp["Z"], A=sp["A"])  # array  [rad/s]

# =========================
# Stix tensor (multi-species sums)
# =========================
den_e = om**2 - Oce**2
S = 1.0 - ope**2 / den_e
D = (Oce/om) * ope**2 / den_e
P = 1.0 - (ope/om)**2

for sp in ions:
    den_i = om**2 - sp["Oci"]**2
    S -= sp["opi"]**2 / den_i
    D += (sp["Oci"]/om) * sp["opi"]**2 / den_i
    P -= (sp["opi"]/om)**2


# =========================
# Fast/slow branches (coupled approx + full 4th-order)
# =========================
num_fast = (k02*S - kpar**2)**2 - (k02*D)**2
den_fast = (k02*S - kpar**2)
kfast2   = num_fast / den_fast
kslow2   = P * (k02*S - kpar**2) / S

a4 = 1.0
b4 = -(((S**2 - D**2)/S + P) * k02 - (P/S + 1.0) * kpar**2)
c4 = P * (k02**2 * (S**2 - D**2)/S + kpar**4 / S - 2.0 * k02 * kpar**2)
D4 = b4**2 - 4.0 * a4 * c4
sqrtD4 = np.sqrt(D4 + 0j)  # allow complex, then take real part
kfast2_full = np.real((-b4 - sqrtD4) / (2.0 * a4))
kslow2_full = np.real((-b4 + sqrtD4) / (2.0 * a4))

# =========================
# Helper scales (do not enter S, D, P)
# =========================
vte    = vth_e(Te) * np.ones_like(Ne)            # electron thermal speed [m/s]
vt_i   = vth_i(Ti, A=1.0) * np.ones_like(Ne)     # ion thermal speed [m/s], example A=1
rhoe   = rho_e(Te, B0) * np.ones_like(Ne)        # electron Larmor radius [m]
lDebye = lambda_D(Te, Ne)                        # Debye length [m]

def safe_lambda(k, tol=1e-12):
    """Return 2π / Re(k) with masking near Re(k)=0 to avoid divide-by-zero."""
    re = np.real(k)
    lam = np.full_like(re, np.nan, dtype=float)
    mask = np.abs(re) > tol
    lam[mask] = 2.0 * np.pi / re[mask]
    return lam

kfast    = np.sqrt(kfast2 + 0j)
kslow    = np.sqrt(kslow2 + 0j)
lam_fast = safe_lambda(kfast)
lam_slow = safe_lambda(kslow)

def signed_log10(arr):
    """Signed log10: sign(x) * log10(|x|) for |x|>1, else 0 (for plotting)."""
    out = np.zeros_like(arr, dtype=float)
    m = np.abs(arr) > 1.0
    out[m] = np.sign(arr[m]) * np.log10(np.abs(arr[m]))
    return out

kfast2_log      = signed_log10(kfast2)
kslow2_log      = signed_log10(kslow2)
kfast2_full_log = signed_log10(kfast2_full)
kslow2_full_log = signed_log10(kslow2_full)

# %%=========================
# Plots
# =========================

# Stix parameters (linear)
plt.figure()
lgx = np.log10(x)
plt.plot(lgx, S, label='S')
plt.plot(lgx, D, label='D')
plt.plot(lgx, P, label='P')
plt.xlabel(r'$\log_{10}(n_e)$ [m$^{-3}$]')
plt.ylabel('Stix parameters')
plt.legend(); plt.tight_layout()

# k_perp^2 (signed log10): approx vs full
plt.figure()
plt.plot(lgx, kfast2_log,      label='FW decoupled')
plt.plot(lgx, kfast2_full_log, label='Full root 1', color='blue')
plt.plot(lgx, kslow2_log,      label='SW decoupled')
plt.plot(lgx, kslow2_full_log, label='Full root 2')
plt.xlabel(r'$\log_{10}(n_e)$ [m$^{-3}$]')
plt.ylabel(r'signed $\log_{10}(k_\perp^2)$ [m$^{-2}$]')
plt.legend(); plt.tight_layout()

# === Extra: fast/slow shown separately (k_perp^2) ===
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))

lgx = np.log10(Ne)

ax1.plot(lgx, kfast2_log,      label='FW decoupled')
ax1.plot(lgx, kfast2_full_log, label='Full root 1')
ax1.set_ylabel(r'signed $\log_{10}(k_{\perp,\mathrm{fast}}^2)$ [m$^{-2}$]')
ax1.legend(loc='best')
ax1.grid(True, alpha=0.3)

ax2.plot(lgx, kslow2_log,      label='SW decoupled')
ax2.plot(lgx, kslow2_full_log, label='Full root 2')
ax2.set_xlabel(r'$\log_{10}(n_e)$ [m$^{-3}$]')
ax2.set_ylabel(r'signed $\log_{10}(k_{\perp,\mathrm{slow}}^2)$ [m$^{-2}$]')
ax2.legend(loc='best')
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# === Extra: dispersion in k_perp (Re/Im) for fast/slow, approx vs full ===
kfast_full = np.sqrt(kfast2_full + 0j)
kslow_full = np.sqrt(kslow2_full + 0j)

fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(7, 6))

# Fast wave
ax1.plot(lgx, np.real(kfast),       label='Re(k⊥) fast, decoupled')
ax1.plot(lgx, np.real(kfast_full),  '--', label='Re(k⊥) fast, full')
ax1.plot(lgx, np.imag(kfast),       ':',  label='Im(k⊥) fast, decoupled')
ax1.plot(lgx, np.imag(kfast_full),  '-.', label='Im(k⊥) fast, full')
ax1.set_ylabel(r'$k_{\perp,\mathrm{fast}}$ [m$^{-1}$]')
ax1.legend(loc='best', ncol=2)
ax1.grid(True, alpha=0.3)

# Slow wave
ax2.plot(lgx, np.real(kslow),       label='Re(k⊥) slow, decoupled')
ax2.plot(lgx, np.real(kslow_full),  '--', label='Re(k⊥) slow, full')
ax2.plot(lgx, np.imag(kslow),       ':',  label='Im(k⊥) slow, decoupled')
ax2.plot(lgx, np.imag(kslow_full),  '-.', label='Im(k⊥) slow, full')
ax2.set_xlabel(r'$\log_{10}(n_e)$ [m$^{-3}$]')
ax2.set_ylabel(r'$k_{\perp,\mathrm{slow}}$ [m$^{-1}$]')
ax2.legend(loc='best', ncol=2)
ax2.grid(True, alpha=0.3)

plt.tight_layout()

# =========================
# Print normalized composition
# =========================
print("\n=== Charge-neutral ion fractions (n_i / n_e) ===")
for sp in ions:
    print(f"{sp['name']}: (n_i/n_e) = {sp['xi_eff']:.6f},  Z={sp['Z']}, A={sp['A']}")
print(f"Check sum(Z_i * n_i/n_e) = {sum(sp['Z']*sp['xi_eff'] for sp in ions):.6f} (should be 1.000000)")

