import numpy as np


# Rocket Engine Mass
# Inputs:
#   Thrust : Thrust produced by the engine [Newtons]
#   Ae     : Exit area of nozzle [m^2]
#   At     : Throat area of nozzle [m^2]
# Output:
#   Mass of rocket engine [kg]
def Rocket_Engine(Thrust, Ae, At):
    return 7.81*10**(-4)*Thrust + 3.37*10**(-5)*Thrust*np.sqrt(Ae/At) + 59


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
#   Po     : Chamber pressure [Pascals]
# Output:
#   Gimbal mass [kg]
def M_gimbals(Thrust, Po):
    return 237.8*(Thrust/Po)**0.9375
