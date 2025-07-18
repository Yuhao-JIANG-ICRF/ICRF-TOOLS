import numpy as np

class Const:
    """Fundamental physical constants"""

    c = 299_792_458             # Speed of light in vacuum [m/s]
    e0 = 8.854_187_817e-12      # Vacuum permittivity [F/m]
    u0 = 4 * np.pi * 1e-7       # Vacuum permeability [H/m]

    q0 = 1.602_177_33e-19       # Elementary charge [C]
    m0 = 1.672_623_1e-27        # Proton mass [kg]

    k_B = 1.38e-23              # Boltzmann constant [J/K]
    #k_B = 8.62e-5              # Boltzmann constant [eV/K]
    eV_to_J = 1.602e-19         # Electronvolt to joule

    @classmethod
    def show_all(cls):
        """Print all constants and their values"""
        for attr in dir(cls):
            if not attr.startswith("_") and not callable(getattr(cls, attr)):
                print(f"{attr:10} = {getattr(cls, attr)}")