from Weight_diagram import get_Weight
from interpolation import get_Lspan
import scipy as sp
import numpy as np
from matplotlib import pyplot as plt


y_axis = np.linspace(0.5,11.98, 1000)


def get_resultant(y):
    return get_Lspan(y,1/180*np.pi,200, 0.287446962)-get_Weight(y)

shear = []
for y in y_axis:
    shear_val, error = sp.integrate.quad(get_resultant, y, 11.98)
    shear.append(shear_val)

plt.plot(y_axis, shear)# get_resultant(y_axis))
plt.title("Shear force diagram")
plt.ylabel("bla [N]")
plt.xlabel("bla location [m]")
plt.show()