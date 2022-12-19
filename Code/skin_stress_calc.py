import numpy as np
from skin_stress import skin_stress
from load_case import *

t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 9.3*10**-3 #m (skin thickness - ask for it in each bay)
a_stringer = (35*10**-3)**2
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
n = 8
m = 0.1

#INPUT
y = 1.6

stress = skin_stress(y, t_f, t_r, t_s, a_stringer, load_max_compr, n, m)