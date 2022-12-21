from skin_stress import mass_config_per_length
from skin_stress import mass_remaining
import numpy as np

a_stringer = (35*10**-3)**2
m = 0.08

def mass_bay(y1, y2, n, m, t, a_stringer):
    mass = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1)
    return mass

def mass_expected(y1, y2, n, m, t, a_stringer):
    exp = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1) + mass_remaining(y2)
    return exp

if __name__=="__main__":
    print(mass_bay(0, 0.94, 6, m, 13.6*10**-3, a_stringer))
    print(mass_expected(0, 0.94, 6, m, 13.6*10**-3, a_stringer))

    #a = np.sqrt(m*a_stringer*10/2)
    #print(a)