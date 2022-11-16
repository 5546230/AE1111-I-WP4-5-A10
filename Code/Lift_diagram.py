import numpy as np
from matplotlib import pyplot as plt
from interpolation import get_Lspan

y_axis = np.linspace(0,11.98, 100)
L_span = get_Lspan(y_axis)

plt.plot(y_axis, L_span)
plt.title("Spanwise lift distribution")
plt.ylabel("Lift [N]")
plt.xlabel("Spanwise location [m]")
plt.show()