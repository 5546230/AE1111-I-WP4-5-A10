import scipy as sp
import numpy as np
from scipy import integrate
from interpolation import get_Lspan 
from matplotlib import pyplot as plt

#calculate the values
steps = 100
b = 11.98
y_axis=np.linspace(0.1,b,steps)
Lspan = get_Lspan(y_axis)
bending_moment =[]
for i in y_axis:
    bending_moment_val, error_bend = sp.integrate.quad(get_Lspan,i,b)
    bending_moment.append(bending_moment_val)


#plot the values 
fig, (ax1,ax2) = plt.subplots(2)
ax1.plot(y_axis, Lspan)
ax1.set_title("Lift Distirbution")
ax2.plot(y_axis, bending_moment)
ax2.set_title("Bending Moment Distirbution")
plt.show()

