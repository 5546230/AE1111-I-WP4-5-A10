import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

def get_Weight(y):
    return y 

y_axis = np.linspace(0,12,1000)
Weight=get_Weight(y_axis)


plt.plot(y_axis, Weight)
plt.title("Spanwise Weight distribution")
plt.xlabel("Spanwise location [m]")
plt.ylabel("Weight [N]")
plt.show()

