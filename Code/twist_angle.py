from Moment_of_inertia import get_J
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from Torque_diagram import m_span
from matplotlib import pyplot as plt


def get_twist(y):
    torque = m_span(y)
    J = get_J(y)
    G = 68e9*3/8
    return (-torque/(G*J))


y_axis = np.linspace(0,11.98,100)
twist = []
for y in y_axis:
    twist_val, _ = sp.integrate.quad(get_twist, 0, y)
    twist.append(twist_val)


plt.plot(y_axis,twist)
