from typing import Tuple, Dict

def mass_estimation(
        X           : float,
        mixture_1   : str,
        mixture_2   : str,
        Isp_values  : Dict[str, int]
        )-> Tuple[float, float, float, float]:
    import numpy as np
    import matplotlib.pyplot as plt
    """
    Calculates relevant mass values for use in heuristics from stage 1 dV fraction, X
    
    Inputs:
    X           (float) : stage 1 dV fraction
    mixture_1   (string): stage 1 Propellant Mixture
    mixture_2   (string): stage 2 Propellant Mixture


    Outputs:
    m_pr_1  (float): mass of stage 1 propellant
    m_pr_2  (float): mass of stage 2 propellant
    m_0     (float): total mass of the LV 
    m_0_2  (float): total mass of stage 2

    Using the stage 1 delta V fraction, find the gross mass 
    """
    #knowns
    dv_req = 12300 #m/s
    g_0 = 9.81 # m/s2
    m_pl_2 = 26000 # kg
    delta_1 = 0.08
    delta_2 = 0.08

    stage_1_dv = dv_req * (X / 100)
    stage_2_dv = dv_req * (1 - X/100)

    stage_1_Isp = Isp_values[mixture_1]
    stage_2_Isp = Isp_values[mixture_2]


    ## Stage 2
    #Find mass ratio
    frac = stage_2_dv / (g_0 * stage_2_Isp)
    r_2 = np.exp(-frac)

    #Find payload fraction from parametric mass ratio
    payload_fraction = r_2 - delta_2

    #Find total mass of stage
    m_0_2 = m_pl_2 / payload_fraction

    #This is the total mass of stage 2 and the payload mass of stage 1
    m_pl_1 = m_0_2

    #Find inert and propellant mass
    m_in_2 = delta_2 * m_0_2
    m_pr_2 = m_0_2 - m_in_2 - m_pl_2

    ## Stage 1
    frac = stage_1_dv / (g_0 * stage_1_Isp)
    r_1 = np.exp(-frac)

    # Find payload fraction
    payload_fraction = r_1 - delta_1

    # Find total mass of LV
    m_0 = m_pl_1 / payload_fraction

    # Find inert and propellant mass
    m_in_1 = delta_1 * m_0
    m_pr_1 = m_0 - m_in_1 - m_pl_1

    #Overwrite edge case if there is a negative mass (non-physical)
    if m_0 < 0:
        m_in_1 = np.nan
        m_pr_1 = np.nan
        m_in_2 = np.nan
        m_pr_2 = np.nan
        m_0 = np.nan

    return m_pr_1, m_pr_2, m_0, m_0_2







