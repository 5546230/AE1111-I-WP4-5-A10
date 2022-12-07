import numpy as np
import scipy as sp
from scipy import integrate
from interpolation import get_mspan
from matplotlib import pyplot as plt

def torque_diagram(alpha, v, rho):
    # find the values of the torque
    y_axis = np.linspace(0,11.98,100)
    m_span = []


    for y in (y_axis):
        m_span_val, error = sp.integrate.quad(get_mspan, y, 11.98, args = (alpha, v, rho))
        m_span.append(m_span_val)


    #Plot the values
    plt.plot(y_axis, m_span)
    plt.title("Torque distribution at quarter chord")
    plt.ylabel("Torque [Nm]")
    plt.xlabel("Spanwise location [m]")
    plt.show()


if __name__=="__main__":
    from load_case import LoadCase
    load = LoadCase(-1.5, 16575.6*9.80665, 156.42, 12500)

    torque_diagram(load.alpha, load.v, load.rho)