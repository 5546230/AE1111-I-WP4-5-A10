import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from skin_stress import skin_stress
from load_case import LoadCase
from interpolation import *




#y, t_f, t_r, t, a_stringer, load_max_compr, n_stringers, m

b = 24 #m
t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 13.6*10**-3 #m (skin thickness - ask for it in each bay)
a_stringer = (35*10**-3)**2
load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
#n = 4
m = 0.362

#INPUT
n = 2
y1 =  9.735

stress1 = skin_stress(y1, t_f, t_r, t_s, a_stringer, load_max_compr, n, m)
#print(stress1)

n = 2
y2 = 12

stress2 = skin_stress(y2, t_f, t_r, t_s, a_stringer, load_max_compr, n, m)
#print(stress2)

ratio = stress1/stress2

print('RATIO IS:', ratio)



#OPTION1:
#n = 6 if x< 7.49 else 4 if x<8.7 else 2
    #m = 0.362
    #ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 
    # 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 
    # 8.385, 8.7, 9.06, 9.435, 9.735, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])
    #masses = [109, 86, 59, 49, 61, 48, 53, 47, 46, 49, 26, 61, 31, 73] -> 798kg
    #41 rib