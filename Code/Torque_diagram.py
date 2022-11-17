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
    alpha = 1/180*np.pi
    v= 200
    rho = 0.25
    torque_diagram(alpha, v, rho)