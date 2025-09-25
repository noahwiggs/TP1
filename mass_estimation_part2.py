

def mass_estimation(X, prop1, prop2):
    import numpy as np
    import matplotlib.pyplot as plt
    """
    Calculates relevant mass values for use in heuristics from stage 1 dV fraction, X
    
    Inputs:
    X (float): stage 1 dV fraction

    Outputs:
    m_pr_1 (float): mass of stage 1 propellant
    m_pr_2 (float): mass of stage 2 propellant
    m_0 (float): total mass of the LV  
    """
    #knowns
    dv_req = 12300 #m/s
    g_0 = 9.81 # m/s2
    m_pl_2 = 26000 # kg
    delta_1 = 0.08
    delta_2 = 0.08

    stage_1_dv = dv_req * (X / 100)
    stage_2_dv = dv_req * (1 - X/100)

    stage_mass(stage_1_dv, stage_2_dv, stage_1_Isp, stage)

def stage_mass(stage_1_dv, stage_2_dv)







