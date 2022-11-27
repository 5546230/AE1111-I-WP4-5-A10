from Moment_of_inertia import get_J, get_zcentroid
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from interpolation import get_mspan, get_Lspan
from matplotlib import pyplot as plt


def get_twist(y: float, load: LoadCase, t: float, alpha: float) -> float:
    '''the relation between the twist angle, polar moment of inertia and the torque'''

    #get the pitching moment
    torque = get_mspan(y, load.alpha+alpha, load.v, load.rho)

    #include the torque created by the lift on the wingbox
    lift = -load.z2_force(y, load.alpha+alpha)
    z_centroid = get_zcentroid(y, t)
    torque_tot = torque + lift * (z_centroid-0.25*(3.49-3.49*(1-0.372)/12*y) )

    J = get_J(y, t)
    G = 68e9*3/8

    return (-torque_tot/(G*J))

def get_t() -> tuple:
    '''optimisation algortithm for the minimum thickness for torque'''
    load = LoadCase(2.62, 16575.6*9.80665, 250.79, 12500)
    y_axis = np.linspace(0,11.98,100)
    t=1.5e-3

    #start a maximum of 100 iterations
    for iteration in np.arange(100):
        twist = [0]

        #calculate twist for each y value
        for i in np.arange(100):
            #get the twist value and include the extra angle of attack due to twist
            twist_val, _ = sp.integrate.quad(get_twist, 0, y_axis[i], args=(load,t, twist[i-1]))
            twist.append(twist_val)
        
        #check if twist between limits
        if twist[-1]<=9.5/180*np.pi and twist[-1]>=9.49/180*np.pi:
            return t, np.array(twist)/np.pi*180
        
        #update the thickness for next iteration
        t=t*twist[-1]/(9.5/180*np.pi)


def diagram(t:float):        
    twist = [0]
    y_axis = np.linspace(0,11.98,101)
    load = LoadCase(2.62, 16575.6*9.80665, 250.79, 12500)
    t=1e-3
    #calculate twist for each y value
    for i in np.arange(100):
        #get the twist value and include the extra angle of attack due to twist
        twist_val, _ = sp.integrate.quad(get_twist, 0, y_axis[i], args=(load,t, twist[i-1]))
        twist.append(twist_val)

    #plot the graph    
    plt.plot(y_axis,twist)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Twist angle [deg]")
    plt.title(f"Twist angle for a thickness of {t*1e3:.1f} [mm]")
    plt.show()

if __name__=="__main__":
    diagram(1e-3)