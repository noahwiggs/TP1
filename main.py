import mass_estimation_part2 as me2
import Mass_functions as Mfunc
import thrust_convergance as tc
import Check_Solid_and_Storables as css
import Fairing_area as fa
import export_fn as exp


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
        Solid       # NOTE: singular
        Storables   # NOTE: plural
    """

    ## Inputs
    X = 50                     # Percentage
    s1_prop_mix = 'LOX_LCH4'   # Stage 1 propellant name
    s2_prop_mix = 'LOX_LCH4'   # Stage 2 propellant name

    # set to value, or find value based of engine configuration from number of engines
    stage_1_radius = 2.6 * 3
    stage_2_radius = 2.6
    
    print('----------------------------------------')
    print(f'Stage 1 Delta-V split: {X}%')
    print('Stage 1 Mixture: ', s1_prop_mix)
    print('Stage 2 Mixture: ', s2_prop_mix)
    print('----------------------------------------')

    ## start by finding part 1 values, gross and propellant mass of each stage
    m_pr_1, m_pr_2, m_0, m_0_2 = me2.mass_estimation(X, s1_prop_mix, s2_prop_mix)
    # print(f"Debug - m_pr_1: {m_pr_1}")
    # print(f"Debug - m_pr_2: {m_pr_2}")
    # print(f"Debug - m_0: {m_0}")
    # print(f"Debug - m_0_2: {m_0_2}")
    m_pl = 26000 # kg

    ## determine tank/insulation/casing properties
    
    s1_tank_radius, s1_total_height, s1_tanks_mass, s1_insul_mass = css.Check_Solid_and_Storables(
        s1_prop_mix,
        m_pr_1,
        tank_radius=stage_1_radius
    )
    s2_tank_radius, s2_total_height, s2_tanks_mass, s2_insul_mass = css.Check_Solid_and_Storables(
        s2_prop_mix,
        m_pr_2,
        tank_radius=stage_2_radius
    )

    print('----------------------------------------')
    print(f'Stage 1 Height: {s1_total_height:.2f} (m)')
    print(f'Stage 2 Height: {s2_total_height:.2f} (m)')
    print(f'Stage 1 L/D: {s1_total_height / s1_tank_radius:.2f}')
    print(f'Stage 2 L/D: {s2_total_height / s2_tank_radius:.2f}')
    print('----------------------------------------')


    # determine mass of other elements

    # determine fairing mass using surface area
    nose_h = 6      # nose cone height (m)
    nose_r = 2.6    # nose cone radius (m)

    f_nose_A, f_pl_A, f_s1_A, f_s2_A, f_if_A, f_aft_A = fa.fairing_area(
        s1_tank_radius,
        s1_total_height,
        s2_tank_radius,
        s2_total_height,
        nose_h,
        nose_r
    )

    nose_fairing_m      = Mfunc.M_fairing(f_nose_A)
    payload_fairing_m   = Mfunc.M_fairing(f_pl_A)
    s1_tank_f_m         = Mfunc.M_fairing(f_s1_A)
    s2_tank_f_m         = Mfunc.M_fairing(f_s2_A)
    inter_fairing_m     = Mfunc.M_fairing(f_if_A)
    aft_fairing_m       = Mfunc.M_fairing(f_aft_A)

    s1_fairing_mass = s1_tank_f_m + inter_fairing_m + aft_fairing_m
    s2_fairing_mass = s2_tank_f_m + payload_fairing_m + nose_fairing_m


    avionic_mass = Mfunc.M_avionic(m_0) # attributed to second stage only

    s1_wiring_mass = Mfunc.M_wiring(m_0, s1_total_height)
    s2_wiring_mass = Mfunc.M_wiring(m_0_2, s2_total_height)

    # find thrust required
    # other masses is the combination of all inert masses, minus thrust structure, engine, and gimbal masses
    stage_1_other_masses = s1_tanks_mass + s1_insul_mass + s1_fairing_mass + s1_wiring_mass
    stage_2_other_masses = s2_tanks_mass + s2_insul_mass + s2_fairing_mass + s2_wiring_mass + avionic_mass

    t_req1, t_req2 = tc.thrust_convergance(m_0, m_0_2, m_pr_1, m_pr_2, m_pl, stage_1_other_masses, stage_2_other_masses, s1_prop_mix, s2_prop_mix)

    # find total rocket mass from thrust
    s1_m_0, s2_m_0, thrust_masses = tc.thrust_mass_calculations(m_pr_1, m_pr_2, m_pl, stage_1_other_masses, stage_2_other_masses, t_req1, t_req2, s1_prop_mix, s2_prop_mix)
    
    s1_engine_mass = thrust_masses[0]   # Engines
    s2_engine_mass = thrust_masses[1]
    s1_t_struct_m = thrust_masses[2]    # Thrust structure
    s2_t_struct_m = thrust_masses[3]
    s1_gimbal_mass = thrust_masses[4]   # Gimbals
    s2_gimbal_mass = thrust_masses[5]


    # TODO: calculate all inert masses
    masses = [
        m_pr_1,             # Propellant
        m_pr_2,
        s1_tanks_mass,      # Propellant tanks -> is casing mass for solids
        s2_tanks_mass,
        s1_insul_mass,      # Propellant tank insulation
        s2_insul_mass,
        s1_engine_mass,     # Engines
        s2_engine_mass,
        s1_t_struct_m,      # Thrust structure
        s2_t_struct_m,
        s1_gimbal_mass,     # Gimbals
        s2_gimbal_mass,
        avionic_mass,       # Avionics -> stage 2 only
        s1_wiring_mass,     # Wiring
        s2_wiring_mass,
        payload_fairing_m,  # Payload fairing
        inter_fairing_m,    # Inter-stage fairing
        s1_tank_f_m,        # Tank fairing
        s2_tank_f_m,
        aft_fairing_m,      # Aft fairing
    ]

    STAGE_1_INERT_INDICIES = [2, 4, 6, 8, 10, 13, 16, 17, 19]
    STAGE_2_INERT_INDICIES = [3, 5, 7, 9, 11, 12, 14, 15, 18]

    s1_inert_mass = sum([masses[i] for i in STAGE_1_INERT_INDICIES])
    s2_inert_mass = sum([masses[i] for i in STAGE_2_INERT_INDICIES])

    print('----------------------------------------')
    print(f'Stage 1 Inert Mass: {s1_inert_mass:.3f} (kg)')
    print(f'Stage 2 Inert Mass: {s2_inert_mass:.3f} (kg)')
    print('----------------------------------------')

    # TODO: calculate cost

    s1_cost = me2.stage_nre_cost(s1_inert_mass)
    s2_cost = me2.stage_nre_cost(s2_inert_mass)

    print(f'Stage 1 cost is: {s1_cost:.3f} $M 2025')
    print(f'Stage 2 cost is: {s2_cost:.3f} $M 2025')
    print(f'Total cost is {(s1_cost + s2_cost)/1000:.3f} $B 2025')
    print('----------------------------------------')


    # TODO: find inert mass fraction

    s1_inert_m_frac = s1_inert_mass / s1_m_0
    s2_inert_m_frac = s2_inert_mass / s2_m_0

    # mass margin
    s1_m_0 *= 1.3
    s2_m_0 *= 1.3

    print(f'Stage 1 inert mass fraction is: {s1_inert_m_frac:.3f}')
    print(f'Stage 2 inert mass fraction is: {s2_inert_m_frac:.3f}')
    print('----------------------------------------')

    masses_for_output = [
        (m_pr_1+m_pr_2),                    # Propellant
        (s1_tanks_mass+s2_tanks_mass),      # Propellant tanks -> is casing mass for solids
        (s1_insul_mass+s2_insul_mass),      # Propellant tank insulation
        (s1_engine_mass+s2_engine_mass),    # Engines
        (s1_t_struct_m+s2_t_struct_m),      # Thrust structure
        (s1_gimbal_mass+s2_gimbal_mass),    # Gimbals
        (avionic_mass),                     # Avionics -> stage 2 only
        (s1_wiring_mass+s2_wiring_mass),    # Wiring
        payload_fairing_m,                  # Payload fairing
        inter_fairing_m,                    # Inter-stage fairing
        (s1_tank_f_m+s2_tank_f_m),          # Tank fairings
        aft_fairing_m,                      # Aft fairing
    ]

    stage_1_totals = (
        m_pr_1 +                # Stage 1 propellant
        s1_tanks_mass +         # Propellant tanks
        s1_insul_mass +         # Tank insulation
        s1_engine_mass +        # Engines
        s1_t_struct_m +         # Thrust structure
        s1_gimbal_mass +        # Gimbals
        s1_wiring_mass +        # Wiring
        s1_tank_f_m +           # Inter-tank fairing
        aft_fairing_m           # Aft fairing
    )

    stage_2_totals = (
        m_pr_2 +                # Stage 2 propellant
        s2_tanks_mass +         # Propellant tanks
        s2_insul_mass +         # Tank insulation 
        s2_engine_mass +        # Engines
        s2_t_struct_m +         # Thrust structure
        s2_gimbal_mass +        # Gimbals
        avionic_mass +          # Avionics (stage 2 only)
        s2_wiring_mass +        # Wiring
        payload_fairing_m +     # Payload fairing
        inter_fairing_m +       # Inter-stage fairing
        s2_tank_f_m             # Inter-tank fairing
    )

    # Overall totals
    totals = [
        stage_1_totals,
        stage_2_totals,
        stage_1_totals + stage_2_totals,
        (s1_cost+s2_cost)
    ]

    ## Output results to csv table
    exp.export(masses_for_output,totals)

if __name__ == '__main__':
    main()