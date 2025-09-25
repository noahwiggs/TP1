#Requires numpy and matplotlib
import numpy as np
import matplotlib.pyplot as plt

def delta_V_split(stage_1_Isp, stage_2_Isp):
    """
    Create a matrix of delta V splits (0, 1) identified by X,
    Where the first stage delta_V fraction X plus the second stage delta_V fraction 1-X
    equals the total required delta_V of 12.3.

    Call stage_mass() to asign each split its corresponding mass properties.

    Input:
    stage_1_Isp (float): Isp of the first stage engine (sec)
    stage_2_Isp (float): Isp of the second stage engine (sec)

    Output:
    delta_V_data (np.array): [X, stage_1_dV, stage_1_dV, m_in_1, m_pr_1, m_in_2, m_pr_2, m0, stage_1_no_pl, stage_1_no_pl], all floats

    """
    #Requirements
    dv_req = 12300 # m/s

    #Initialize loop parameters
    N = 100
    delta_V_data = np.zeros((N, 10))

    #Iterate X across range of 0.01 to 1
    for X in range(N):
        #Calculate the dV % for each stage at given value of X
        stage_1_dv = dv_req * (X / 100)
        stage_2_dv = dv_req * (1 - X/100)

        #Call stage_mass() to calculate the mass parameters of that stage
        m_in_1, m_pr_1, m_in_2, m_pr_2, m_0, stage_1_no_pl, stage_2_no_pl = stage_mass(stage_1_dv, stage_2_dv, stage_1_Isp, stage_2_Isp)

        #fill out the numpy array with relevant data for each iteration
        delta_V_data[X, 0] = X
        delta_V_data[X, 1] = stage_1_dv
        delta_V_data[X, 2] = stage_2_dv
        delta_V_data[X, 3] = m_in_1
        delta_V_data[X, 4] = m_pr_1
        delta_V_data[X, 5] = m_in_2
        delta_V_data[X, 6] = m_pr_2
        delta_V_data[X, 7] = m_0
        delta_V_data[X, 8] = stage_1_no_pl
        delta_V_data[X, 9] = stage_2_no_pl

    return delta_V_data

def stage_mass(stage_1_delta_V, stage_2_delta_V, stage_1_Isp, stage_2_Isp):
    """
    Calculate the masses of each stage based of allocated delta V.

    Input:
    stage_1_delta_V (float): Delta V allocated to stage 1
    stage_2_delta_V (float): Delta V allocated to stage 2
    stage_1_Isp (int): Isp of stage 1 propellant
    stage_2_Isp (int): Isp of stage 2 propellant

    Return:
    m_in_1 (float): inert mass of stage 1 (kg)
    m_pr_1 (float): propellant mass of stage 1 (kg)
    m_in_2 (float): inert mass of stage 2 (kg)
    m_pr_2 (float): propellant mass of stage 2 (kg)
    m_0 (float): total mass LV (kg)
    stage_1_no_pl (float): stage 1 mass, without payload (kg)

    """

    #Knowns/requirements
    delta_1 = 0.08
    delta_2 = 0.08
    g_0 = 9.81 # m/s2
    m_pl_2 = 26000 # kg

    ## Stage 2
    #Find mass ratio
    frac = stage_2_delta_V / (g_0 * stage_2_Isp)
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

    frac = stage_1_delta_V / (g_0 * stage_1_Isp)
    r_1 = np.exp(-frac)

    # Find payload fraction
    payload_fraction = r_1 - delta_1

    # Find total mass of LV
    m_0 = m_pl_1 / payload_fraction

    # Find inert and propellant mass
    m_in_1 = delta_1 * m_0
    m_pr_1 = m_0 - m_in_1 - m_pl_1
    stage_1_no_pl = m_in_1 + m_pr_1
    stage_2_no_pl = m_in_2 + m_pr_2

    #Overwrite edge case if there is a negative mass (non-physical)
    if m_0 < 0:
        m_in_1 = np.nan
        m_pr_1 = np.nan
        m_in_2 = np.nan
        m_pr_2 = np.nan
        m_0 = np.nan
        stage_1_no_pl = np.nan
        stage_2_no_pl = np.nan

    return m_in_1, m_pr_1, m_in_2, m_pr_2, m_0, stage_1_no_pl, stage_2_no_pl


def plot_delta_V_split(delta_V_split):
    """
    Plot the total initial mass of the launch vehicle as a function of dV split
    between stage 1 and stage 2.

    Input:
    delta_V_split (np.array): Matrix with split data.

    Return:
    min_mass (float): Minimum total mass across all dV splits (kg).
    """

    # Extract X (stage-1 dV fraction in percent) and total mass from data
    X = delta_V_split[:, 0]
    stage_1_no_pl=delta_V_split[:,8]/1000
    stage_2_no_pl=delta_V_split[:,9]/1000
    m_0 = delta_V_split[:, 7]/1000

    #Find minimum total mass and corresponding dV fraction
    min_mass = np.nanmin(m_0)
    i_min = np.nanargmin(m_0)
    X_min = X[i_min]

    #Plot total mass vs dV split
    plt.plot(X, m_0,label='Gross Mass')
    plt.plot(X,stage_1_no_pl, label='Stage 1 Mass (no pl)')
    plt.plot(X,stage_2_no_pl,label='Stage 2 Mass (no pl)')
    plt.plot(X_min, min_mass, "ro", label="Minimum")
    plt.title('Stage 1: ?   Stage 2: ?')
    plt.xlabel('Stage 1 dV fraction (%)')
    plt.ylabel('Mass (t)')
    plt.legend()
    plt.grid(True)
    plt.show()

    print(f'Min LV gross mass: {min_mass:.0f} t')
    print(f'Min LV mass sol stage 1 dV fraction: {X[i_min]/100.0}')

    m_in_1_min = delta_V_split[i_min, 3]  #stage 1 inert mass (kg)
    m_in_2_min = delta_V_split[i_min, 5]  # stage 2 inert mass (kg)

    C1_min = stage_nre_cost(m_in_1_min)   #millions of 2025 $
    C2_min = stage_nre_cost(m_in_2_min)   #millions of 2025 $
    Ctot_min = C1_min + C2_min

    print(f'Min LV mass program cost: ${Ctot_min:.2f} M')
    print(' ')

    return min_mass


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


def plot_cost(stage_1_cost, stage_2_cost, total_cost, X, m_0):
    """
    Plot program cost trends as a function of first-stage dV fraction.

    Input:
    stage_1_cost (array): NRE cost of stage 1 for each dV fraction (millions $)
    stage_2_cost (array): NRE cost of stage 2 for each dV fraction (millions $)
    total_cost (array): Total program cost (millions $)
    X (array): Stage 1 dV fraction values (percent)
    m_0 (array): Total initial mass values (kg)

    Return:
    None
    """

    #Find index of minimum total cost
    i_min = np.nanargmin(total_cost)
    X_min, cost_min, mass_cost_min = X[i_min], total_cost[i_min], m_0[i_min]

    #Report minimum cost, dV fraction, and mass at that point
    print(f"Min program cost: ${cost_min:.2f} M")
    print(f"Min progran cost stage 1 dV fraction: {X_min/100.0}")
    print(f"Min program cost LV gross mass: {mass_cost_min/1000:.3e} t")
    print(" ")

    # Plot stage costs, total cost, and highlight the minimum
    plt.plot(X, stage_1_cost, label="Stage 1 cost")
    plt.plot(X, stage_2_cost, label="Stage 2 cost")
    plt.plot(X, total_cost,   label="Total cost")
    plt.plot(X_min, cost_min, "ro", label="Minimum")
    plt.xlabel('Stage 1 dV fraction (%)')
    plt.ylabel("Cost")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    """
    Inputs:  None (uses the test Isp values defined inside)
    Returns: None (produces plots and console output)
    """

    #Test cases:
    test_Isp1 = 366  # specific impulse of stage 1 (sec)
    test_Isp2 = 366  # specific impulse of stage 2 (sec)

    #Find and report min mass across dV plots

    # Creates (N x 8) table over X = 1-100% split dV split between stage 1 and 2
    delta_V_data = delta_V_split(test_Isp1, test_Isp2)

    #Plot m0 vs X; return minimum mass (kg)
    min_mass = plot_delta_V_split(delta_V_data)

    #Extract arrays from the dV table for cost plotting
    X = delta_V_data[:, 0]
    m_0 = delta_V_data[:, 7]
    m_in_1 = delta_V_data[:, 3]
    m_in_2 = delta_V_data[:, 5]

    #Compute NRE costs for each split ($M, 2025)
    stage_1_cost = stage_nre_cost(m_in_1)
    stage_2_cost = stage_nre_cost(m_in_2)
    total_cost = stage_1_cost + stage_2_cost

    #Plot cost trends vs dV split, mark the min point
    plot_cost(stage_1_cost, stage_2_cost, total_cost, X, m_0)

if __name__ == '__main__':
    main()