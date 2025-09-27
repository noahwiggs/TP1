import numpy as np

# Thrust(Newtons), Ae (m^2), At (m^2)
def Rocket_Engine(Thrust,Ae,At):
    return 7.81*10**(-4)*Thrust + 3.37*10**(-5)*Thrust*np.sqrt(Ae/At) + 59

# M_pr(Kilograms)
def Motor_Casing(M_pr):
    return 0.135*M_pr

# Thrust(Newtons)
def Struct_Mass(Thrust):
    return 2.25*10**(-4)*Thrust

# A_fairing (m^2)
def M_fairing(A_fairing):
    return 4.95*A_fairing**1.15

# Mo (Kilograms)
def M_avionic(Mo):
    return 10*Mo**0.361

# Mo (Kilograms)
def M_wiring(Mo,l):
    return 1.058*np.sqrt(Mo)*l**0.25

# Thrust(Newtons), Po (Pascals)
def M_gimbals(Thrust,Po):
    return 237.8*(Thrust/Po)**0.9375

