import numpy as np
from matplotlib import pyplot as plt
from interpolation import get_Lspan
import scipy as sp

y_axis = np.linspace(0.5,11.98, 1000)
L_span = get_Lspan(y_axis,10/180*np.pi,10,1.225)
print(sp.integrate.quad(get_Lspan, 0, 11.98, args=(1/180*np.pi, 200, 0.287446962
)))
plt.plot(y_axis, L_span)
plt.title("Spanwise lift distribution")
plt.ylabel("Lift [N]")
plt.xlabel("Spanwise location [m]")
plt.show()