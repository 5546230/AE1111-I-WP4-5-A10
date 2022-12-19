import numpy as np
from column_buckling import *
from matplotlib import pyplot as plt

m=0.5
a_stringer = (35*10**-3)**2
n = 4
t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 12*10**-3

ribs_list = np.array([0.33, 2.4, 2.61, 3.70, 4.00, 5.15, 5.34, 6.24, 7.04, 7.74, 8.05])
lengths = np.zeros(len(ribs_list))
for i in range(0,len(ribs_list)):
    if i == 0:
        lengths[i] = ribs_list[i]
    else:
        lengths[i] = ribs_list[i]-ribs_list[i-1]
print(lengths)
option1 = design_option_column((m)*a_stringer, n, 10, lengths, t_s, t_f, t_r)
option1.generate_plot()
print(option1.test())
print(option1.a)