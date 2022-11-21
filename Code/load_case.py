from ISA import ISA_rho
from interpolation import get_alpha, get_Lspan, get_dispan
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
        self.x2_shear_calc()
    
    def z2_force(self, y: float) -> float:
        return (get_Lspan(y, self.alpha, self.v, self.rho) - get_Weight(y))*np.cos(self.alpha)#+ get_dispan(y, self.alpha, self.v, self.rho)*np.sin(self.alpha)
    
    def x2_force(self, y: float) -> float:
        return -(get_Lspan(y, self.alpha, self.v, self.rho) - get_Weight(y))*np.sin(self.alpha)#+ get_dispan(y, self.alpha, self.v, self.rho)*np.cos(self.alpha)

    def z2_shear_calc(self)->None:
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.z2_force, y, 11.98)
            shear.append(-shear_val)

        self.z2_shear = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")

    def x2_shear_calc(self)->None:
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.x2_force, y, 11.98)
            shear.append(-shear_val)
        
        self.x2_shear = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")

    def z2_shear_diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.z2_shear(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Shear force [N]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Vertical shearforce diagram")
        plt.show()

    def x2_shear_diagram(self)-> None:
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.x2_shear(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Shear force [N]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Horizontal shearforce diagram")
        plt.show()

    def torque_diagram(self)-> None:
        torque_diagram(self.alpha, self.v, self.rho)

load1 = LoadCase(1, 162550, 200, 12500)
load1.z2_shear_diagram()