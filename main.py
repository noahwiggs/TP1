import mass_estimation_part2 as me2
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
    stage_1_mixture = 'LOX_LH2'
    stage_2_mixture = 'Storables'
    
    m_pr_1, m_pr_2, m_0, m_0_2 = me2.mass_estimation(
        X, 
        stage_1_mixture, 
        stage_2_mixture, 
        Isp_values)
    
    





if __name__ == '__main__':
    main()