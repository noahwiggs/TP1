import propellant_tank_calculations as Calc
import Mass_functions as Mfunc
from dictionaries import (Isp_values,fuel_ratios,prop_densities)
import numpy as np
'''
Inputs: 

Prop                (Sting): Propellant Mixture
M_pr                (Float): Mass of Propellant
Num_Tank              (Int): Number of Propellant Tanks
tank_radius         (float): radius of the tank (m)
tank_height         (float): height of the tank (m)


Outputs: 
    M_Total (Float): Total mass of Casing/Tank/Insulation

'''




def Check_Solid_and_Storables(Prop: str,M_pr: float, tank_radius: float = 2.6, tank_height: float = np.nan, Num_Tank: int = 1):

    #Check if Solids
    if Prop =='Solids':
        Total_M = Num_Tank*Mfunc.Motor_Casing(M_pr/Num_Tank)

    elif Prop =='Storables':
        oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume = Calc.find_prop_mass_volume(M_pr,'Storables', 'Storables', 'Storables',fuel_ratios,prop_densities)
        Total_Volume = oxidizer_volume + fuel_volume
        Total_M =  Calc.find_tank_mass(Total_Volume, 'Storables', Num_Tank)

    else:
        Fuel = Prop[4:]

        oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume = Calc.find_prop_mass_volume(M_pr,'LOX', Fuel, Prop,fuel_ratios,prop_densities)
        Total_Volume = oxidizer_volume + fuel_volume
        Tank_Mass =  Calc.find_tank_mass(Total_Volume, 'Storables', Num_Tank)


        tank_surface_area, tank_radius, tank_height = Calc.find_cyl_tank_dim(Total_Volume, tank_radius, tank_height, Num_Tank)

        Insulation_mass = Calc.find_insulation_mass(tank_surface_area,Num_Tank,Prop)

        Total_M = Tank_Mass + Insulation_mass


    return Total_M, tank_radius, tank_height
