from typing import Tuple, Dict

def find_prop_mass_volume(
        propellant_mass: float, 
        oxidizer: str, 
        fuel: str, 
        mixture: str, 
        fuel_ratios: Dict[str, float],
        prop_density: Dict[str, float]
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

    Example Call:
    f_m, f_v, o_m, o_v = find_prop_mass_volume(
        propellant_mass = 10000,
        oxidizer = 'LOX',
        fuel = 'LH2',
        mixture = 'LOX_LH2',
        fuel_ratios = fuel_ratios,
        prop_densities = prop_densities
        )
    """
    # Start by determing the mass of the Oxidizer and fuel based on their ratio
    # If the ratio is 1, than we are using solids

    total_parts = fuel_ratios[mixture] + 1
    mass_per_part = propellant_mass / total_parts
    oxidizer_mass = mass_per_part * fuel_ratios[mixture]
    fuel_mass = mass_per_part

    # deterrmine volume of the fluids
    oxidizer_volume = oxidizer_mass / prop_density[oxidizer]
    fuel_volume = fuel_mass / prop_density[fuel]

    return oxidizer_mass, oxidizer_volume, fuel_mass, fuel_volume

def find_cyl_tank_dim(
        volume: float, 
        radius: float = 2.6, 
        height: float = 0, 
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

    Example Call:
        area, radius, height = find_cyl_tank_dim(
            volume = 100000,
            tank_amount = 6
            )
        Code will assume 2.6m for radius if no radius or height is provided
    """
    tank_surface_area = 0
    tank_radius = radius
    tank_height = height

    return tank_surface_area, tank_radius, tank_height