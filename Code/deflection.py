from Moment_of_inertia import get_ixx
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

def get_deflection(y: float, load: LoadCase, t:float) -> float:
    '''the relation between the moment, moment of inertia and the second derivative of the deflection'''
    moment = load.z2_moment(y)
    ixx = get_ixx(y, t)
    E = 68e9
    return (-moment/(E*ixx))

def get_t() -> tuple:
    '''calculate the minimum thickness for the deflection through an iterative process'''
    load = LoadCase(2.62, 16575.6*9.80665, 250.79, 12500)

    y_axis = np.linspace(0,11.98,100)
    t = 1.5e-3

    #start the iteration
    for iteration in np.arange(99999):
        #integrate twice to get the deflection
        defl = []
        for y in y_axis:
            defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= (load, t))
            defl.append(defl_val)

        #interpolate to be able to integrate again
        defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")

        deflection, _ = sp.integrate.quad(defl_func, 0, 11.98)

        #check if deflection within limits
        if deflection>=-23.5*0.15 and deflection<=-23.5*0.149:
            return t, deflection
        
        #update the thickness
        t*=deflection/-23.5/0.15

def diagram(t: float):
    '''Get a deflection diagram for a thickness of t'''
    defl = []
    y_axis = np.linspace(0,11.98,100)
    load = LoadCase(2.62, 16575.6*9.80665, 250.79, 12500)

    for y in y_axis:
        defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= (load, t))
        defl.append(defl_val)

    defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")
    defl_lst= []
    for y in y_axis:
        deflection, _ = sp.integrate.quad(defl_func, 0, y)
        defl_lst.append(deflection)

    plt.plot(y_axis, defl_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Deflection [m]")
    plt.title(f"Deflection for a thickness of {t*1e3:.1f} mm")
    plt.show()

if __name__=="__main__":
    # t= get_t()    
    # print(t)
    diagram(2.4*1e-3)