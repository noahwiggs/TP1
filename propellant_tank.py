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
    fuel (string): type of fuel
    oxidizer (string): type of oxidizer
    mixture (string): fuel to oxidizer ratio
    fuel_ratios (Dict(str, float)) : dictionary containing mixture ratio oxidizer:fuel
    prop_density (Dict(str, float)): dictionary containing propellant densities (kg/m3)

    Output: 
    fuel_mass (float): mass of fuel
    fuel_volume (foat): volume of fuel
    oxidizer_mass (float): mass of oxidizer
    oxodizer_volume (float): volume of oxidizer

    --------------------
    Code takes propellant mass, uses the mixture ratio (weight) to find
    the mass of the fuel and oxidizer.
    Then find the volume of the fuel and oxidizer using its density

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