from Weight_diagram import get_Weight
from interpolation import get_Lspan
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

def shear_diagram(alpha, v, rho):
    y_axis = np.linspace(0.5,11.98, 100)


    def get_resultant(y: float) -> float:
        '''get the resultant force'''
        return get_Lspan(y,alpha, v, rho)-get_Weight(y)


    shear = []
    for y in y_axis:
        shear_val, error = sp.integrate.quad(get_resultant, y, 11.98)
        shear.append(shear_val)

    plt.plot(y_axis, shear)# get_resultant(y_axis))
    plt.title("Shear force diagram")
    plt.ylabel("bla [N]")
    plt.xlabel("bla location [m]")
    plt.show()

if __name__=="__main__":
    alpha = 1/180*np.pi
    v= 200
    rho = 0.25
    shear_diagram(alpha, v, rho)