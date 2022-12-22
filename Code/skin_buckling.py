import numpy as np
from skin_stress import *
from load_case import LoadCase

class design_option_skin:
    def __init__(self, a_stringer: float, n_stringers, ribs: list, t_lst: list, y_lst: list, t_f: float, t_r: float, m: float):
        #define the variables
        self.a_stringer = m*a_stringer
        self.n_stringers = n_stringers
        self.ribs = ribs
        self.y_lst = y_lst
        self.t_lst = t_lst
        self.t_f = t_f
        self.t_r = t_r
        self.m = m
        self.load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    def skin_buckling_mos(self, y1: float, y2: float):
        indices = np.where(self.y_lst > y1)
        t_index = np.amin(indices)

        #critical and actual stresses in a bay
        critical = stress_crit(y1, y2, self.t_lst[t_index], self.n_stringers(y1)//2, self.n_stringers(y1)//2, 1)[0]
        actual = av_skin_stress(y1, y2, self.t_f, self.t_r, self.t_lst[t_index], self.a_stringer, self.load, self.n_stringers(y1), self.m)

        print("\n", y1, y2, self.t_lst[t_index], "Critical: ", critical, "Actual: ", actual, "\n")

        margin = actual/critical

        return margin

    def skin_buckling_mos_plot(self):
        for i in range(0, len(self.ribs)-1):
            y1 = self.ribs[i]
            y2 = self.ribs[i+1]
            mos = self.skin_buckling_mos(y1, y2)
            span_lst.append(y1)
            mos_lst.append(mos)
        plt.plot(span_lst, mos_lst)
        plt.yscale("log")
        plt.xlim(0,12)
        plt.show()

if __name__=="__main__":
    ### config data - INPUT HERE ###
    ribs = np.array([0, 0.47, 0.94, 1.35, 1.78, 2.06, 2.36, 2.61, 2.86, 3.28, 3.68, 4.2, 4.71, 5.44, 6.14, 6.8, 7.43, 8.03, 8.59, 9.13, 9.64, 10.12, 10.58, 11.02, 11.43, 11.82])
    t_lst = np.array([13.6e-3, 12.3e-3, 10.9e-3, 9.9e-3, 9.2e-3, 7.9e-3, 6.5e-3, 4.4e-3, 2.8e-3, 2e-3, 1.7e-3, 1.5e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    y_lst = np.array([0.94,1.78,2.36,2.86,3.68,4.71,6.14,7.43,8.59,9.13,9.64,12])

    #other input data
    a_stringer = (35*10**-3)**2
    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    n_stringers = lambda x: 6 if x<2.86 else 4 if x<4.2 else 2 if x<4.71 else 0
    m = 0.08
    mos_lst = []
    span_lst = []

    option1 = design_option_skin(a_stringer, n_stringers, ribs, t_lst, y_lst, t_f, t_r, m)
    option1.skin_buckling_mos_plot()