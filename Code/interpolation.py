import numpy as np
import scipy as sp
from scipy import interpolate
from importing import get_lst
from matplotlib import pyplot as plt
from scipy import integrate

#get the uninterolated values
filename_0 = "Data\MainWing_a=0.00_v=10.00ms.csv"
filename_10 = "Data\MainWing_a=10.00_v=10.00ms.csv"
ylst, clst, ailst_0, Cllst_0, Cdilst_0, Cmlst_0 = get_lst(filename_0)
_,_, ailst_10, Cllst_10, Cdilst_10, Cmlst_10 = get_lst(filename_10)


#interpolation functions
get_c = sp.interpolate.interp1d(ylst, clst, kind="linear", fill_value="extrapolate")

get_cl_0 = sp.interpolate.interp1d(ylst, Cllst_0, kind="cubic", fill_value="extrapolate")

get_cdi_0 = sp.interpolate.interp1d(ylst, Cdilst_0, kind="cubic", fill_value="extrapolate")

get_cm_0 = sp.interpolate.interp1d(ylst, Cmlst_0, kind="cubic", fill_value="extrapolate")

get_cl_10 = sp.interpolate.interp1d(ylst, Cllst_10, kind="cubic", fill_value="extrapolate")

get_cdi_10 = sp.interpolate.interp1d(ylst, Cdilst_10, kind="cubic", fill_value="extrapolate")

get_cm_10 = sp.interpolate.interp1d(ylst, Cmlst_10, kind="cubic", fill_value="extrapolate")

cl_0 = 0.441429
cl_10 = 1.295089

cm_0 = -0.398281
cm_10 = -0.979889

cdi_0 = 0.006339
cdi_10 = 0.052246

def get_alpha(cld: float)-> float:
    sin = (cld-cl_0)/(cl_10-cl_0)*np.sin(10/180*np.pi)
    return np.arcsin(sin)

def get_Cl(y: float, alpha: float) -> float:
    '''get the cl distridution for a angle of attack in the range [0,10]'''
    cld = np.sin(alpha)/np.sin(1/18*np.pi)*(cl_10-cl_0)+cl_0
    out = get_cl_0(y) + (cld-cl_0)/(cl_10-cl_0)*(get_cl_10(y)- get_cl_0(y))
    return out

def get_Cm(y: float, alpha: float) -> float:
    '''get the cm distridution for aa desired cl, cld.'''
    cmd = np.sin(alpha)/np.sin(1/18*np.pi)*(cm_10-cdi_0)+cm_0
    out = get_cm_0(y) + (cmd-cm_0)/(cm_10-cm_0)*(get_cm_10(y)- get_cm_0(y))
    return out

def get_Cdi(y: float, alpha: float) -> float:
    '''get the cm distridution for aa desired cl, cld.'''
    cdid = np.sin(alpha)/np.sin(1/18*np.pi)*(cdi_10-cdi_0)+cdi_0
    out = get_cdi_0(y) + (cdid-cdi_0)/(cdi_10-cdi_0)*(get_cdi_10(y)- get_cdi_0(y))
    return out

def get_Lspan(y: float, alpha: float, v: float, rho: float) -> float:
    '''Returns the lift per unit span at spanwise location y. for angle of attack and velocity'''
    return 0.5*rho*v**2*get_Cl(y, alpha)*get_c(y)

def get_mspan(y: float, alpha: float, v: float, rho: float) -> float:
    '''Returns the pitching moment per unit span at spanwise location y. '''
    return 0.5*rho*v**2*get_Cm(y, alpha)*get_c(y)**2

def get_dispan(y: float, alpha: float, v: float, rho: float) -> float:
    '''Returns the induced drag per unit span at spanwise location y. '''
    return 0.5*rho*v**2*get_Cdi(y, alpha)*get_c(y)

alpha = 3/180*np.pi
v = 10
rho = 1.225
estimate_Lift, error_l = sp.integrate.quad(get_Lspan, 0.1,12, args = (alpha, v, rho))
estimate_S, error_s = sp.integrate.quad(get_c, 0,12)
estimate_cl = estimate_Lift/(0.5*rho*v**2*estimate_S)

# y = np.linspace(0.5,12,100)
# Lspan = get_Lspan(y)
# plt.plot(y,Lspan)
# plt.show()