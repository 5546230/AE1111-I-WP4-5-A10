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

        self.torque_calc()
        
    def z2_force(self, y: float, alpha=0) -> float:
        '''get the forces in the z direction of the wingbox at a location y along the span'''
        return -(get_Lspan(y, self.alpha+alpha, self.v, self.rho) - get_Weight(y)*self.n)*np.cos(self.alpha+alpha)- get_dispan(y, self.alpha+alpha, self.v, self.rho)*np.sin(self.alpha+alpha)
    

    def z2_shear_calc(self)->None:
        '''generates the shear function in z direction'''
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.z2_force, y, 11.98)
            shear.append(shear_val)

        #generating the function for shear by interpolation
        self.z2_shear = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")

    def z2_moment_calc(self)->None:
        '''generates the bending moment function'''
        y_axis = np.linspace(0,11.98, 100)
        shear = []
        for y in y_axis:
            shear_val, _= sp.integrate.quad(self.z2_shear, y, 11.98)
            shear.append(-shear_val)
        
        self.z2_moment = sp.interpolate.interp1d(y_axis, shear, kind="cubic", fill_value="extrapolate")


    def z2_shear_diagram(self)-> None:
        '''generates the shear diagram'''
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.z2_shear(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Shear force [N]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Vertical shearforce diagram")
        plt.show()


    def z2_moment_diagram(self)-> None:
        '''generates the moment diagram'''
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.z2_moment(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Bending moment [Nm]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Bending moment diagram")
        plt.show()

    def x2_moment_diagram(self)-> None:
        '''generates the moment diagram'''
        y_axis = np.linspace(0,11.98,100)
        x_axis = self.x2_moment(y_axis)

        plt.plot(y_axis, x_axis)
        plt.ylabel("Moment in z-axis force [Nm]")
        plt.xlabel("Spanwise location [m]")
        plt.title("Moment in z-axis diagram")
        plt.show()

    def torque_calc(self)->None:
        y_axis = np.linspace(0,11.98, 100)
        torque = []
        for y in y_axis:
            torque_val, _= sp.integrate.quad(get_mspan, y, 11.98, args=(self.alpha, self.v, self.rho))
            torque.append(torque_val)
        
        self.torque = sp.interpolate.interp1d(y_axis, torque, kind="linear", fill_value="extrapolate")


    def torque_diagram(self)-> None:
        '''generates the torque diagram'''
        torque_diagram(self.alpha, self.v, self.rho)

    def diagram(self)-> None:
        '''generates the diagrams'''
        y_axis = np.linspace(0,11.98,100)
        z_shear = self.z2_shear(y_axis)
        bending_moment = self.z2_moment(y_axis)
        m_span = []


        for y in (y_axis):
            m_span_val, error = sp.integrate.quad(get_mspan, y, 11.98, args = (self.alpha, self.v, self.rho))
            m_span.append(m_span_val)

        fig, axs = plt.subplots(3, sharex=True)

        fig.suptitle(f"Load case for n = {self.n:.2f}, v = {self.v:.2f} [m/s], W = {self.w:.2f} [N] and h = {self.h:.2f} [m]")
        fig.set_figheight(8)
        fig.set_figwidth(8)

        axs[0].plot(y_axis, z_shear, )
        # axs[0].set_title("Shear force diagram")
        axs[0].set_ylabel("Shear force [N]")
        axs[0].set_xbound(0,12)
        axs[0].set_ybound(np.min(z_shear)*1.1,np.max(z_shear)*1.1)
        axs[0].grid(True)

        axs[1].plot(y_axis, bending_moment)
        # axs[1].set_title("Bending moment diagram")
        axs[1].set_ylabel("Bending moment [Nm]")
        axs[1].set_xbound(0,12)
        axs[1].set_ybound(np.min(bending_moment)*1.1,np.max(bending_moment)*1.1)
        axs[1].grid(True)

        axs[2].plot(y_axis, m_span)
        # axs[2].set_title("Torque diagram")
        axs[2].set_ylabel("Torque [Nm]")
        axs[2].set_xlabel("Spanwise location [m]")
        axs[2].set_xbound(0,12)
        axs[2].set_ybound(np.min(m_span)*1.1,np.max(m_span)*1.1*np.max(m_span)>0)
        axs[2].grid(True)
        
        # plt.show()
        plt.savefig("Positive_load_factor.svg", format="svg", transparent = True)

if __name__=="__main__":
    # load1_1 = LoadCase(2.62, 9318.5*9.80665, 49.94, 0)
    # load1_2 = LoadCase(2.62, 16575.6*9.80665, 66.6, 0)
    # load1_3 = LoadCase(2.62, 10328.5*9.80665, 52.57, 0)
    # load2_1 = LoadCase(2.62, 9318.5*9.80665, 117.28, 12500)
    load2_2 = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
    # load2_3 = LoadCase(2.62, 10328.5*9.80665, 132.47, 12500)
    # load3_1 = LoadCase(-1.5, 16575.6*9.80665, 156.42, 12500)


    # load1_1.diagram()
    # load1_2.diagram()
    # load1_3.diagram()
    # load2_1.diagram()
    load2_2.diagram()
    # load3_1.diagram()
    # load2_3.diagram()