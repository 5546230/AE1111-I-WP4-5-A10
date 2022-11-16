import numpy as np
from matplotlib import pyplot as plt
from interpolation import get_Lspan

y_axis = np.linspace(0.5,11.98, 1000)
L_span = get_Lspan(y_axis,10/180*np.pi,10,1.225)

plt.plot(y_axis, L_span)
plt.title("Spanwise lift distribution")
plt.ylabel("Lift [N]")
plt.xlabel("Spanwise location [m]")
plt.show()