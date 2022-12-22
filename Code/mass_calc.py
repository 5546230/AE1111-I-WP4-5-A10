from skin_stress import mass_config_per_length
from skin_stress import mass_remaining
import numpy as np

a_stringer = (35*10**-3)**2
m = 0.08
masses = [94, 120, 96, 75, 58, 45, 35, 26, 19, 14, 11, 14, 10, 9, 7]
ribs_list=[0.33, 0.66, 1.13, 1.59, 2.04, 2.48, 2.91, 3.32, 3.72, 4.11, 4.49, 4.86, 5.23, 5.59, 5.94, 6.28, 6.61, 6.93, 7.24, 7.54, 7.84, 8.13, 8.69, 9.22, 9.72, 10.20, 10.66, 11.09, 11.50, 12]

def mass_bay(y1, y2, n, m, t, a_stringer):
    mass = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1)
    return mass

def mass_expected(y1, y2, n, m, t, a_stringer):
    exp = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1) + mass_remaining(y2)
    return exp

if __name__=="__main__":
    print(mass_bay(0, 0.94, 6, m, 13.6*10**-3, a_stringer))
    print(mass_expected(0, 0.94, 6, m, 13.6*10**-3, a_stringer))
    print(mass_remaining(11.9))
    print(sum(masses))
    print(len(ribs_list))

    #a = np.sqrt(m*a_stringer*10/2)
    #print(a)