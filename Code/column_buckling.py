import numpy as np
from matplotlib import pyplot as plt
from skin_stress import skin_stress
import scipy as sp
from scipy import interpolate
from load_case import LoadCase

class design_option_column:
    '''a class for column buckling of the stringers for a design option'''
    def __init__(self, a_stringer: float, n_stringers: int, a_t: float, lengths: list, t_s: float, t_f: float, t_r: float):
        #define the variables
        self.a_stringer = a_stringer
        self.n_stringers = n_stringers
        self.a = np.sqrt(a_stringer*a_t/2)
        self.t_s = t_s
        self.t_f = t_f
        self.t_r = t_r
        self.load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

        #check if lengths were specified
        if lengths is None:
            self.lengths = self.calc_lengths()
        else:
            self.lengths = np.array(lengths)


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
        '''calculates the required lengths of the stringers'''
        #define the variables
        k = 4
        e = 68e9

        #initialize the variables
        rib_lengths = []
        y = 0

        #find the lengths
        while y<12:
            stress = skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringers, 1)
            if not y:
                print(stress)
            length = np.sqrt(k * np.pi**2*e*self.a**2 / (6*stress))
            rib_lengths.append(length)

            #update the y coordinate
            y+=length

        return np.array(rib_lengths)

    def crit_stress(self) -> float:
        '''calculates the critical stress'''
        #define the variables
        k = 4
        e = 68e9

        #calculate the critical stress
        crit_stress = k * np.pi**2*e*self.a**2 / (6*self.lengths**2)

        #return the critical stress
        return crit_stress
    
    def test(self) -> bool:
        '''tests whether the design option satisfies the column buckling requirement'''
        y_axis = np.linspace(0,12,100)

        for y in y_axis:
            if skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringers, 1) < 1:
                return False
        return True
    
    def generate_plot(self):
        '''generates the plot of the margin of safety for column buckling'''
        #define the y-axis
        y_axis = np.linspace(0,12,1000)

        #calculate the critical stress
        critical = self.critical_stress(y_axis)

        #calculate the actual stress at each y location
        actual = []
        for y in y_axis:
            actual.append(skin_stress(y, self.t_f, self.t_r, self.t_s, self.a_stringer, self.load, self.n_stringers, 1))
        actual = np.array(actual)

        #calculate the factor
        factor = critical/actual

        #plot the values
        plt.plot(y_axis, factor)
        plt.yscale("log")
        plt.xlim(0,12)
        plt.ylim(1)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        plt.grid(1)

        #define the name of the file
        option = 3-(self.n_stringers==2)
        name = f"./Figures/mos_col_option_{option}.svg"

        #save the plot
        plt.savefig(name, format="svg")

        #clear the plot
        plt.cla()

def main():
    #define option 2
    option_2 = design_option_column((0.045**2), 14, 10, None,5.7e-3,5.5e-3,4e-3)
    #define option 3
    option_3 = design_option_column((0.001225), 4, 10, None,5e-3,5.5e-3,4e-3)

    #generate the plots
    option_2.generate_plot()
    # option_3.generate_plot()

if __name__=="__main__":
    main()