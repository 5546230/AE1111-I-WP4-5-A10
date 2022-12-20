from skin_stress import mass_config_per_length
from skin_stress import mass_remaining

a_stringer = (35*10**-3)**2

def mass_bay(y1, y2, n, m, t, a_stringer):
    mass = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1)
    return mass

def mass_expected(y1, y2, n, m, t, a_stringer):
    exp = mass_config_per_length(n, m, y1, y2, t, a_stringer)*(y2-y1) + mass_remaining(y2)
    return exp

if __name__=="__main__":
    print(mass_bay(1.26, 4.5, 6, 0.5, 12.4*10**-3, a_stringer))
    print(mass_expected(1.26, 4.5, 6, 0.5, 12.4*10**-3, a_stringer))