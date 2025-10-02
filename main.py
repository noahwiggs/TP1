import mass_estimation_part2 as me2
import Mass_functions as Mfunc
from Check_Solid_and_Storables import Check_Solid_and_Storables
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

    """

    """
    --------------------------------
    | DEFINE YOUR ROCKET PROPERTIES|
    --------------------------------

     Valid mixture names:
        LOX_LH2
        LOX_LCH4
        LOX_RP1
        Solids
        Storables
    """
    X = 0.5 #
    s1_mixture = 'LOX_LH2'
    s2_mixture = 'Storables'
    tank_amount = 1
    
    # start by finding part 1 values, gross and propellant mass of each stage
    m_pr_1, m_pr_2, m_0, m_0_2 = me2.mass_estimation(
        X, 
        s1_mixture, 
        s2_mixture, 
        Isp_values)
    
    # determine tank/insulation/casing properties

    s1_t_n_insul_m, s1_t_r, s1_t_h = Check_Solid_and_Storables(s1_mixture, m_pr_1)
    s2_t_n_insul_m, s2_t_rm, s2_t_h = Check_Solid_and_Storables(s2_mixture, m_pr_2)

    # determine mass of other elements

    # TODO: 
    # fairing_mass = Mfunc.M_fairing(A_fairing)
    avionic_mass = Mfunc.M_avionic(m_0)

    # TODO : 
    # rocket_height = ...
    # wiring_mass = Mfunc.M_wiring(m_0, rocket_height)
    
    






if __name__ == '__main__':
    main()