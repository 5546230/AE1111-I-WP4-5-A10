from Moment_of_inertia import get_J
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from interpolation import get_mspan
from matplotlib import pyplot as plt


def get_twist(y, load, t):
    torque = get_mspan(y, load.alpha, load.v, load.rho)
    J = get_J(y, t)
    G = 68e9*3/8
    return (-torque/(G*J))
def get_t():
    load = LoadCase(2.2390, 16575.6*9.80665, 289.223, 0)

    y_axis = np.linspace(0,11.98,100)
    t=1.5e-3

    for n in np.arange(100):
        twist = []
        for y in y_axis:
            twist_val, _ = sp.integrate.quad(get_twist, 0, y, args=(load,t))
            twist.append(twist_val)
        
        if twist[-1]<=9.5/180*np.pi and twist[-1]>=9/190*np.pi:
            return t
        t=t*twist[-1]/(9.5/180*np.pi)


# print(np.max(twist)/np.pi*180)
# plt.plot(y_axis,twist)
# plt.show()