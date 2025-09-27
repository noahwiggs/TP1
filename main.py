import mass_estimation_part2 as me
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
    #Assumed or fixed vehicle properties
    X = 0.1 #
    prop1 = 1
    prop2 = 1

    m_pr_1, m_pr_2, m_0 = me.mass_estimation(X, prop1, prop2)


if __name__ == '__main__':
    main()