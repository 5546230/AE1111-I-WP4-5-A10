from Weight_diagram import get_Weight
from interpolation import get_Lspan
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

def get_shear(alpha, v, rho):
    y_axis = np.linspace(0.5,11.98, 100)


    def get_resultant(y: float) -> float:
        '''get the resultant force'''
        return get_Lspan(y,alpha, v, rho)-get_Weight(y)


    shear = []
    for y in y_axis:
        shear_val, error = sp.integrate.quad(get_resultant, y, 11.98)
        shear.append(shear_val)
   
    return shear

# def moment_diagram(alpha, v, rho):
#     y_axis = np.linspace(0.5, 11.98, 100)
    
#     shear = get_shear(alpha, v, rho)

#     moment = []
#     for y in y_axis:
#         moment_val, error = sp.integrate.quad(shear, y, 11.98)
#         moment.append(moment_val)

#     plt.plot(y_axis, moment)# get_resultant(y_axis))
#     plt.title("Bending moment diagram")
#     plt.ylabel("bla [Nm]")
#     plt.xlabel("bla location [m]")
#     plt.show()

    
# if __name__=="__main__":
#     alpha = 1/180*np.pi
#     v= 200
#     rho = 0.25
#     moment_diagram(alpha, v, rho)