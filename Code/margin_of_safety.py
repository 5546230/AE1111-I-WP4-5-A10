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
        t_lst: list[float],
        y_lst: list[float],
        n_stringer,
        a_stringer: float,
        load: LoadCase,
        ribs: list[float]
    ):
        self.t_f = t_f
        self.t_r = t_r
        self.t_lst = t_lst
        self.y_lst = y_lst
        self.t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")
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
        y_axis = np.append(y_axis, self.y_lst)
        y_axis = np.sort(y_axis)
        
        column_class = design_option_column(self.a_stringer, self.n_stringer, 10, self.lengths, self.t_s, self.t_f, self.t_r)
        compr_class = design_option_compr(self.a_stringer, self.n_stringer, 10, self.t_f, self.t_r, self.t_s, 1, self.load)
        # skin_class = design_option_skin(self.a_stringer, self.n_stringer, self.ribs, self.t_lst, self.y_lsts, self.t_f, self.t_r, 1)

        mos= []
        for y in y_axis:
            mos_col = column_class.critical_stress(y)/skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringer(y), 1)
            mos_compr_f = compr_class.mos_front(y)
            mos_compr_r = compr_class.mos_rear(y)
            mos_compr_s = compr_class.mos_skin(y)
            mos_compr_str = compr_class.mos_stringer(y)
            mos_shear_front = get_mos(y, self.load, 1)
            mos_shear_rear = get_mos(y, self.load, 0)

            mos.append(np.min([mos_col, mos_compr_f, mos_compr_r, mos_compr_s, mos_compr_str, mos_shear_front, mos_shear_rear]))
        mos = np.array(mos)
        for y in self.y_lst:
            if y ==12:
                continue
            index = np.where(y_axis==y)[0]
            for i in index:
                mos[i]=1

        plt.plot(y_axis, mos)
        plt.xlim(0,12)
        plt.ylim(1)
        plt.yscale('log')
        plt.grid(True)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        name = f"./Figures/MoS_design.svg"
        plt.savefig(name, format="svg", transparent=True)
        plt.cla()



def main():
    ### config data - INPUT HERE ###
    m = 0.362
    n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
    t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])
    

    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    #other input data
    a_stringer = (35*10**-3)**2
    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
    option = design_option(t_f, t_r, t_lst, y_lst, n, m*a_stringer, load, ribs_list)
    option.plot_mos()

if __name__ =="__main__":
    main()