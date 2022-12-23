import numpy as np
from skin_stress import *
from load_case import LoadCase
from interpolation import *

class design_option_skin:
    def __init__(self, a_stringer: float, n_stringers, ribs: list, t_lst: list, y_lst: list, t_f: float, t_r: float, m: float):
        #define the variables
        self.a_stringer = a_stringer
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
        critical = stress_crit(y1, y2, self.t_lst[t_index], self.n_stringers(y1)//2, self.n_stringers(0), 1)[0]
        actual = av_skin_stress(y1, y2, self.t_f, self.t_r, self.t_lst[t_index], self.a_stringer, self.load, self.n_stringers(y1), self.m)

        K = stress_crit(y1, y2, self.t_lst[t_index], self.n_stringers(y1)//2, self.n_stringers(0), 1)[1]
        slenderness = stress_crit(y1, y2, self.t_lst[t_index], self.n_stringers(y1)//2, self.n_stringers(0), 1)[2]
        #print("c: ", get_c(y1))
        #print("\n", y1, y2, K, slenderness, self.t_lst[t_index], "Critical: ", critical, "Actual: ", actual, "\n")

        margin = critical/actual

        return margin

    def skin_buckling_mos_plot(self, option):
        for i in range(0, len(self.ribs)-1):
            y1 = self.ribs[i]
            y2 = self.ribs[i+1]
            mos = self.skin_buckling_mos(y1, y2)
            span_lst.append(y2)
            mos_lst.append(mos)
        name = f"./Figures/Option"+str(option)+"_MoS_SB.svg"
        plt.plot(span_lst, mos_lst)
        plt.ylim([0, 5])
        plt.xlim(0,12)
        plt.grid(1)
        plt.xlabel("Spanwise location [m]")
        plt.ylabel("Margin of Safety [-]")
        plt.savefig(name, format="svg")
        plt.show()

if __name__=="__main__":
    ### config data - INPUT HERE ###
    #OPTION1:
    #option = 1
    #m = 0.362
    #n = lambda x: 6 if x< 7.49 else 4 if x<8.7 else 2
    #ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 8.385, 8.7, 9.06, 9.435, 9.735, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])


    #OPTION2:
    option = 2
    m = 0.362
    n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
    t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])

    #OPTION3:
    # option = 3
    # m = 0.265
    # n = lambda x: 4 if x<8.62 else 2
    # ribs_list = np.array([0, 0.345, 0.69, 1.02, 1.35, 1.655, 1.96, 2.25, 2.535, 2.815, 3.09, 3.36, 3.63, 3.895, 4.155, 4.41, 4.665, 4.92, 5.175, 5.41, 5.645, 5.88, 6.115, 6.335, 6.555, 6.775, 6.995, 7.2, 7.405, 7.615, 7.825, 8.02, 8.215, 8.415, 8.62, 8.975, 9.34, 9.59, 9.85, 10.13, 12])
    # t_lst = np.array([13.3e-3, 12.5e-3, 11.4e-3, 10.4e-3, 10.0e-3, 9.5e-3, 9.2e-3, 8.7e-3, 7.7e-3, 6.8e-3, 6.0e-3, 5.3e-3, 7.0e-3, 4.8e-3])
    # y_lst = np.array([0.69, 1.35, 1.96, 2.535, 3.09, 3.63, 4.155, 5.175, 6.115, 6.995, 7.825, 8.62, 9.34, 12])

    #other input data
    a_stringer = (35*10**-3)**2
    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    mos_lst = []
    span_lst = []

    option1 = design_option_skin(a_stringer, n, ribs_list, t_lst, y_lst, t_f, t_r, m)
    option1.skin_buckling_mos_plot(option)

#OPTION1:
#n = 6 if x< 7.49 else 4 if x<8.7 else 2
    #m = 0.362
    #ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 8.385, 8.7, 9.06, 9.435, 9.735, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])
    #masses = [109, 86, 59, 49, 61, 48, 53, 47, 46, 49, 26, 61, 31, 73] -> 798kg
    #41 rib

# n = lambda x: 6 if x< 7.49 else 4 if x<8.7 else 2
# ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 8.385, 8.7, 9.06, 9.435, 9.735, 12])
# t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
# y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])





#OPTION2:
#n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    #m = 0.362
    #ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])
    #masses = [109, 86, 59, 49, 61, 48, 53, 47, 46, 49, 26, 27] -> 749 kg
    #46 rib

# n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
# ribs_list = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
# t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
# y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])

#OPTION3:
    # m = 0.265
    # n = lambda x: 4 if x<8.62 else 2
    # ribs_list = np.array([0, 0.345, 0.69, 1.02, 1.35, 1.655, 1.96, 2.25, 2.535, 2.815, 3.09, 3.36, 3.63, 3.895, 4.155, 4.41, 4.665, 4.92, 5.175, 5.41, 5.645, 5.88, 6.115, 6.335, 6.555, 6.775, 6.995, 7.2, 7.405, 7.615, 7.825, 8.02, 8.215, 8.415, 8.62, 8.975, 9.34, 9.59, 9.85, 10.13, 12])
    # t_lst = np.array([13.3e-3, 12.5e-3, 11.4e-3, 10.4e-3, 10.0e-3, 9.5e-3, 9.2e-3, 8.7e-3, 7.7e-3, 6.8e-3, 6.0e-3, 5.3e-3, 7.0e-3, 4.8e-3])
    # y_lst = np.array([0.69, 1.35, 1.96, 2.535, 3.09, 3.63, 4.155, 5.175, 6.115, 6.995, 7.825, 8.62, 9.34, 12])
    # masses = [98, 85, 70, 58, 53, 47, 43, 76, 59, 46, 37, 30, 30, 14, 50] -> 796kg
    # 39 ribs











##### Probably wrong, dont use:
#OPTION4:
# m = 0.204
# n = lambda x: 4 if x<4.86 else 2 if x< 8.13 else 0
# ribs_list=np.array([0, 0.33, 0.66, 1.13, 1.59, 2.04, 2.48, 2.91, 3.32, 3.72, 4.11, 4.49, 4.86, 5.23, 5.59, 5.94, 6.28, 6.61, 6.93, 7.24, 7.54, 7.84, 8.13, 8.69, 9.22, 9.72, 10.20, 10.66, 11.09, 11.50, 12])
# t_lst=np.array([13.4e-3, 12.7e-3, 11.1e-3, 9.6e-3, 8.2e-3, 6.9e-3, 6.0e-3, 5.0e-3, 4.0e-3, 3.2e-3, 2.6e-3, 2.3e-3, 2.0e-3, 2.0e-3, 2.0e-3])
# y_lst=np.array([0.66, 1.59, 2.48, 3.32, 4.11, 4.86, 5.59, 6.28, 6.93, 7.54, 8.13, 9.22, 10.20, 11.09, 12])
# masses = [94, 120, 96, 75, 58, 45, 35, 26, 19, 14, 11, 14, 10, 9, 7] -> 633kg
# 29 ribs