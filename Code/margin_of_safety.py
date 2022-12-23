import numpy as np
from matplotlib import pyplot as plt
from column_buckling import design_option_column
from compressive_strength import design_option_compr
from skin_buckling import design_option_skin
from spar_shear import get_mos
from load_case import LoadCase
from skin_stress import skin_stress
import scipy as sp

class design_option:
    def __init__(
        self,
        t_f: float,
        t_r: float,
        t_s,
        n_stringer,
        a_stringer: float,
        load: LoadCase,
        ribs: list[float]
    ):
        self.t_f = t_f
        self.t_r = t_r
        self.t_s = t_s
        self.n_stringer = n_stringer
        self.a_stringer = a_stringer
        self.load = load
        self.ribs = ribs
        self.lengths = np.zeros(len(ribs))
        for i in range(0,len(ribs)):
            if i == 0:
                self.lengths[i] = ribs[i]
            else:
                self.lengths[i] = ribs[i]-ribs[i-1]

    def plot_mos(self):
        y_axis = np.linspace(0,12)
        
        column_class = design_option_column(self.a_stringer, self.n_stringer, 10, self.lenghts, self.t_s, self.t_f, self.t_r)
        compr_class = design_option_compr(self.a_stringer, self.n_stringer, 10, self.t_f, self.t_r, self.t_s, 1, self.load)
        skin_class = design_option_skin(self.a_stringer, self.n_stringer, self.ribs, )

        mos= []
        for y in y_axis:
            mos_col = column_class.critical_stress(y)/skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringer, 1)
            mos_compr_f = compr_class.mos_front(y)
            mos_compr_r = compr_class.mos_rear(y)
            mos_compr_s = compr_class.mos_skin(y)
            mos_compr_str = compr_class.mos_stringer(y)
            mos_shear_front = get_mos(y, self.load, 1)
            mos_shear_rear = get_mos(y, self.load, 0)
            #####add margin of safety for skin buckling######

            mos.append(np.min([mos_col, mos_compr_f, mos_compr_r, mos_compr_s, mos_compr_str, mos_shear_front, mos_shear_rear]))
        print(np.min(mos))
        plt.plot(y_axis, mos)
        plt.xlim(0,12)
        plt.ylim(1)
        plt.yscale('log')
        plt.grid(True)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        plt.show()




def main():
    ### config data - INPUT HERE ###
    ribs = np.array([0, 0.47, 0.94, 1.35, 1.78, 2.06, 2.36, 2.61, 2.86, 3.28, 3.68, 4.2, 4.71, 5.44, 6.14, 6.8, 7.43, 8.03, 8.59, 9.13, 9.64, 10.12, 10.58, 11.02, 11.43, 11.82])
    t_lst = np.array([13.6e-3, 12.3e-3, 10.9e-3, 9.9e-3, 9.2e-3, 7.9e-3, 6.5e-3, 4.4e-3, 2.8e-3, 2e-3, 1.7e-3, 1.5e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    y_lst = np.array([0.94,1.78,2.36,2.86,3.68,4.71,6.14,7.43,8.59,9.13,9.64,12])
    t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")
    #other input data
    a_stringer = (35*10**-3)**2
    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    n_stringers = lambda x: 6 if x<2.86 else 4 if x<4.2 else 2 if x<4.71 else 0
    m = 0.08
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
    option = design_option(t_f, t_r, t_s, n_stringers, m*a_stringer, load, ribs)
    option.plot_mos()

if __name__ =="__main__":
    main()