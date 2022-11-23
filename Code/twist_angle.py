from Moment_of_inertia import get_J
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from interpolation import get_mspan
from matplotlib import pyplot as plt


def get_twist(y: float, load: LoadCase, t: float) -> float:
    '''the relation between the twist angle, polar moment of inertia and the torque'''
    torque = get_mspan(y, load.alpha, load.v, load.rho)
    J = get_J(y, t)
    G = 68e9*3/8
    return (-torque/(G*J))

def get_t() -> tuple:
    '''optimisation algortithm for the minimum thickness for torque'''
    load = LoadCase(2.62, 16575.6*9.80665, 156.42, 12500)
    y_axis = np.linspace(0,11.98,100)
    t=1.5e-3

    for n in np.arange(100):
        twist = []
        for y in y_axis:
            twist_val, _ = sp.integrate.quad(get_twist, 0, y, args=(load,t))
            twist.append(twist_val)
        
        if twist[-1]<=9.5/180*np.pi and twist[-1]>=9/190*np.pi:
            return t, twist[-1]/np.pi*180
        t=t*twist[-1]/(9.5/180*np.pi)

print(get_t())
# print(np.max(twist)/np.pi*180)
# plt.plot(y_axis,twist)
# plt.show()