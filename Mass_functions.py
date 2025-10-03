import numpy as np
from typing import Dict

# Rocket Engine Mass
# Inputs:
#   Thrust      : Thrust produced by the engine [Newtons]
#   Mixture     : Type of mixture, correlates to a specific Ae/At
#   Stage number: Stage 1 or 2
# Output:
#   Mass of rocket engine [kg]
def Rocket_Engine(
        Thrust                  : float,
        mixture                 : str,
        Expansion_ratio_stage   : Dict[str, float],

    )-> float:

    expansion_ratio = Expansion_ratio_stage[mixture]

    engine_mass = 7.81*10**(-4)*Thrust + 3.37*10**(-5)*Thrust*np.sqrt(expansion_ratio) + 59
    
    return engine_mass


# Motor Casing Mass
# Inputs:
#   M_pr : Propellant mass [kg]
# Output:
#   Motor casing mass [kg]
def Motor_Casing(M_pr: float)-> float:
    return 0.135*M_pr


# Structural Mass
# Inputs:
#   Thrust : Thrust produced by the stage [Newtons]
# Output:
#   Thrust Structure mass [kg]
def Struct_Mass(Thrust: float)-> float:
    return 2.25*10**(-4)*Thrust


# Payload Fairing Mass
# Inputs:
#   A_fairing : Fairing surface area [m^2]
# Output:
#   Fairing mass [kg]
def M_fairing(A_fairing: float)-> float:
    return 4.95*A_fairing**1.15


# Avionics Mass
# Inputs:
#   Mo : Stage initial mass [kg]
# Output:
#   Avionics mass [kg]
def M_avionic(Mo: float)-> float:
    return 10*Mo**0.361


# Wiring Mass
# Inputs:
#   Mo : Stage initial mass [kg]
#   l  : Stage 1 length [m]
# Output:
#   Wiring mass [kg]
def M_wiring(Mo: float, l: float)-> float:
    return 1.058*np.sqrt(Mo)*l**0.25


# Gimbal Mass
# Inputs:
#   Thrust : Thrust produced by the engine [Newtons]
#   Mixture: name of propellant mixture
#   Stage_number: stage 1 or stage 2
# Output:
#   Gimbal mass [kg]
def M_gimbals(
        Thrust                  : float,
        mixture                 : str,
        Chamber_pressure_stage  : Dict[str, int], 
    )-> float:

    Po = Chamber_pressure_stage[mixture]

    return 237.8*(Thrust/Po)**0.9375
