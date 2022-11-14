import scipy as sp
import numpy as np
from scipy import integrate
from interpolation import get_Lspan 
from matplotlib import pyplot as plt

steps = 100
y_axis=np.linspace(0.1,12,steps)
Lspan = get_Lspan(y_axis)
bending_moment = Lspan*y_axis

fig, (ax1,ax2) = plt.subplots(2)
ax1.plot(y_axis, Lspan)
ax1.set_title("Lift Distirbution")
ax2.plot(y_axis, bending_moment)
ax2.set_title("Bending Moment Distirbution")
plt.show()

