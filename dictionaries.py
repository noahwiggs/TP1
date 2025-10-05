#Dictionaries=(Isp (sec), Trust Stage 1 (N), Thrust Stage 2 (N), Exhaust Area Stage 1 (m), Exhaust Area Stage 2 (m), 
# Chamber Pressure Stage 1 (Pa), Chamber Pressure Stage 2 (Pa))
# LOX_CH4=dict(Isp=327, Thrust_st1=2260000, Thrust_st2=745000, A_e1=2.4, A_e2=1.5, Pressure_st1=35160000, Pressure_st2=10100000)
# LOX_LH2=dict(Isp=366, Thrust_st1=1860000, Thrust_st2=99000, A_e1=2.4, A_e2=2.15, Pressure_st1=20640000, Pressure_st2=4200000)
# LOX_RP1=dict(Isp=311, Thrust_st1=1920000, Thrust_st2=61000, A_e1=3.7, A_e2=.92, Pressure_st1=25800000,Pressure_st2=6770000)
# Solid=dict(Isp=269, Thrust_st1=4500000, Thrust_st2=2940000, A_e1=6.6, A_e2=2.34, Pressure_st1=10500000, Pressure_st2=5000000)
# Storeable=dict(Isp=285, Thrust_st1=1750000, Thrust_st2=67000, A_e1=1.5, A_e2=1.13, Pressure_st1=15700000, Pressure_st2=14700000)

from typing import Dict

# mixture name : Isp (seconds)
Isp_values: Dict[str, int] = {
    'LOX_LCH4'   : 327,
    'LOX_LH2'    : 366,
    'LOX_RP1'    : 311,
    'Solid'      : 269,
    'N2O4'       : 285,
    'Storables'  : 285,
}

# mixturer name : Thrust (N)
Thrust_stage1: Dict[str, int] = {
    'LOX_LCH4'   : 2260000,
    'LOX_LH2'    : 1860000,
    'LOX_RP1'    : 1920000,
    'Solid'      : 4500000,
    'Storables'  : 1750000,

}

# mixture name : Thrust (N)
Thrust_stage2: Dict[str, int] = {
    'LOX_LCH4'   : 745000,
    'LOX_LH2'    : 99000,
    'LOX_RP1'    : 61000,
    'Solid'      : 2940000,
    'Storables'  : 67000,

}

# mixture name : Area ratio
Expansion_ratio_stage1: Dict[str, float] = {
    'LOX_LCH4'   : 34.34,
    'LOX_LH2'    : 78,
    'LOX_RP1'    : 37,
    'Solid'      : 16,
    'Storables'  : 26.2,

}

# mixture name : Area ratio
Expansion_ratio_stage2: Dict[str, float] = {
    'LOX_LCH4'   : 45,
    'LOX_LH2'    : 84,
    'LOX_RP1'    : 14.5,
    'Solid'      : 56,
    'Storables'  : 81.3,

}

# mixture name : Pressure (Pa)
Chamber_pressure_stage1: Dict[str, int] = {
    'LOX_LCH4'   : 35160000,
    'LOX_LH2'    : 20640000,
    'LOX_RP1'    : 25800000,
    'Solid'      : 10500000,
    'Storables'  : 15700000,

}

# mixture name : Pressure (Pa)
Chamber_pressure_stage2: Dict[str, int] = {
    'LOX_LCH4'   : 10100000,
    'LOX_LH2'    : 4200000,
    'LOX_RP1'    : 6770000,
    'Solid'      : 5000000,
    'Storables'  : 14700000,

}


# mixture name : oxidizer : fuel
fuel_ratios: Dict[str, float] = {
    'LOX_LCH4'   : 3.6,
    'LOX_LH2'    : 6.03,
    'LOX_RP1'    : 2.72,
    'Solid'      : 1,
    'Storables'  : 2.67,

}

# prop name : density (kg/m3)
prop_densities: Dict[str, int] ={
    'LH2'        : 71, 
    'LOX'        : 1140, 
    'RP1'        : 820, 
    'LCH4'       : 423, 
    'Solid'      : 1680, 
    'N2O4'       : 1442, 
    'UDMH'       : 791
    
}

# prop name : exhaust diameter
exhaust_diameter_stage1: Dict[str, float] ={
    'LOX_LCH4'   : 2.4,
    'LOX_LH2'    : 2.4,
    'LOX_RP1'    : 3.7,
    'Solid'      : 6.6,
    'Storables'  : 1.5,
}

# prop name : exhaust diameter
exhaust_diameter_stage2: Dict[str, float] ={
    'LOX_LCH4'   : 1.5,
    'LOX_LH2'    : 2.15,
    'LOX_RP1'    : 0.92,
    'Solid'      : 2.34,
    'Storables'  : 1.13,
}