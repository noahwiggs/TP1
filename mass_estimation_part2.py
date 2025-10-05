import numpy as np

from typing import Tuple
from dictionaries import Isp_values


def mass_estimation(
        X           : float,
        mixture_1   : str,
        mixture_2   : str,
    )-> Tuple[float, float, float, float]:
    """
    Calculates relevant mass values for use in heuristics from stage 1 dV fraction, X
    
    Inputs:
    X           (float) : stage 1 dV fraction percentage
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

    # print(f'Debug - {stage_1_Isp}')
    # print(f'Debug - {stage_2_Isp}')


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

    print(f'Stage 1 Inert Mass Estimate: {m_in_1}')
    print(f'Stage 2 Inert Mass Estimate: {m_in_2}')

    #Overwrite edge case if there is a negative mass (non-physical)
    if m_0 < 0:
        m_in_1 = np.nan
        m_pr_1 = np.nan
        m_in_2 = np.nan
        m_pr_2 = np.nan
        m_0 = np.nan

    # print(f"Debug - m_pr_1: {m_pr_1}")
    # print(f"Debug - m_pr_2: {m_pr_2}")
    # print(f"Debug - m_0: {m_0}")
    # print(f"Debug - m_0_2: {m_0_2}")

    return m_pr_1, m_pr_2, m_0, m_0_2

def stage_nre_cost(m_in):
    """
    Estimate the total non-recurring engineering (NRE) cost of a launch vehicle stage

    Input:
    m_in (float): Inert mass of stage (kg)

    Return:
    stage_cost (float): Cost of stage (millions of dollars, 2025)
    """
    stage_cost = 13.52 * pow(m_in, 0.55)
    return stage_cost







