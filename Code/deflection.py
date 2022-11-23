from Moment_of_inertia import get_ixx
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate

def get_deflection(y, load):
    moment = load.z2_moment(y)
    ixx = get_ixx(y)
    E = 68e9
    return (-moment/(E*ixx))

load = LoadCase(2.2390, 16575.6*9.80665, 289.223, 0)

y_axis = np.linspace(0,11.98,100)
defl = []
for y in y_axis:
    defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= load)
    defl.append(defl_val)

defl_func = sp.interpolate.interp1d(y_axis, defl, kind="cubic", fill_value="extrapolate")

deflection, _ = sp.integrate.quad(defl_func, 0, 11.98)

print(deflection)