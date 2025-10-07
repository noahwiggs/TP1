from typing import Tuple, Dict
import math

import Mass_functions as Mfunc

from dictionaries import(
     Thrust_stage1,
     Thrust_stage2,
     Expansion_ratio_stage1,
     Expansion_ratio_stage2,
     Chamber_pressure_stage1,
     Chamber_pressure_stage2
)


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

def thrust_convergance(
        stage_1_gross_mass      : float,
        stage_2_gross_mass      : float,
        m_pr_1                  : float,
        m_pr_2                  : float,
        m_pl                    : float,
        stage_1_other_masses    : float,
        stage_2_other_masses    : float,
        stage_1_mixture         : str,
        stage_2_mixture         : str,
    )-> Tuple[float, float]:
    """
    Inputs:
        stage_1_gross_mass    (float): gross mass calculation from part 1,
        stage_2_gross_mass    (float): gross mass calculation from part 1,
        m_pr_1                (float): propellant mass calculation from part 1,
        m_pr_2                (float): propellant mass calculation from part 1,
        m_pl                  (float): required payload mass,
        stage_1_other_masses  (float): masses calculated in this section,
        stage_2_other_masses  (float): masses calculated in this section,
        stage_1_mixture       (str)  : name of mixture
        stage_2_mixture       (str)  : name of mixture

    Outputs:
        stage_1_thrust_req (float): the required thrust for stage 1
        stage_2_thrust_req (float): the required thrust for stage 2

    This function calculates the thrust required, finds mass of components required to meet the thrust,
    updates the new thrust required based off updated mass and iterates until we converge upon a required thrust
    """

    # Initial values
    # find thrust required
    stage_1_thrust_req = T_W_req_stage_1 * g_0 * stage_1_gross_mass * 1.3
    stage_2_thrust_req = T_W_req_stage_2 * g_0 * stage_2_gross_mass * 1.3

    tolerance = 1e-3
    thrust_dif_1 = 100
    thrust_dif_2 = thrust_dif_1

    iterations = 0

    # iterate to find convergence
    while iterations < 1000:
        # store/update previous values
        stage_1_thrust_req_0 = stage_1_thrust_req
        stage_2_thrust_req_0 = stage_2_thrust_req

        # obtain new gross masses
        stage_1_gross_mass, stage_2_gross_mass, _ = thrust_mass_calculations(
            m_pr_1,
            m_pr_2,
            m_pl,
            stage_1_other_masses,
            stage_2_other_masses,
            stage_1_thrust_req, 
            stage_2_thrust_req,
            stage_1_mixture,
            stage_2_mixture,
        )

        # use new gross masses to calculate new thrust required
        stage_1_thrust_req = T_W_req_stage_1 * g_0 * stage_1_gross_mass * 1.3
        stage_2_thrust_req = T_W_req_stage_2 * g_0 * stage_2_gross_mass * 1.3

        # check the difference between previous thrust required and new thrust required
        thrust_dif_1 = abs(stage_1_thrust_req - stage_1_thrust_req_0) / stage_1_thrust_req_0
        thrust_dif_2 = abs(stage_2_thrust_req - stage_2_thrust_req_0) / stage_2_thrust_req_0
        # dividing by previous thrust req so we are considering percent change bc of large numbers

        # if within tolerance break, we found the required thrust
        if thrust_dif_1 < tolerance and thrust_dif_2 < tolerance:
            # Print final engine counts after convergence
            stage_1_engine_count = math.ceil(stage_1_thrust_req / Thrust_stage1[stage_1_mixture])
            stage_2_engine_count = math.ceil(stage_2_thrust_req / Thrust_stage2[stage_2_mixture])
            print(f'Stage 1 engine count: {stage_1_engine_count}')
            print(f'Stage 2 engine count: {stage_2_engine_count}')
            print('----------------------------------------')
            print(f'Stage 1 thrust: {stage_1_thrust_req/1000:.3f} (Kilo-Newtons)')
            print(f'Stage 2 thrust: {stage_2_thrust_req/1000:.3f} (Kilo-Newtons)')
            print(f'Stage 1 thrust weight ratio: {stage_1_thrust_req/(stage_1_gross_mass*9.81):.3f} ')
            print(f'Stage 2 thrust weight ratio: {stage_2_thrust_req/(stage_2_gross_mass*9.81):.3f} ')
            break

        iterations += 1


    return stage_1_thrust_req, stage_2_thrust_req

def thrust_mass_calculations(
        m_pr_1                  : float,
        m_pr_2                  : float,
        m_pl                    : float,
        stage_1_other_masses    : float,
        stage_2_other_masses    : float,
        stage_1_thrust_req      : float, 
        stage_2_thrust_req      : float,
        stage_1_mixture         : str,
        stage_2_mixture         : str,
        )-> Tuple[float, float, list[float]]:
    """
    Inputs:
        m_pr_1                  (float) : propellant mass,
        m_pr_2                  (float) : propellant mass,
        m_pl                    (float) : payload mass,
        stage_1_other_masses    (float) : masses found in part 2,
        stage_2_other_masses    (float) : masses found in part 2,
        stage_1_thrust_req      (float) : thrust for stage 1, 
        stage_2_thrust_req      (float) : thrust for stage 2,
        stage_1_mixture         (str)   : stage 1 mixture name,
        stage_2_mixture         (str)   : stage 2 mixture name

    Outputs:
        stage_1_total_mass      (float) : total mass of stage 1
        stage_2_total_mass      (float) : total mass of stage 2
        X                   list(float) : list of masses from each component


    This code finds the masses of components that depend 
    on thrust and then sums the total mass of each stage.
    """
    # find number of engines required
    stage_1_engine_count = math.ceil(stage_1_thrust_req / Thrust_stage1[stage_1_mixture])
    stage_2_engine_count = math.ceil(stage_2_thrust_req / Thrust_stage2[stage_2_mixture])

    # find thrust per engine
    stage_1_tpe = stage_1_thrust_req / stage_1_engine_count
    stage_2_tpe = stage_2_thrust_req / stage_2_engine_count

    # find total engine mass
    stage_1_total_engine_mass = stage_1_engine_count * Mfunc.Rocket_Engine(stage_1_tpe, stage_1_mixture, Expansion_ratio_stage1)
    stage_2_total_engine_mass = stage_2_engine_count * Mfunc.Rocket_Engine(stage_2_tpe, stage_2_mixture, Expansion_ratio_stage2)

    # find thrust structure mass
    stage_1_thrust_struct_mass = Mfunc.Struct_Mass(stage_1_thrust_req)
    stage_2_thrust_struct_mass = Mfunc.Struct_Mass(stage_2_thrust_req)

    # find gimbal mass
    stage_1_gimbal_mass = Mfunc.M_gimbals(stage_1_thrust_req, stage_1_mixture, Chamber_pressure_stage1)
    stage_2_gimbal_mass = Mfunc.M_gimbals(stage_2_thrust_req, stage_2_mixture, Chamber_pressure_stage2)

    # recalculate total mass of stage 1 and stage 2
    # does stage_2_other_masses include payload? if so remove from line under
    stage_2_total_mass = m_pr_2 + stage_2_other_masses + stage_2_total_engine_mass + stage_2_gimbal_mass + stage_2_thrust_struct_mass + m_pl
    stage_1_total_mass = m_pr_1 + stage_1_other_masses + stage_1_total_engine_mass + stage_1_gimbal_mass + stage_1_thrust_struct_mass + stage_2_total_mass

    X = [stage_1_total_engine_mass, stage_2_total_engine_mass, stage_1_thrust_struct_mass, stage_2_thrust_struct_mass, stage_1_gimbal_mass, stage_2_gimbal_mass]

    return stage_1_total_mass, stage_2_total_mass, X