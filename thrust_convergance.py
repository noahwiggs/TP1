from typing import Tuple
import math

import Mass_functions as mf


# remove when done
from dictionaries import Thrust_stage1, Thrust_stage2
# Initial thrust to weight ratio of >= 1.3 for stage 1
# Initial thrust to weight ratio of >= 0.76 for subsequent stages


# Start with total weight to find required thrust - Use numbers from section 1

# Use required thrust to find 

g_0 = 9.81
T_W_req_stage_1 = 1.3
T_W_req_stage_2 = 0.76


"""
Process:
    - Start with the initial mass values found in section 1, will want total mass,
    mass of stage 1, propellant mass of stage 1, mass of stage 2, propellant mass of stage 2
    NOTE: Don't forget payload masses

    - Use total weight of each stage to find the required thrust at each stage
    - Use thrust at each stage to determine the number of engines required
    - Use these values to calculate the mass of the rocket engines, thrust structure,
    and the mass of the gimbals.

    - Use these masses, along with the masses we found 
"""

def thrust_component_mass(
        stage_1_gross_mass: float,
        stage_2_gross_mass: float,
        stage_1_mixture: str,
        stage_2_mixture: str,
    )-> Tuple[float, float]:
    """
    Inputs:
    stage_1_mass (float): the total mass of stage 1, (gross mass)) (kg)
    stage_2_mass (float): the total mass of stage 2

    stage_1_mixture (str): name of stage 1 mixture
    stage_2_mixture (str): name of stage 2 mixture

    Outputs:


    """

    # Initial values
    # find thrust required
    stage_1_thrust_req = T_W_req_stage_1 * g_0 * stage_1_gross_mass
    stage_2_thrust_req = T_W_req_stage_2 * g_0 * stage_2_gross_mass

    # find number of engines required
    stage_1_engine_count = math.ceil(stage_1_thrust_req / Thrust_stage1[stage_1_mixture])
    stage_2_engine_count = math.ceil(stage_2_thrust_req / Thrust_stage2[stage_2_mixture])

    # find thrust per engine
    stage_1_tpe = stage_1_thrust_req / stage_1_engine_count
    stage_2_tpe = stage_2_thrust_req / stage_2_engine_count

    # find total engine mass
    stage_1_total_engine_mass = stage_1_engine_count * mf.Rocket_Engine(stage_1_tpe, stage_1_mixture, 1)
    stage_2_total_engine_mass = stage_2_engine_count * mf.Rocket_Engine(stage_2_tpe, stage_2_mixture, 2)

    # find thrust structure mass
    stage_1_thrust_struct_mass = mf.Struct_Mass(stage_1_thrust_req)
    stage_2_thrust_struct_mass = mf.Struct_Mass(stage_2_thrust_req)

    # find gimbal mass
    stage_1_gimbal_mass = mf.M_gimbals(stage_1_thrust_req, stage_1_mixture, 1)
    stage_2_gimbal_mass = mf.M_gimbals(stage_2_thrust_req, stage_2_mixture, 2)

    # recalculate total mass of stage 1 and stage 2



    a = 0.1
    b = 0.2


    return a, b