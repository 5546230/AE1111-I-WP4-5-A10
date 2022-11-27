from Moment_of_inertia import get_ixx
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate

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
    t=1.5e-3
    for n in np.arange(99999):
        defl = []
        for y in y_axis:
            defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= (load, t))
            defl.append(defl_val)

        defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")

        deflection, _ = sp.integrate.quad(defl_func, 0, 11.98)

        if deflection>=-23.5*0.15 and deflection<=-23.5*0.149:
            return t, deflection
        t*=deflection/-23.5/0.15

t= get_t()    
print(t)

# load = LoadCase(2.2390, 16575.6*9.80665, 289.223, 0)

# y_axis = np.linspace(0,11.98,100)
# defl = []
# for y in y_axis:
#     defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= load)
#     defl.append(defl_val)

# defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")

# deflection, _ = sp.integrate.quad(defl_func, 0, 11.98)

# print(deflection)