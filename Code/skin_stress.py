import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"

#default is option 1
design_option = 1
design_option = int(input("Design option (1, 2 or 3):", ))

#design options parameters (n_stringers, t, ...)
designs = [0, 4, 1, 1.5, 2, 1.5]

n_stringers = designs[2*design_option-2]
t = designs[2*design_option-1]*10**-3 #m

#load case for maximum compression in upper skin panels
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

#assumed distance from NA is the upper left corner of the wing box (conservative)
def skin_stress(y):
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t, n_stringers) #Pa; flexure formula
    return sigma

def av_skin_stress(y1, y2):
    sigma_av = 0.5*(skin_stress(y1)+skin_stress(y2))
    return sigma_av
