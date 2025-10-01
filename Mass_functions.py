import numpy as np

# remove when done
from dictionaries import (
    Isp_values,
    Thrust_stage1,
    Thrust_stage2,
    Expansion_ratio_stage1,
    Expansion_ratio_stage2,
    Chamber_pressure_stage1,
    Chamber_pressure_stage2,
    fuel_ratios,
    prop_densities
)

# Rocket Engine Mass
# Inputs:
#   Thrust      : Thrust produced by the engine [Newtons]
#   Mixture     : Type of mixture, correlates to a specific Ae/At
#   Stage number: Stage 1 or 2
# Output:
#   Mass of rocket engine [kg]
def Rocket_Engine(Thrust, mixture, stage_number):
    if stage_number not in [1, 2]:
        raise ValueError('Stage number must be 1 or 2')
    
    expansion_ratio = (Expansion_ratio_stage1[mixture] if stage_number == 1 
                       else Expansion_ratio_stage2[mixture])

    engine_mass = 7.81*10**(-4)*Thrust + 3.37*10**(-5)*Thrust*np.sqrt(expansion_ratio) + 59
    
    return engine_mass


# Motor Casing Mass
# Inputs:
#   M_pr : Propellant mass [kg]
# Output:
#   Motor casing mass [kg]
def Motor_Casing(M_pr):
    return 0.135*M_pr


# Structural Mass
# Inputs:
#   Thrust : Thrust produced by the stage [Newtons]
# Output:
#   Thrust Structure mass [kg]
def Struct_Mass(Thrust):
    return 2.25*10**(-4)*Thrust


# Payload Fairing Mass
# Inputs:
#   A_fairing : Fairing surface area [m^2]
# Output:
#   Fairing mass [kg]
def M_fairing(A_fairing):
    return 4.95*A_fairing**1.15


# Avionics Mass
# Inputs:
#   Mo : Stage initial mass [kg]
# Output:
#   Avionics mass [kg]
def M_avionic(Mo):
    return 10*Mo**0.361


# Wiring Mass
# Inputs:
#   Mo : Stage initial mass [kg]
#   l  : Stage length [m]
# Output:
#   Wiring mass [kg]
def M_wiring(Mo, l):
    return 1.058*np.sqrt(Mo)*l**0.25


# Gimbal Mass
# Inputs:
#   Thrust : Thrust produced by the engine [Newtons]
#   Mixture: name of propellant mixture
#   Stage_number: stage 1 or stage 2
# Output:
#   Gimbal mass [kg]
def M_gimbals(Thrust, mixture, stage_number):

    if stage_number not in [1, 2]:
        raise ValueError('Stage number must be 1 or 2')
    
    Po = (Chamber_pressure_stage1[mixture] if stage_number == 1 
                       else Chamber_pressure_stage2[mixture])
    return 237.8*(Thrust/Po)**0.9375
