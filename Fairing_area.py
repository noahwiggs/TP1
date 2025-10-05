import numpy as np

# input fairing_area(stage 1 tank radius, stage 1 total height, stage 2 tank radius, stage 2 total height)
def fairing_area(st1_r,st1_h,st2_r,st2_h, nose_h, nose_r):
    # prolate ellipsoid calculations
    e = np.sqrt(1 - (nose_r**2 / nose_h**2))
    A_ellipsoid = 2 * np.pi * nose_r**2 * (1 + (nose_h / (nose_r * e)) * np.arcsin(e))
    # nose cone is half of the ellipsoid
    A_nose_cone = A_ellipsoid / 2

    A_pl=2*np.pi*2.6*14
    A_st2=2*np.pi*st2_r*st2_h
    A_st1=2*np.pi*st1_r*st1_h
    A_if=np.pi*(st1_r+st2_r)*np.sqrt((st2_r-st1_r)**2+3)
    A_aft=2*np.pi*st1_r*3
    # s1_combined_A = A_st1 + A_aft
    # s2_combined_A = A_nose_cone + A_pl + A_st2 + A_if

    return A_nose_cone, A_pl, A_st2, A_st1, A_if, A_aft

# def fairing_area_ellipsoid(a, b):
# NOTE: Implemented ontop
#     alpha = np.acos(a/b)
#     A_fairing=2*np.pi*(a**2+(a*b*alpha)/np.sin(alpha))
    
#     return A_fairing

