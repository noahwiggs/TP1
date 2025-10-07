import pandas as pd

def export(masses, totals):
    rows = [
        "Propellant",
        "Propellant tanks/casing",
        "Propellant tank insulation",
        "Engines",
        "Thrust structure",
        "Gimbals",
        "Avionics",
        "Wiring",
        "Payload fairing",
        "Inter-tank fairing",
        "Inter-stage fairing",
        "Aft fairing"
    ]
    
    masses_t = [m / 1000 for m in masses]
    totals_t = [
        totals[0] / 1000,   # Stage 1 total mass
        totals[1] / 1000,   # Stage 2 total mass
        totals[2] / 1000,   # Total mass
        totals[3] / 1e3,    # Total Cost
        totals[4] / 1e3,    # Total Cost with margin 
    ]


    df = pd.DataFrame({
        "Subsystem": rows,
        "Mass (t)": masses_t,
    })
    
    df = pd.concat([
        df,
        pd.DataFrame({"Subsystem": ["Stage 1 Total"], "Mass (t)": [totals_t[0]]}),
        pd.DataFrame({"Subsystem": ["Stage 2 Total"], "Mass (t)": [totals_t[1]]}),
        pd.DataFrame({"Subsystem": ["Total Mass with mass margin to inert masses"], "Mass (t)": [totals_t[2]]}),
        pd.DataFrame({"Subsystem": ["Total Cost ($B, 2025)"], "Mass (t)": [totals_t[3]]}),
        pd.DataFrame({"Subsystem": ["Total Cost With Margin ($B, 2025)"], "Mass (t)": [totals_t[4]]})
    ], ignore_index=True)
    
    df.to_csv("results.csv", index=False)
    print(df.round(3))