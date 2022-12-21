import numpy as np
from column_buckling import *
from matplotlib import pyplot as plt

m=0.08
a_stringer = (35*10**-3)**2
n = 0
t_f = 5.5*10**-3 #m
t_r = 4*10**-3 #m
t_s = 1.3*10**-3

a = 4.5

ribs_list = np.array([0.47, 0.94, 1.35, 1.78, 2.06, 2.36, 2.61, 2.86, 3.28, 3.68, 4.2, 4.71, 5.44, 6.14, 6.8, 7.43, 8.03, 8.59, 9.13])
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

#this is insanely slow down here
#while not option1.test():
#    ribs_list = np.array([0.38, 0.81, 1.26, 1.71, a, 6, 6.2, 6.24, 7.04, 7.74, 8.05])
#    a -= 0.1
#    lengths = np.zeros(len(ribs_list))
#    for i in range(0,len(ribs_list)):
#        if i == 0:
#            lengths[i] = ribs_list[i]
#        else:
#            lengths[i] = ribs_list[i]-ribs_list[i-1]
#    option1 = design_option_column((m)*a_stringer, n, 10, lengths, t_s, t_f, t_r)

#print(a)