from ISA import ISA_rho
from interpolation import get_alpha, get_Lspan, get_dispan, get_mspan
from Torque_diagram import torque_diagram
from Weight_diagram import get_Weight
import numpy as np
import scipy as sp
from scipy import interpolate
from matplotlib import pyplot as plt


class LoadCase:
    def __init__(self, n: float, W: float, v: float, h: float) -> None:
        self.n = n
        self.w = W
        self.l = 1.1*W*n
        self.h = h
        self.v = v
        self.s = 57.418137

        #define flow conditions
        self.rho = ISA_rho(self.h)
        self.cld = self.l/(0.5*self.rho*self.v**2*self.s)
        self.alpha = get_alpha(self.cld)

        #get shear functions
        self.z2_shear_calc()

        #get mometn functions
        self.z2_moment_calc()
    
    def z2_force(self, y: float) -> float:
        return -(get_Lspan(y, self.alpha, self.v, self.rho) - get_Weight(y))*np.cos(self.alpha)- get_dispan(y, self.alpha, self.v, self.rho)*np.sin(self.alpha)
    

    def z2_shear_calc(self)->None:
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.z2_force, y, 11.98)
            shear.append(shear_val)

        self.z2_shear = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")

    def z2_moment_calc(self)->None:
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.z2_shear, y, 11.98)
            shear.append(-shear_val)
        
        self.z2_moment = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")


    def z2_shear_diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.z2_shear(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Shear force [N]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Vertical shearforce diagram")
        plt.show()


    def z2_moment_diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.z2_moment(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Bending moment [Nm]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Bending moment diagram")
        plt.show()

    def x2_moment_diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.x2_moment(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Moment in z-axis force [Nm]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Moment in z-axis diagram")
        plt.show()

    def torque_diagram(self)-> None:
        torque_diagram(self.alpha, self.v, self.rho)

    def diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        z_shear = self.z2_shear(y_axis)
        bending_moment = self.z2_moment(y_axis)
        torque = get_mspan(y_axis, self.alpha, self.v, self.rho)


        fig, axs = plt.subplots(3, sharex=True)

        fig.suptitle(f"Load case for n = {self.n:.2f}, v = {self.v:.2f} [m/s], W = {self.w:.2f} [N] and h = {self.h:.2f}")

        axs[0].plot(y_axis, z_shear)
        axs[0].set_title("Shear force diagram")

        axs[1].plot(y_axis, bending_moment)
        axs[1].set_title("Bending moment diagram")

        axs[2].plot(y_axis, torque)
        axs[2].set_title("Torque diagram")

        plt.show()

if __name__=="__main__":
    # load1_1 = LoadCase(2.3367, 9318.5*9.80665, 289.223, 0)
    load1_2 = LoadCase(2.2390, 16575.6*9.80665, 289.223, 0)
    # load1_3 = LoadCase(2.3156, 10328.5*9.80665, 289.223, 0)
    # load2_1 = LoadCase(2.3367, 9318.5*9.80665, 250.786, 0)
    # load2_2 = LoadCase(2.2390, 16575.6*9.80665, 250.786, 0)
    # load2_3 = LoadCase(2.3156, 10328.5*9.80665, 250.786, 0)

    # load1_1.diagram()# = LoadCase(2.3367, 9318.5*9.80665, 289.223, 0)
    load1_2.diagram()# = LoadCase(2.2390, 16575.6*9.80665, 289.223, 0)
    # load1_3.diagram()# = LoadCase(2.3156, 10328.5*9.80665, 289.223, 0)
    # load2_1.diagram()# = LoadCase(2.3367, 9318.5*9.80665, 250.786, 0)
    # load2_2.diagram()# = LoadCase(2.2390, 16575.6*9.80665, 250.786, 0)
    # load2_3.diagram()# = LoadCase(2.3156, 10328.5*9.80665, 250.786, 0)