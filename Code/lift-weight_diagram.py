import scipy as sp
import numpy as np
from scipy import integrate
from interpolation import get_Lspan 
from matplotlib import pyplot as plt


#commented lines are for plotting the lift for the whole span
step = 0.01
y_axis_Lift1 = np.linspace(0.1,12,100)
#y_axis_Lift2 = np.linspace(-12,-0.1,100)
Lspan1 = get_Lspan(y_axis_Lift1)
#Lspan2 = get_Lspan(y_axis_Lift2)

#plot of the lift distribution
plt.plot(y_axis_Lift1, Lspan1)
#plt.plot(y_axis_Lift2, Lspan2)
plt.show()

