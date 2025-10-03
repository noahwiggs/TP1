import numpy as np

# input fairing_area(stage 1 tank radius, stage 1 tank height, stage 2 tank radius, stage 2 tank height)
def fairing_area(st1_r,st1_h,st2_r,st2_h):

    A_cone=np.pi*2.6*np.sqrt(2.6^2+10^2)
    A_pl=2*np.pi*2.6*14
    A_st2=2*np.pi*st2_r*st2_h
    A_st1=2*np.pi*st1_r*st1_h
    A_if=np.pi*(st1_r+st2_r)*np.sqrt((st2_r-st1_r)^2+3)
    A_aft=2*np.pi*st1_r*3
    A_fairing=A_cone+A_pl+A_if+A_aft+A_st2+A_st1

    return A_fairing