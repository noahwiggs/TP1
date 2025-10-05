import pandas as pd

def export(masses):
    rows = [
        "Stage 1 Propellant",
        "Stage 2 Propellant",
        "Stage 1 Propellant tanks",
        "Stage 2 Propellant tanks",
        "Stage 1 Propellant tank insulation",
        "Stage 2 Propellant tank insulation",
        "Stage 1 Engines",
        "Stage 2 Engines",
        "Stage 1 Thrust structure",
        "Stage 2 Thrust structure",
        "Stage 1 Gimbals",
        "Stage 2 Gimbals",
        "Avionics",
        "Stage 1 Wiring",
        "Stage 2 Wiring",
        "Payload fairing",
        "Inter-tank fairing",
        "Stage 1 Inter-stage fairing",
        "Stage 2 Tank fairing",
        "Aft fairing"
    ]
    
    df = pd.DataFrame({
        "Subsystem": rows,
        "Mass (kg)": masses,
    })
    
    totals = pd.DataFrame({
        "Subsystem": ["TOTAL"],
        "Mass (kg)": [sum(masses)],
    })
    
    df = pd.concat([df, totals], ignore_index=True)
    
    df.to_csv("results.csv", index=False)
    
    print(df)