import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"

#wingspan
b = 24 #m
E = 68e9 #Pa
nu = 0.33 #-

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
n_u = n_stringers//2
t = designs[design_option]["t"]*1e-3 #m
a_stringer = designs[design_option]["a_stringer"] #m^2

#Manual t input - leave it like this
t = 0.0063
#

#load case for maximum compression in upper skin panels
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

#assumed distance from NA is the upper left corner of the wing box (conservative)
def skin_stress(y):
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t, n_stringers, 3*a_stringer) #Pa; flexure formula #On purpose 3*
    return sigma

def av_skin_stress(y1, y2):
    sigma_av = 0.5*(skin_stress(y1)+skin_stress(y2))
    return sigma_av

def ratio():
    ratio = []
    for i in range(5, int(b/2)+1):
        r = skin_stress(5)/skin_stress(i+1)
        ratio.append(r)
    return ratio

def stress_crit(y1, y2):
    slenderness = ((n_u+1)*(y2-y1))/(get_c(y1)) #a over b
    K = 0.0364*(slenderness)**2 - 0.3815*(slenderness) + 4.2206 #for linearly varying moment
    sigma_crit = ((t**2*E*np.pi**2)/(12*(1-nu**2)))*(((n_u+1)/(get_c(y1)))**2)
    return sigma_crit

sigma_yield = 271*10**6
#s = skin_stress(0)
#print(s)

#while s > sigma_yield:
#    t += 0.0001
#    s = skin_stress(0)

#print(t)
#print(s)

#Rib placement
dy = 0.1 #m
y1 = 0 #m
y2 = y1 + dy #m

s = skin_stress(y2)
s_crit = stress_crit(y1, y2)

#while s > s_crit:

#Work in progress