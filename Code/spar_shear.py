import numpy as np
from load_case import LoadCase
from matplotlib import pyplot as plt
import scipy as sp
from scipy import interpolate

def shear_max(y: float, t_f: float, t_r: float, load: LoadCase) -> float:
    """
    Returns the maximum shear stress in a wingbox, with front spar thickness t_f and rear spar thickness t_r, due to shear for a load case, load, at a spanwise location, y.
    """
    #get the shear force from the load case
    V = load.z2_shear(y)

    #define the k_v
    k_v = 1.2

    #calculate the chord
    c_r = 3.5
    c = c_r-c_r*(1-0.372)/12*y

    #calculate the spar heights
    h_f = 0.114*c
    h_r = 0.063*c

    #calculate the average shear stress
    tau_ave = V / ((h_f*t_f+h_r*t_r))

    #return the maximum shear stress
    return k_v*tau_ave

def shear_tor(y: float, t: float, load: LoadCase) -> float:
    """
    Returns the torsional shear stress in a wingbox, with spar thickness t, due to shear for a load case, load, at a spanwise location, y.
    """
    
    #calculate the chord
    c_r = 3.5
    c = c_r-c_r*(1-0.372)/12*y

    #get the torque from the load case
    T = load.torque(y)+ 0.3*c*load.z2_shear(y)

    #calculate the enclosed area
    A_i = 0.5*(0.114*c + 0.063*c)*0.55*c

    #calculate the shear flow
    q = T/(2*A_i)

    #return the shear stress
    return q/t

def shear_tot(y: float, t_f: float, t_r: float, load: LoadCase, front: bool) -> float:
    """
    Returns the total shear stress in a wingbox, with front spar thickness t_f and rear spar thickness t_r, due to shear and torsion for a load case, load, at a spanwise location, y.
    """
    #check whether the front or rear spar is relevant
    if front:
        t=t_f
    else:
        t=t_r

    #return the total shear stress
    return abs(shear_tor(y,t,load)+shear_max(y,t_f,t_r,load))

def shear_crit(y: float, t_f: float, t_r: float, k_s: float, front: bool)-> float:
    """
    Returns the critical shear stress in a wingbox, with front spar thickness t_f and rear spar thickness t_r, due to shear and torsion for a load case, load, at a spanwise location, y.
    """
    #calculate the chord
    c_r = 3.5
    c = c_r-c_r*(1-0.372)/12*y

    #define the material properties
    nu = 1/3 
    E= 68e9

    #check if the front or rear spar is relevant
    if front:
        b = 0.113*c
        t = t_f
    else:
        b = 0.063*c
        t = t_r

    #calculate the critical shear stress
    tau_crit = (np.pi)**2*k_s*E/(12*(1-nu**2))*(t/b)**2

    #return the critical shear stress
    return tau_crit

def get_ks(t_f: float, t_r: float, load: LoadCase, front: bool) -> float:
    """
    Returns the ks in a wingbox, with front spar thickness t_f and rear spar thickness t_r, due to shear and torsion for a load case, load, at a spanwise location, y.
    """
    #set ks to 10
    k_s = np.array([10]*100)

    #define the lists
    y_axis = np.linspace(0.1,11.98,100)
    factor_lst = []

    #iterate through the y_axis to find the current factor of safety
    for y in np.arange(len(y_axis)):
        factor = shear_crit(y_axis[y], t_f,t_r, k_s[y], front)/shear_tot(y_axis[y], t_f, t_r, load, front)
        factor_lst.append(factor)

    #reduce the ks such that the factor is 1
    factor_lst = np.array(factor_lst)
    k_s = k_s/(factor_lst)

    #return the ks
    return k_s

#define the ks lists for the front and rear spars based on the graphs
ks_lst_f= [11.8,11.4,11.4,11.3,11.3,11.0,10.8,10.5,10.4,10.3,9.3]
ks_lst_r= [9.7,9.6,9.6,9.5,9.4,9.35,9.3,9.3,9.3,9.3,9.3]
y_lst = np.linspace(0.6,6,10)
y_lst = np.append(y_lst,12)

#interpolate the lists
ks_f = sp.interpolate.interp1d(y_lst,ks_lst_f,kind= "next", fill_value="extrapolate")
ks_r = sp.interpolate.interp1d(y_lst,ks_lst_r,kind= "next", fill_value="extrapolate")


def get_mos(y: float, load: LoadCase, front: bool) -> float:
    """
    Returns the Maring of Safety in a wingbox due to shear and torsion for a load case, load, at a spanwise location, y.
    """
    #define the thicknesses
    t_f = 5.5e-3
    t_r = 4e-3

    #check if the front or rear spar is relevant
    if front:
        ks_val = ks_f(y)
    else:
        ks_val = ks_r(y)

    #calculate the total and critical shear stress
    tot = shear_tot(y, t_f,t_r, load, front)
    crit = shear_crit(y, t_f,t_r, ks_val, front)

    #return the ratio of the critical and total stress
    return crit/tot

def mos_plot(front):
    """
    Plots the Maring of Safety in a wingbox due to shear and torsion for a load case, load, as a function of the spanwise location, y.
    """
    #define the thicknesses
    y_axis = np.linspace(0.1,11.98,100)

    #define the load case
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    #calculate the mos at each y location
    lst=[]
    for y in y_axis:
        mos = get_mos(y, load, front)
        lst.append(mos)

    #plot the values
    plt.plot(y_axis, lst)
    plt.yscale('log')
    plt.grid(True)
    plt.xlim(0,12)
    plt.ylim(1)
    plt.xlabel('Spanwise location [m]')
    plt.ylabel('Margin of Safety [-]')
    if front:
        name = f".//figures//front_mos.svg"
    else:
        name = f".//figures//rear_mos.svg"
    #save the figure as a svg
    plt.savefig(name, format='svg')
    plt.cla()

def ks_compare_plot(front: bool):
    """
    Plots the required and actual KS in a wingbox due to shear and torsion for a load case, load, at a spanwise location, y.
    """
    #define the y_axis
    y_axis = np.linspace(0.1,11.98,100)

    #define the load case
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    #define the thicknesses
    t_f = 5.5e-3
    t_r = 4e-3

    #check if the front or rear spar is relevant
    if front:
        ks_lst = ks_f(y_axis)
    
    else:
        ks_lst = ks_r(y_axis)

    #calculate the required ks 
    ks_lst2 = get_ks(t_f,t_r, load, front)

    #plot the values
    plt.plot(y_axis, ks_lst, label='Actual ks')
    plt.plot(y_axis, ks_lst2, label='Required ks')
    plt.legend()
    plt.grid(True)
    plt.xlabel('spanwise location [m]')
    plt.ylabel('ks [-]')
    plt.xlim(0,12)
    plt.ylim(0,12)
    if front:
        name = f".//figures//front_ks.svg"
    else:
        name = f".//figures//rear_ks.svg"
    #save the figure as a svg
    plt.savefig(name, format='svg')
    plt.cla()


if __name__ == "__main__":
    mos_plot(1)
    mos_plot(0)
    ks_compare_plot(1)
    ks_compare_plot(0)