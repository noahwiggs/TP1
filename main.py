import mass_estimation_part2 as me2
import Mass_functions as Mfunc
import thrust_convergance as tc
import Check_Solid_and_Storables as css
import Fairing_area as fa
import export_fn as exp

import numpy as np
import pandas as pd

from dictionaries import (
    Isp_values,
    Thrust_stage1,
    Thrust_stage2,
    Expansion_ratio_stage1,
    Expansion_ratio_stage2,
    Chamber_pressure_stage1,
    Chamber_pressure_stage2,
    fuel_ratios,
    prop_densities
)

def main():
    """
    General workflow:
    1) Feed in X for each prop mix in a for loop
    2) Estimate required masses for heuristics
    3) Calculate heuristics
    4) Produce mass budget for each

    Valid mixture names:
        LOX_LH2
        LOX_LCH4
        LOX_RP1
        Solids
        Storables
    """

    ## Inputs
    X = 0.5 
    s1_prop_mix = 'LOX_LH2'
    s2_prop_mix = 'Storables'
    tank_amount = 1
    
    ## start by finding part 1 values, gross and propellant mass of each stage
    m_pr_1, m_pr_2, m_0, m_0_2 = me2.mass_estimation(X, s1_prop_mix, s2_prop_mix, Isp_values)
    
    ## determine tank/insulation/casing properties
    
    preferred_radius_1 = 2.6 #units?
    preferred_height_1 = np.nan
    preferred_radius_2 = 2.6 #units?
    preferred_height_2 = np.nan

    s1_tank_insul_combined_mass, s1_tank_radius, s1_tank_height, s1_tank_mass, s1_insul_mass = css.Check_Solid_and_Storables(s1_prop_mix, m_pr_1, preferred_height_1, preferred_radius_1)
    s2_tank_insul_combined_mass, s2_tank_radius, s2_tank_height, s2_tank_mass, s2_insul_mass = css.Check_Solid_and_Storables(s2_prop_mix, m_pr_2, preferred_height_2, preferred_radius_2)

    ## determine mass of other elements

    # determine fairing mass using surface area
    # fairing_area = fa.fairing_area_cone(s1_t_r,s1_t_h,s2_t_r,s2_t_h)
    a = 6 #physical meaning?
    b = 2.6 #physical meaning?
    fairing_area = fa.fairing_area_ellipsoid(a, b)
    fairing_mass = Mfunc.M_fairing(fairing_area)

    avionic_mass = Mfunc.M_avionic(m_0)

    # TODO : 
    stage_1_length = 1
    wiring_mass = Mfunc.M_wiring(m_0, stage_1_length)

    # find thrust required
    # TODO: Find other masses
    # stage_1_other_masses = ...
    # stage_2_other_masses = ...
    # t_req1, t_req2 = tc.thrust_convergance(m_0, m_0_2, m_pr_1, m_pr_2, m_pl, stage_1_other_masses, stage_2_other_masses, s1_prop_mix, s2_prop_mix)

    # find total rocket mass from thrust
    # s1_m_0, s2_m_0, X = tc.thrust_mass_calculations(m_pr_1, m_pr_2, m_pl, stage_1_other_masses, stage_2_other_masses, t_req1, t_req2, s1_prop_mix, s2_prop_mix)
    
    # mass margin
    # s1_m_0 *= 1.3
    # s2_m_2 *= 1.3

    # TODO: calculate all inert masses

    # TODO: calculate cost

    # TODO: find inert mass fraction

    ## Output results to csv table
    
    compiled_masses = [
    (m_pr_1+m_pr_2),  # Propellant
    ,  # Propellant tanks
    ,  # Propellant tank insulation
    ,  # Engines
    ,  # Thrust structure
    ,  # Casing (only solid, 0 for liquid)
    ,  # Gimbals
    ,  # Avionics
    ,  # Wiring
    ,  # Payload fairing
    ,  # Inter-tank fairing
    ,  # Inter-stage fairing
       # Aft fairing
    ]

    exp.export(compiled_masses)


if __name__ == '__main__':
    main()