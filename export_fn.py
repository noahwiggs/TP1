import pandas as pd

def export(compiled_masses):
    rows = [
        "Propellant",
        "Propellant tanks",
        "Propellant tank insulation",
        "Engines",
        "Thrust structure",
        "Casing",
        "Gimbals",
        "Avionics",
        "Wiring",
        "Payload fairing",
        "Inter-tank fairing",
        "Inter-stage fairing",
        "Aft fairing"
        "Total"
        ]
        
    df = pd.DataFrame({
    "Subsystem": rows,
    "Mass (kg)": compiled_masses,
    })

    totals = pd.DataFrame({
    "Subsystem": ["TOTAL"],
    "Total Mass (kg)": [sum(compiled_masses)],
    })
    
    df = pd.concat([df, totals], ignore_index=True)

    df.to_csv("results.csv", index=False)
    
    print(df)