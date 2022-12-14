import numpy as np
from matplotlib import pyplot as plt


class design_option:
    def __init__(self, a_stringer: float, a_t: float, ribs: list):
        self.a_stringer = a_stringer
        self.a = np.sqrt(a_stringer*a_t/2)
        self.ribs = np.array(ribs)
        self.lengths = self.ribs -np.insert(self.ribs, 0,0)[:-1]

        print(self.a, self.a_stringer, self.lengths)

    def crit_stress(self) -> float:
        k = 4
        e = 69e9
        crit_stress = k * np.pi**2*e*self.a**2 / (6*self.ribs**2)

        return crit_stress
    

    
ribs_2 = np.array([10.34,16.16])
ribs_3 = np.array([3.21,3.81,5.66])

option_2 = design_option((0.012675), 10, ribs_2)
option_3 = design_option((0.001225), 10, ribs_3)

print(option_2.crit_stress())
print(option_3.crit_stress())
