import numpy as np
import scipy as sp
from scipy import interpolate
from importing import get_lst
from matplotlib import pyplot as plt
from scipy import integrate

#get the uninterolated values
filename = "Data\MainWing_a=10.00_v=10.00ms.csv"
ylst, clst, ailst, Cllst, Cdilst, Cmlst = get_lst(filename)

#define flow conditions
v= 10#[m/s]
rho = 1.225#[m/s}

Lspanlst = 0.5*v**2*rho*Cllst*clst

#interplotion functions
get_c = sp.interpolate.interp1d(ylst, clst, kind="linear", fill_value="extrapolate")

get_cl = sp.interpolate.interp1d(ylst, Cllst, kind="cubic", fill_value="extrapolate")

get_cdi = sp.interpolate.interp1d(ylst, Cdilst, kind="cubic", fill_value="extrapolate")

get_cm = sp.interpolate.interp1d(ylst, Cmlst, kind="cubic", fill_value="extrapolate")

get_Lspan = sp.interpolate.interp1d(ylst, Lspanlst, kind="cubic", fill_value="extrapolate")

estimate_cl = sp.integrate.quad(Lspanlst,0,12)
print(estimate_cl)


# y = np.linspace(0.5,12,100)
# Lspan = get_Lspan(y)
# plt.plot(y,Lspan)
# plt.show()