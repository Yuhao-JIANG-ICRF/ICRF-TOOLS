import numpy as np

class Const:
    """Fundamental physical constants
    
    Notes
    -----
    - Values follow the post-2019 SI (e, k_B, c are exact).
    """

    # --- Base constants (SI) ---
    c = 299_792_458                     # Speed of light in vacuum [m/s]
    e0 = 8.854_187_8128e-12             # Vacuum permittivity [F/m]
    u0 = 4 * np.pi * 1e-7               # Vacuum permeability [H/m]

    q_e = 1.602_176_634e-19             # Elementary charge [C]
    m_e = 9.109_383_7015e-31            # Electron mass [kg]
    m_p = 1.672_621_923_69e-27          # Proton mass [kg]

    k_B = 1.380_649e-23                 # Boltzmann constant [J/K]
    eV_to_J = q_e                       # Electronvolt to joule
    
    
    @classmethod
    def show_all(cls):
        """Print all constant names and values."""
        for name in dir(cls):
            val = getattr(cls, name)
            if not name.startswith("_") and not callable(val):
                print(f"{name:12} = {val!r}")


    # --- Derived “ready-to-use” coefficients (for common formulas) ---
    @classmethod
    def omega_ce_coef(cls):
        """Coefficient for electron cyclotron angular frequency:
        ω_ce = (q_e/m_e) * B  → [rad·s⁻¹·T⁻¹]."""
        return cls.q_e / cls.m_e  # ≈ 1.758820e11

    @classmethod
    def omega_ci_coef(cls):
        """Reference coefficient for ion cyclotron angular frequency with m_p:
        ω_ci ≈ (q_e/m_p) * (Z/A) * B → [rad·s⁻¹·T⁻¹] (without Z/A)."""
        return cls.q_e / cls.m_p   # ≈ 9.578833e7

    @classmethod
    def omega_pe_coef(cls):
        """Coefficient for electron plasma angular frequency:
        ω_pe = sqrt(n_e q_e² /(ε0 m_e)) = coef * sqrt(n_e[m⁻³]) → [rad/s]."""
        return np.sqrt(cls.q_e**2 / (cls.e0 * cls.m_e))  # ≈ 56.4146

    @classmethod
    def omega_pi_coef(cls):
        """Reference coefficient for ion plasma angular frequency with m_p:
        ω_pi ≈ coef * Z * sqrt(n_i/A), coef = sqrt(q_e²/(ε0 m_p)) → [rad/s]."""
        return np.sqrt(cls.q_e**2 / (cls.e0 * cls.m_p))  # ≈ 1.31655


# -------- Helper functions for common plasma quantities --------

def omega_ce(B_T):
    """Electron cyclotron angular frequency ω_ce [rad/s].

    Parameters
    ----------
    B_T : float or ndarray
        Magnetic field in tesla.
    """
    return -Const.omega_ce_coef() * B_T


def omega_ci(B_T, Z=1.0, A=1.0):
    """Ion cyclotron angular frequency ω_ci [rad/s], with m_i ≈ A * m_p.

    Parameters
    ----------
    B_T : float or ndarray
        Magnetic field in tesla.
    Z : float
        Ion charge state.
    A : float
        Mass number (≈ atomic mass in units of m_p).
    """
    m_i = A * Const.m_p
    return (Z * Const.q_e / m_i) * B_T


def omega_pe(n_e_m3):
    """Electron plasma angular frequency ω_pe [rad/s].

    Parameters
    ----------
    n_e_m3 : float or ndarray
        Electron number density in m⁻³.
    """
    return Const.omega_pe_coef() * np.sqrt(n_e_m3)


def omega_pi(n_i_m3, Z=1.0, A=1.0):
    """Ion plasma angular frequency ω_pi [rad/s], with m_i ≈ A * m_p.

    Parameters
    ----------
    n_i_m3 : float or ndarray
        Ion number density in m⁻³.
    Z : float
        Ion charge state.
    A : float
        Mass number.
    """
    m_i = A * Const.m_p
    return np.sqrt(n_i_m3 * (Z * Const.q_e)**2 / (Const.e0 * m_i))


def vth_e(Te_eV, oneD=True):
    """Electron thermal speed v_th,e [m/s].

    Parameters
    ----------
    Te_eV : float or ndarray
        Electron temperature in eV.
    oneD : bool
        If True uses sqrt(kT/m); if False uses sqrt(2kT/m).
    """
    factor = 1.0 if oneD else 2.0
    return np.sqrt(factor * Const.eV_to_J * Te_eV / Const.m_e)


def vth_i(Ti_eV, A=1.0, oneD=True):
    """Ion thermal speed v_th,i [m/s], with m_i ≈ A * m_p.

    Parameters
    ----------
    Ti_eV : float or ndarray
        Ion temperature in eV.
    A : float
        Mass number.
    oneD : bool
        If True uses sqrt(kT/m); if False uses sqrt(2kT/m).
    """
    factor = 1.0 if oneD else 2.0
    m_i = A * Const.m_p
    return np.sqrt(factor * Const.eV_to_J * Ti_eV / m_i)


def rho_e(Te_eV, B_T, oneD=True):
    """Electron Larmor radius ρ_e [m] via v_th / |ω_c|."""
    return vth_e(Te_eV, oneD=oneD) / np.abs(omega_ce(B_T))


def rho_i(Ti_eV, B_T, Z=1.0, A=1.0, oneD=True):
    """Ion Larmor radius ρ_i [m] via v_th / |ω_c|, with m_i ≈ A * m_p."""
    return vth_i(Ti_eV, A=A, oneD=oneD) / np.abs(omega_ci(B_T, Z=Z, A=A))


def lambda_D(Te_eV, n_e_m3):
    """Debye length λ_D [m].

    Parameters
    ----------
    Te_eV : float or ndarray
        Electron temperature in eV.
    n_e_m3 : float or ndarray
        Electron number density in m⁻³.
    """
    return np.sqrt(Const.e0 * Const.eV_to_J * Te_eV / (n_e_m3 * Const.q_e**2))


# Public API on `from physconst import *`
__all__ = [
    "Const",
    "omega_ce", "omega_ci", "omega_pe", "omega_pi",
    "vth_e", "vth_i", "rho_e", "rho_i", "lambda_D",
]