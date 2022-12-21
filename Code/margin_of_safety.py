import numpy as np
from matplotlib import pyplot as plt
from column_buckling import design_option_column
from compressive_strength import design_option_compr
from spar_shear import get_mos
from load_case import LoadCase
from skin_stress import skin_stress

class design_option:
    def __init__(
        self,
        t_f: float,
        t_r: float,
        t_s,
        n_stringer: int,
        a_stringer: float,
        load: LoadCase,
        lenghts: list[float]
    ):
        self.t_f = t_f
        self.t_r = t_r
        self.t_s = t_s
        self.n_stringer = n_stringer
        self.a_stringer = a_stringer
        self.load = load
        self.lenghts = lenghts

    def plot_mos(self):
        y_axis = np.linspace(0,12)
        
        column_class = design_option_column(self.a_stringer, self.n_stringer, 10, self.lenghts, self.t_s, self.t_f, self.t_r)
        compr_class = design_option_compr(self.a_stringer, self.n_stringer, 10, self.t_f, self.t_r, self.t_s, 1, self.load)

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
    m = 0.08
    a_stringer = (35*10**-3)**2
    n = 2
    t_f = 5.5*10**-3 #m
    t_r = 4*10**-3 #m
    t_s = lambda x: 1.5e-3 if x>9.64 else 1.7e-3 if x>9.13 else 2e-3 if x>8.59 else 2.8e-3 if x>7.43 else 4.4e-3 if x>6.14 else 6.5e-3 if x>4.71 else 7.9e-3 if x>3.68 else 9.2e-3 if x>2.86 else 9.9e-3 if x>2.36 else 10.9e-3 if x>1.78 else 12.3e-3 if x> 0.94 else 13.6e-3

    a = 4.5

    ribs_list = np.array([0.47, 0.94, 1.35, 1.78, 2.06, 2.36, 2.61, 2.86, 3.28, 3.68, 4.2, 4.71, 5.44, 6.14, 6.8, 7.43, 8.03, 8.59,12])
    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
    option = design_option(t_f, t_r, t_s, n, m*a_stringer, load, lengths)
    option.plot_mos()

if __name__ =="__main__":
    main()