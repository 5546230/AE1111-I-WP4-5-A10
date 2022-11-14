import scipy as sp
import numpy as np
from scipy import integrate
from interpolation import get_Lspan 
from matplotlib import pyplot as plt

step = 0.01
y_axis=np.linspace(0.1,12,100)
Lspan = get_Lspan(y_axis)



plt.plot(y_axis, Lspan)
plt.show()

