import numpy as np
from skin_stress import skin_stress
from load_case import *

t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 13.6*10**-3 #m (skin thickness - ask for it in each bay)
a_stringer = (35*10**-3)**2
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
n = 4
m = 0.08

#INPUT
n=2
y1 = 10.16

stress1 = skin_stress(y1, t_f, t_r, t_s, a_stringer, load_max_compr, n, m)
print(stress1)

n=4
y2 = 9.9

stress2 = skin_stress(y2, t_f, t_r, t_s, a_stringer, load_max_compr, n, m)
print(stress2)