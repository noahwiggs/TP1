from typing import Tuple, Dict
import numpy as np
from scipy.optimize import fsolve

def find_prop_mass_volume(
        propellant_mass: float, 
        oxidizer: str, 
        fuel: str, 
        mixture: str, 
        fuel_ratios: Dict[str, float],
        prop_densities: Dict[str, float]
    ) -> Tuple[float, float, float, float]:
    """
    Input:
    propellant_mass (float): total propellant mass (kg)
    oxidizer        (string): type of oxidizer
    fuel            (string): type of fuel
    mixture         (string): fuel to oxidizer ratio
    fuel_ratios     (Dict(str, float)): dictionary containing mixture ratio oxidizer:fuel
    prop_densities  (Dict(str, float)): dictionary containing propellant densities (kg/m3)

    Output: 
    fuel_mass       (float): mass of fuel
    fuel_volume     (float): volume of fuel
    oxidizer_mass   (float): mass of oxidizer
    oxodizer_volume (float): volume of oxidizer

    --------------------
    Code takes propellant mass, uses the mixture ratio (weight) to find
    the mass of the fuel and oxidizer.
    Then find the volume of the fuel and oxidizer using its density

    Usage Examples:
        # Generic Propellant
        f_m, f_v, o_m, o_v = find_prop_mass_volume(
            propellant_mass = 10000,
            oxidizer = 'LOX',
            fuel = 'LH2',
            mixture = 'LOX_LH2',
            fuel_ratios = fuel_ratios,
            prop_densities = prop_densities
            )

        # Storables
        f_m, f_v, o_m, o_v = find_prop_mass_volume(
            propellant_mass = 10000,
            oxidizer = 'Storables',
            fuel = 'Storables',
            mixture = 'Storables',
            fuel_ratios = fuel_ratios,
            prop_densities = prop_densities
            )

    """
    # Manage Storables naming
    if mixture == 'Storables':
        oxidizer = 'N2O4'
        fuel = 'UDMH'

    total_parts = fuel_ratios[mixture] + 1

    mass_per_part = propellant_mass / total_parts
    oxidizer_mass = mass_per_part * fuel_ratios[mixture]
    fuel_mass = mass_per_part

    # deterrmine volume of the fluids
    oxidizer_volume = oxidizer_mass / prop_densities[oxidizer]
    fuel_volume = fuel_mass / prop_densities[fuel]

    return oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume

def find_cyl_tank_dim(
        volume: float, 
        radius: float = 2.6, 
        height: float = np.nan, 
        tank_amount: int = 1
    ) -> Tuple[float, float, float]:
    """
    Input:
    volume      (float): volume of the propellant   (m3)
    radius      (float): radius of the tank         (m)
    height      (float): height of the tank         (m)
    tank_amount (int)  : number of tanks

    Return:
    tank_surface_area   (float): surface area of the tank (m2)
    tank_radius         (float): radius of the tank (m)
    tank_height         (float): height of the tank (m)
    --------------------
    This code calculates the dimensions (area, radius, height) of a cylindrical
    propallent tank.
    This code assumes a cylindrical tank with hemispherical end caps
    NOTE: Tank height includes radius of hemispherical end caps

    There are three ways to use this code:
    1) Find height of tank given/assuming constant radius
        ie. find_cyl_tank_dim(100000)

        The function will attempt to find required height of the prop tank
        assuming a radius of 2.6m. This value comes from the required radius of the faring
    
        or. find_cyl_tank_dim(100000, 4)
        The funciton will attempt to find the required height of the prop tank
        with a radius of 4m


    2) Find the radius of the tank given a height
        ie. find_cyl_tank_dim(volume = 100000, height = 100)
        
        The function will attempt to find the required radius of the prop tank
        with a height of 100m


    3) Variable number of tanks
        You can also vary the number of tanks being used, ie 3 tanks for oxidizer
        The function assumes every tank has the same dimensions and will provide
        the dimensions of one tank.

        Radius of one tank, height of one tank, surface area of one tank.


    ==============================
    ** IMPORTANT **:
    NOTE: DIMENSIONS ARE PER TANK
    ==============================

    Example Call:
        area, radius, height = find_cyl_tank_dim(
            volume = 100000,
            tank_amount = 6
            )
        Code will assume 2.6m for radius if no radius or height is provided
    """
    
    # Determine number of tanks
    if not isinstance(tank_amount, int) or tank_amount < 1:
        raise ValueError('Tank amount must be a positive integer')

    volume = volume / tank_amount

    # find height
    if np.isnan(height):
        a_sphere = 4 * np.pi * radius**2
        v_sphere = (4/3) * np.pi * radius**3
        v_cyl = volume - v_sphere
        tank_height = v_cyl / (np.pi * radius**2) + 2 * radius
        tank_radius = radius
    else:
        # find radius
        def volume_eqn(r):
            cyl_height = height - 2 * r
            return np.pi * r**2 * cyl_height + (4/3) * np.pi * r**3 - volume
        
        radius_guess = 1
        tank_radius = fsolve(volume_eqn, radius_guess)[0]
        tank_height = height
        
    # find surface area

    tank_surface_area = 4 * np.pi * tank_radius**2 + 2 * np.pi * tank_radius * (tank_height - tank_radius)


    return tank_surface_area, tank_radius, tank_height

def find_tank_mass(
        tank_volume: float,
        propellant: str = '',
        tank_amount: int = 1
    ) -> float:
    """
    Inputs:
    tank_volume (float): volume of the tank (m3)
    propellant  (str)  : name of the propellant
    tank_amount (int)  : number of tanks

    Output:
    total_tank_mass   (float): mass of the tank (kg)
    ----------
    Given the volume of the propellant, find the mass of the propellant tanks

    NOTE: If the propellant is LH2, you need to let the function know

    Usage Examples: 
        # Generic Propellant
        tank_m = find_tank_mass(10000, tank_amount = 6)

        # LH2
        tank_m = find_tank_mass(10000, 'LH2') 
    """

    propellant = propellant.upper()
    if propellant not in ['LH2', '']:
        raise ValueError('Unsupported Propellant type, use LH2 or leave blank')
    if not isinstance(tank_amount, int) or tank_amount < 1:
        raise ValueError('Tank amount must be positive integer (defaults to 1)')
    
    total_tank_mass = 9.09 * tank_volume if propellant == 'LH2' else 12.16 * tank_volume

    total_tank_mass *= tank_amount
    return total_tank_mass


def find_insulation_mass(
        tank_area: float, 
        tank_amount: int = 1, 
        propellant: str = ''
    ) -> float:
    """
    Input:
    tank_area   (float): surface area of the tank
    tank_amount (int)  : number of tanks
    propellant  (str)  : type of propellant

    Output:
    total_insulation_mass (float): total mass of the insulation:

    ----------
    Given tank area and number of tanks, find the total mass of the insulation.
    NOTE: If the proopellant is LH2, you need to let the function know

    Usage Examples:
        # Generic Propellant
        total_insulation_m = find_insulation_mass(10000)
        # Generic Propellant 3 tanks
        total_insulation_m = find_insulation_mass(10000, 3)
        # LH2
        total_insulation_m = find_insulation_mass(10000, propellant = 'LH2')
    """
    propellant = propellant.upper()
    if propellant not in ['LH2', '']:
        raise ValueError('Unsupported Propellant type, use LH2 or leave blank')
    if not isinstance(tank_amount, int) or tank_amount < 1:
        raise ValueError('Tank amount must be positive integer (defaults to 1)')

    total_insulation_mass = 2.88 * tank_area if propellant == 'LH2' else 1.123 * tank_area

    total_insulation_mass *= tank_amount 

    return total_insulation_mass