import numpy as np
from column_buckling import *
from matplotlib import pyplot as plt

m=0.1
a_stringer = (35*10**-3)**2
n = 10
t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 9.3*10**-3

ribs_list = np.array([0.63, 2.19, 2.61, 3.70, 4.00, 5.51, 5.34, 6.24, 7.04, 7.74, 8.05])
option1 = design_option_column((m)*a_stringer, n, 10, ribs_list, t_s, t_f, t_r)
option1.generate_plot()