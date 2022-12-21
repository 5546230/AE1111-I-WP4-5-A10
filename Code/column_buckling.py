import numpy as np
from matplotlib import pyplot as plt
from skin_stress import skin_stress
import scipy as sp
from scipy import interpolate
from load_case import LoadCase

class design_option_column:
    '''a class for column buckling of the stringers for a design option'''
    def __init__(self, a_stringer: float, n_stringers, a_t: float, lengths: list, t_s, t_f: float, t_r: float):
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
            stress = skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1)
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

        critical = self.critical_stress(y_axis)

        actual = []
        for y in y_axis:
            if self.critical_stress(y)/skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1) < 1:
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
            actual.append(skin_stress(y, self.t_f, self.t_r, self.t_s(y), self.a_stringer, self.load, self.n_stringers(y), 1))
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
        # option = 3-(self.n_stringers==2)
        # name = f"./Figures/mos_col_option_{option}.svg"
        plt.show()
        #save the plot
        # plt.savefig(name, format="svg")

        # #clear the plot
        # plt.cla()

def main():
    m = 0.08
    a_stringer = (35*10**-3)**2
    n = lambda x:4
    t_f = 5.5*10**-3 #m
    t_r = 4*10**-3 #m

    t_lst = [13.6e-3, 12.3e-3, 10.9e-3, 9.9e-3, 9.2e-3, 7.9e-3, 6.5e-3, 4.4e-3, 2.8e-3, 2e-3, 1.7e-3, 1.5e-3]
    y_lst = [0.94,1.78,2.36,2.86,3.68,4.71,6.14,7.43,8.59,9.13,9.64,12]
    t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")

    ribs_list = np.array([0.47, 0.94, 1.35, 1.78, 2.06, 2.36, 2.61, 2.86, 3.28, 3.68, 4.2, 4.71, 5.44, 6.14, 6.8, 7.43, 8.03, 8.59, 9.13,12])
    lengths = np.zeros(len(ribs_list))
    for i in range(0,len(ribs_list)):
        if i == 0:
            lengths[i] = ribs_list[i]
        else:
            lengths[i] = ribs_list[i]-ribs_list[i-1]
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)    #define option 2
    option_2 = design_option_column(m*a_stringer, n, 10, lengths,t_s,t_f,t_r)
    #define option 3

    #generate the plots
    option_2.generate_plot()
    # option_3.generate_plot()

if __name__=="__main__":
    main()