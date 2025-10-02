import propellant_tank_calculations as Calcs
import Mass_functions as Mfunc
import numpy as np
from typing import Tuple, Dict


'''
Determine tank/casing/insulation mass for different propellant types.

Behavior:
    - If Prop == 'Solids':
        Use Motor_Casing() to estimate casing mass for solid motors.
        Computes cylindrical Casing geometry.
        Assumes solid propellant is inside a motor casing (no separate tanks/insulation).
    - If Prop == 'Storables':
        Storables are liquid propellants that are storable at ambient temperature/pressure.
        Uses find_prop_mass_volume() to split M_pr into oxidizer/fuel masses & volumes, 
        computes cylindrical tank geometry, sums volumes and calls find_tank_mass() 
        to size tanks and return tank mass.
    - Else (assume bipropellant with LOX oxidizer and specified fuel):
        The code slices Prop[4:] to extract the fuel name for combinations like 'LOXRP1'
        It computes oxidizer+fuel masses and volumes, estimates tank mass (using Storables type
        as the tank type for mass Calcsulation), computes cylindrical tank geometry, then
        estimates insulation mass and returns Tank + Insulation mass.

Returns:
    (Total_M, tank_radius, tank_height)
    
'''

def Check_Solid_and_Storables(
        Prop            : str, 
        M_pr            : float,
        fuel_ratios     : Dict[str, float],
        prop_densities  : Dict[str, int],
        tank_radius     : float = 2.6, 
        tank_height     : float = np.nan, 
        Num_Tank        : int = 1,

    )-> Tuple[float, float, float]:

    '''
    Inputs: 
        Prop                (String): Propellant Mixture (e.g. 'LOXRP1', 'Storables', 'Solids')
        M_pr                (Float) : Total mass of propellant (kg)
        Num_Tank            (Int)   : Number of identical tanks to split propellant across
        tank_radius         (Float) : Preferred tank radius (m). If tank_height is NaN, Calcs.find_cyl_tank_dim can compute height.
        tank_height         (Float) : Preferred tank height (m). If NaN, Calcs.find_cyl_tank_dim can compute height.

    Outputs: 
        tank_total_mass             (Float) : Total mass of casing/tank/insulation (kg)
        tank_radius         (Float) : Final tank radius used (m)
        tank_height         (Float) : Final tank height used (m)
    '''

    # Check for valid propellant name
    if Prop not in [
        'LOX_LH2'
        'LOX_LCH4'
        'LOX_RP1'
        'Solids'
        'Storables']:
        raise ValueError('Invalid mixture name, check naming convention in main')
    
    #Check if Solids
    if Prop == 'Solids':
        # Solids only has casing mass
        tank_total_mass = Num_Tank*Mfunc.Motor_Casing(M_pr/Num_Tank)

    #Check if Storables
    elif Prop == 'Storables':
        # Storables does not need insulation
        oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume = Calcs.find_prop_mass_volume(
            M_pr,
            'Storables',
            'Storables',
            'Storables',
            fuel_ratios,
            prop_densities
        )
        Total_Volume = oxidizer_volume + fuel_volume
        tank_surface_area, tank_radius, tank_height = Calcs.find_cyl_tank_dim(
            Total_Volume,
            tank_radius,
            tank_height,
            Num_Tank
        )

        tank_total_mass = Calcs.find_tank_mass(Total_Volume, 'Storables', Num_Tank)

    else:
        Fuel = Prop[4:]

        oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume = Calcs.find_prop_mass_volume(
            M_pr,
            'LOX',
            Fuel,
            Prop,
            fuel_ratios,
            prop_densities
        )
        
        Total_Volume = oxidizer_volume + fuel_volume
        tank_surface_area, tank_radius, tank_height = Calcs.find_cyl_tank_dim(
            Total_Volume,
            tank_radius,
            tank_height,
            Num_Tank
        )

        Insulation_mass = Calcs.find_insulation_mass(
            tank_surface_area,
            Num_Tank,
            Prop
        )
        Tank_Mass = Calcs.find_tank_mass(Total_Volume, 'Storables', Num_Tank)
        
        tank_total_mass = Tank_Mass + Insulation_mass


    return tank_total_mass, tank_radius, tank_height
