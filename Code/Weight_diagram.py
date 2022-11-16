import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

t= 0.01
A_root = 1.094
mass = 756
lamda = 0.372
volume = 6.613 
def spar_weight_025(y):
    w = 2700*0.114*3.5*(1-(1-0.372)*(y/11.98))*9.81*t
    return w 

def spar_weight_075(y):
    w = 2700*0.063*3.5*(1-(1-0.372)*(y/11.98))*9.81*t
    return w 

def fuel_weight(y):
    w = 9.81*0.04425*3.5**2*804*(1-(1-0.372)*(y/11.98))**2
    return w


def get_Weight(y):
    return A_root*((lamda-1)/12*y+1)**2*mass/volume + fuel_weight(y)

def main():
    y_axis = np.linspace(0,12,1000)
    Weight=get_Weight(y_axis)

    val, _=(sp.integrate.quad(get_Weight, 0, 11.98))
    print(val/9.81)
    plt.plot(y_axis, Weight)
    plt.title("Spanwise Weight distribution")
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Weight [N]")
    plt.show()

if __name__=="__main__":
    main()
    