import scipy as sp
import numpy as np
from matplotlib import pyplot as plt

def spar_weight_025(y):
    w = 2700*0.114*3.5*(1-(1-0.372)(y/11.98))
    return

def spar_weight_075(y):
    return

def get_Weight(y):
    return y 

def main():
    y_axis = np.linspace(0,12,1000)
    Weight=get_Weight(y_axis)


    plt.plot(y_axis, Weight)
    plt.title("Spanwise Weight distribution")
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Weight [N]")
    plt.show()

if __name__=="__main__":
    main()