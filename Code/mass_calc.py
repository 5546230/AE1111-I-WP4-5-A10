from skin_stress import mass_config_per_length
from skin_stress import mass_remaining
import numpy as np

a_stringer = (35*10**-3)**2
m = 0.08
masses = [98, 85, 70, 58, 53, 47, 43, 76, 59, 46, 37, 30, 30, 14, 50]
ribs_list = np.array([0, 0.345, 0.69, 1.02, 1.35, 1.655, 1.96, 2.25, 2.535, 2.815, 3.09, 3.36, 3.63, 3.895, 4.155, 4.41, 4.665, 4.92, 5.175, 5.41, 5.645, 5.88, 6.115, 6.335, 6.555, 6.775, 6.995, 7.2, 7.405, 7.615, 7.825, 8.02, 8.215, 8.415, 8.62, 8.975, 9.34, 9.59, 9.85, 10.13, 12])

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