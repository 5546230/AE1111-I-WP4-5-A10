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
v= 10                   #[m/s]
rho = 1.225             #[m/s}
q = 0.5* rho *v**2      #[Pa]

#interpolation functions
get_c = sp.interpolate.interp1d(ylst, clst, kind="linear", fill_value="extrapolate")

get_cl = sp.interpolate.interp1d(ylst, Cllst, kind="cubic", fill_value="extrapolate")

get_cdi = sp.interpolate.interp1d(ylst, Cdilst, kind="cubic", fill_value="extrapolate")

get_cm = sp.interpolate.interp1d(ylst, Cmlst, kind="cubic", fill_value="extrapolate")


#aerodynamic forces functions
def get_Lspan(y):
    return 0.5*rho*v**2*get_cl(y)*get_c(y)

def get_mspan(y):
    return 0.5*rho*v**2*get_cl(y)*get_c(y)**2

def get_dispan(y):
    return 0.5*rho*v**2*get_cl(y)*get_c(y)

estimate_l, error_l = sp.integrate.quad(get_Lspan,0,12)
estimate_S, error_s = sp.integrate.quad(get_c, 0,12)
estimate_cl = estimate_l/(q*estimate_S)

# y = np.linspace(0.5,12,100)
# Lspan = get_Lspan(y)
# plt.plot(y,Lspan)
# plt.show()