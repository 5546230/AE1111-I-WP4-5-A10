import numpy as np
from load_case import LoadCase
from matplotlib import pyplot as plt
import scipy as sp
from scipy import interpolate

def shear_max(y: float, t: float, load: LoadCase) -> float:
    V = load.z2_shear(y)
    c_r = 3.5
    k_v= 1.2
    c = c_r-c_r*(1-0.372)/12*y
    h_f = 0.114*c
    h_r = 0.063*c

    tau_ave = V / ((h_f+h_r)*t)

    return k_v*tau_ave

def shear_tor(y: float, t: float, load: LoadCase) -> float:
    c_r = 3.5
    c = c_r-c_r*(1-0.372)/12*y
    T = load.torque(y)+ 0.3*c*load.z2_shear(y)

    A_i = 0.5*(0.114*c + 0.063*c)*0.55*c

    q = T/(2*A_i)

    return q/t

def shear_tot(y: float, t: float, load: LoadCase) -> float:
    return abs(shear_tor(y,t,load)+shear_max(y,t,load))

def shear_crit(y: float, t: float, k_s: float)-> float:
    c_r = 3.5
    c = c_r-c_r*(1-0.372)/12*y
    nu = 1/3 
    b = 0.113*c
    E= 68e9

    tau_crit = (np.pi)**2*k_s*E/(12*(1-nu**2))*(t/b)**2

    return tau_crit

def get_ks(t: float, load: LoadCase) -> float:
    #set ks to 10
    k_s = np.array([10]*100)

    y_axis = np.linspace(0.1,11.98,100)
    factor_lst = []
    for y in np.arange(len(y_axis)):
        factor = shear_crit(y_axis[y], t, k_s[y])/shear_tot(y_axis[y], t, load)
        factor_lst.append(factor)
    factor_lst = np.array(factor_lst)
    k_s = k_s/(factor_lst)

    return k_s

def a_b(y):
    c_r = 3.5 
    c = c_r-c_r*(1-0.372)/12*y
    b = 0.114*c
    a = 0.75+0.25*(y>6)
    return a/b

ks_lst= [11,10.6,10.3,9.9,9.8,9.65,9.6,9.5,9.3,9.3]
# y_lst = [0.75,1.5,2.25,3,3.75,4.5,5.25,6,7,8,9,10,11,12]
y_lst = [0.75,1.5,2.25,3,3.75,4.5,5.25,6,9,12]

ks = sp.interpolate.interp1d(y_lst,ks_lst,kind= "next", fill_value="extrapolate")

def get_mos(y: float, load: LoadCase) -> float:
    ks_val = ks(y)
    t = 5.5e-3-(1.5e-3)*(y>6)-(1e-3)*(y>9)
    tot = shear_tot(y, t, load)
    crit = shear_crit(y, t, ks_val)

    return crit/tot


y_axis = np.linspace(0.1,11.98,100)

load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

t=5.5e-3
lst=[]

for y in y_axis:
    mos = get_mos(y, load)
    lst.append(mos)

ks_lst2= ks(y_axis)
# fig, axs = plt.subplots(2)
# axs[0].plot(y_axis, lst)
plt.plot(y_axis, lst)
# plt.xlim(6)
plt.yscale('log')
plt.show()