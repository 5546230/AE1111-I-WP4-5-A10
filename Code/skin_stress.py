import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"

#default is option 1
design_option = 1
design_option = str(input("Design option (1, 2 or 3):", ))

#design options parameters (n_stringers, t, ...)
designs = {
    "1":dict(t = 4, n_stringers = 0, a_stringer = 0),
    "2":dict(t = 1.5, n_stringers = 2, a_stringer = (65e-3)**2),
    "3":dict(t = 2, n_stringers = 4, a_stringer = (35e-3)**2)
}

n_stringers = designs[design_option]["n_stringers"]
t = designs[design_option]["t"]*1e-3 #m
a_stringer = designs[design_option]["a_stringer"] #mm^2

#load case for maximum compression in upper skin panels
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

#assumed distance from NA is the upper left corner of the wing box (conservative)
def skin_stress(y):
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t, n_stringers, a_stringer) #Pa; flexure formula
    return sigma

def av_skin_stress(y1, y2):
    sigma_av = 0.5*(skin_stress(y1)+skin_stress(y2))
    return sigma_av

def ratio(0, y):
    ratio = []
    for i in len(0, b/2):
        y = +1
        ratio[i] = skin_stress(0)/skin_stress(y[i])
        ration.append(ratio[i])
    return ratio

