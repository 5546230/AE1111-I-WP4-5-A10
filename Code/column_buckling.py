import numpy as np
from matplotlib import pyplot as plt
from skin_stress import skin_stress
import scipy as sp
from scipy import interpolate
from load_case import LoadCase

class design_option_column:
    def __init__(self, a_stringer: float, n_stringers: float, a_t: float, lengths: list, t_s: float, t_f: float, t_r: float):
        #define the variables
        self.a_stringer = a_stringer
        self.n_stringers = n_stringers
        self.a = np.sqrt(a_stringer*a_t/2)
        self.t_s = t_s
        self.t_f = t_f
        self.t_r = t_r
        self.load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
        if lengths == None:
            self.lengths = self.calc_lengths()
        else:
            self.lengths = lengths


        #calculate the y coordinate of the ribs
        self.ribs = []
        for i in range(len(self.lengths)):
            self.ribs.append(np.sum(self.lengths[:i+1]))

        #get the critical stresses
        crit_stress = self.crit_stress()

        #interpolate the critical stresses
        if len(self.lengths)==1:
            crit_stress = np.append(crit_stress, crit_stress)
            self.ribs = np.append(self.ribs, self.ribs[0]+1)

        self.critical_stress = sp.interpolate.interp1d(self.ribs, crit_stress, kind = "next", fill_value="extrapolate")

    def calc_lengths(self) -> list:
        #define the variables
        k = 4
        e = 68e9

        #calculate the length of each rib
        rib_lengths = []
        y = 0

        #find the lengths
        while y<12:
            stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringers, 1)
            length = np.sqrt(k * np.pi**2*e*self.a**2 / (6*stress))
            rib_lengths.append(length)
            y+=length

        return np.array(rib_lengths)

    def crit_stress(self) -> float:
        #define the variables
        k = 4
        e = 68e9

        #calculate the critical stress
        crit_stress = k * np.pi**2*e*self.a**2 / (6*self.lengths**2)

        #return the critical stress
        return crit_stress
    
    def generate_plot(self):
        y_axis = np.linspace(0,12,100)
        critical = self.critical_stress(y_axis)
        actual = []
        for y in y_axis:
            actual.append(skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringers, 1))
        actual = np.array(actual)
        factor = critical/actual
        plt.plot(y_axis, factor)
        plt.yscale("log")
        plt.xlim(0,12)
        plt.ylim(1)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        plt.grid(1)
        option = 3-(self.n_stringers==2)
        name = f"./Figures/mos_col_option_{option}.svg"
        plt.savefig(name, format="svg")
        plt.cla()

def main():
    option_2 = design_option_column((0.012675), 2, 10, None,8e-3,5.5e-3,4e-3)
    # print(option_2.lengths)
    option_3 = design_option_column((0.001225), 4, 10, None,8e-3,5.5e-3,4e-3)
    # print(option_3.lengths)

    option_2.generate_plot()
    option_3.generate_plot()

if __name__=="__main__":
    main()