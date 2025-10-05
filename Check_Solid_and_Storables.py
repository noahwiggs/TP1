import propellant_tank_calculations as Calcs
import Mass_functions as Mfunc
import numpy as np
from typing import Tuple

from dictionaries import fuel_ratios, prop_densities


'''
Determine tank/casing/insulation mass for different propellant types.

Behavior:
    - If mixture == 'Solids':
        Use Motor_Casing() to estimate casing mass for solid motors.
        Computes cylindrical Casing geometry.
        Assumes solid propellant is inside a motor casing (no separate tanks/insulation).
    - If mixture == 'Storables':
        Storables are liquid propellants that are storable at ambient temperature/pressure.
        Uses find_prop_mass_volume() to split M_pr into oxidizer/fuel masses & volumes, 
        computes cylindrical tank geometry, sums volumes and calls find_tank_mass() 
        to size tanks and return tank mass.
    - Else (assume bipropellant with LOX oxidizer and specified fuel):
        The code slices mixture[4:] to extract the fuel name for combinations like 'LOXRP1'
        It computes oxidizer+fuel masses and volumes, estimates tank mass (using Storables type
        as the tank type for mass Calcsulation), computes cylindrical tank geometry, then
        estimates insulation mass and returns Tank + Insulation mass.

Returns:
    (Total_M, tank_radius, tank_height)
    
'''

def Check_Solid_and_Storables(
        mixture            : str, 
        M_pr            : float,
        tank_radius     : float = 2.6, 
        tank_height     : float = np.nan, 
        Num_Tank        : int = 1,

    )-> Tuple[float, float, float, float]:

    '''
    Inputs: 
        mixture             (String): Propellant Mixture (e.g. 'LOXRP1', 'Storables', 'Solids')
        M_pr                (Float) : Total mass of propellant (kg)
        Num_Tank            (Int)   : Number of identical tanks to split propellant across
        tank_radius         (Float) : Preferred tank radius (m). If tank_height is NaN, Calcs.find_cyl_tank_dim can compute height.
        tank_height         (Float) : Preferred tank height (m). If NaN, Calcs.find_cyl_tank_dim can compute height.

    Outputs: 
        tank_radius         (Float) : Final tank radius used (m)
        tank_height         (Float) : Final tank height used (m)
        Tank_Mass           (Float) : Total tank/casing mass
        Insulation_Mass     (Float) : Total insulation mass
    '''

    # Check for valid propellant name
    if mixture not in [
        'LOX_LH2',
        'LOX_LCH4',
        'LOX_RP1',
        'Solid',
        'Storables']:
        raise ValueError('Invalid mixture name, check naming convention in dictionary')
    
    # set as needed
    oxidizer_tank_count = 1
    fuel_tank_count = 1

    
    #Check if Solids
    if mixture == 'Solid':
        # set based off number of solid rocket motors needed
        num_of_casing = 1

        # Solids only has casing mass
        _, solid_volume, _, _ = Calcs.find_prop_mass_volume(
            M_pr,
            'Solid',
            'Solid',
            'Solid',
        )

        # find dimensions
        _, casing_radius, casing_height = Calcs.find_cyl_tank_dim(
            solid_volume, 
            radius=tank_radius, 
            height=tank_height, 
            tank_amount=num_of_casing
        )

        # prepare return values
        Tank_Mass = Num_Tank*Mfunc.Motor_Casing(M_pr/Num_Tank)
        Insulation_mass = 0
        tank_radius = casing_radius
        total_height = casing_height

    #Check if Storables
    elif mixture == 'Storables':

        # Storables does not need insulation
        # find oxidizer/fuel volume
        _, oxidizer_volume, _, fuel_volume = Calcs.find_prop_mass_volume(
            M_pr,
            'Storables',
            'Storables',
            'Storables',
        )

        # dimensions
        oxi_sur_A, oxi_r, oxi_h     = Calcs.find_cyl_tank_dim(
            oxidizer_volume, 
            radius=tank_radius, 
            height=tank_height, 
            tank_amount=oxidizer_tank_count
        )
        fuel_sur_A, _, fuel_h  = Calcs.find_cyl_tank_dim(
            fuel_volume, 
            radius=tank_radius, 
            height=tank_height, 
            tank_amount=fuel_tank_count
        )

        # find tank masses
        oxi_tank_mass = Calcs.find_tank_mass(oxidizer_volume, 'Storables', tank_amount=oxidizer_tank_count)
        fuel_tank_mass = Calcs.find_tank_mass(fuel_volume, 'Storables', tank_amount=fuel_tank_count)

        # prepare return values
        Tank_Mass = oxi_tank_mass + fuel_tank_mass
        Insulation_mass = 0
        total_height = oxi_h + fuel_h
        tank_radius = oxi_r

    else:
        # prepare strings
        Fuel = mixture.split('_')[1]
        Oxidizer = 'LOX'

        # find oxidizer/fuel volume
        _, oxidizer_volume, _, fuel_volume = Calcs.find_prop_mass_volume(
            M_pr,
            Oxidizer,
            Fuel,
            mixture,
        )

        # dimensions
        oxi_sur_A, oxi_r, oxi_h = Calcs.find_cyl_tank_dim(
            oxidizer_volume, 
            radius=tank_radius, 
            height=tank_height, 
            tank_amount=oxidizer_tank_count
        )
        fuel_sur_A, _, fuel_h = Calcs.find_cyl_tank_dim(
            fuel_volume, 
            radius=tank_radius, 
            height=tank_height, 
            tank_amount=fuel_tank_count
        )

        # find masses
        oxi_tank_mass = Calcs.find_tank_mass(oxidizer_volume, Oxidizer, tank_amount=oxidizer_tank_count)
        fuel_tank_mass = Calcs.find_tank_mass(fuel_volume, Fuel, tank_amount=fuel_tank_count)

        oxi_insul_mass = Calcs.find_insulation_mass(oxi_sur_A, Num_Tank, Oxidizer)
        fuel_insul_mass = Calcs.find_insulation_mass(fuel_sur_A, fuel_tank_count, Fuel)

        Tank_Mass = oxi_tank_mass + fuel_tank_mass
        Insulation_mass = oxi_insul_mass + fuel_insul_mass

        # prepare return values
        tank_radius = oxi_r
        total_height = oxi_h + fuel_h


    return tank_radius, total_height, Tank_Mass, Insulation_mass
