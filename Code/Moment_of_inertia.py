import math
import numpy as np
from matplotlib import pyplot as plt

def get_ixx(y: float, t: float, n_stringer: int = 0, A_stringer: float = 0.000625) -> float:
    '''returns the area moment of inertia at a y location along the span for a given thickness t, even number of stringers n_stringer with area A_stringer.'''
    c_r = 3.49 #root chord[m]
    c = c_r-c_r*(1-0.372)/12*y #formula for chord
    # t = 2*10**-3 #thickness

    
    h_up = 0.027543*c #
    h_mid = 0.063*c #height right side
    h_low = 0.023457*c
    h_2 = h_low
    h = 0.114*c #height left side
    l = 0.55*c #lenght

    H_1 = 0.5505*c #hyphotenus
    H_2 = 0.55069*c
    beta_1 = math.atan(h_up/l) #top angle
    beta_2 = math.atan(h_2/l) #bottom angle

    A_1 = h*t 
    A_2 = H_2*t
    A_3 = h_mid*t
    A_4 = H_1*t

    #calculate the z coordinate of the wingbox
    z_centroid = ((h_low+h_mid/2)*A_3+h/2*A_1+H_1/2*np.sin(beta_2)*A_4+A_2*(h-H_2/2*np.sin(beta_1)))/(A_1+A_2+A_3+A_4)
    
    #calculate the moment of inertia components
    I_xx_1 = 1/12*t*h**3 + A_1*(h/2-z_centroid)**2
    I_xx_2 = 1/12*t*H_2**3*math.sin(beta_1)**2+A_2*(h-H_2/2*np.sin(beta_1)-z_centroid)**2
    I_xx_3 = 1/12*t*h_mid**3+A_3*(h_low+h_mid/2-z_centroid)**2
    I_xx_4 = 1/12*t*H_1**3*math.sin(beta_2)**2 + A_4*(z_centroid-H_1/2*np.sin(beta_2))**2

    nr_up = n_stringer//2 #number of upper part stringers
    nr_down = n_stringer//2 #number of lower part stringers

    #case 1: t=2.4 no stringers
    #case 2: t=1 2 stringers (side=35mm)
    #case 3: t=1 4 stringers (side=25mm)

    #calculate the total ixx
    I_xx = I_xx_1 + I_xx_2 + I_xx_3 + I_xx_4 + nr_up*A_stringer*(h-H_2/2*np.sin(beta_1)-z_centroid)**2 + nr_down*A_stringer*(H_1/2*np.sin(beta_2)-z_centroid)**2
    return(I_xx)

def get_zcentroid(y: float, t: float) -> float:
    '''returns the z-coordinate for the centroid of the wingbox at location  along the span for a thickness of t'''
    c_r = 3.49 #root chord[m]
    c = c_r - c_r * (1 - 0.372)/12*y #formula for chord
    # t = 2*10**-3 #thickness

    
    h_up = 0.027543*c #
    h_mid = 0.063*c #height right side
    h_low = 0.023457*c
    h_2 = h_low
    h = 0.114*c #height left side
    l = 0.55*c #lenght

    H_1 = 0.5505*c #hyphotenus
    H_2 = 0.55069*c
    beta_1 = math.atan(h_up/l) #top angle
    beta_2 = math.atan(h_2/l) #bottom angle

    A_1 = h*t 
    A_2 = H_2*t
    A_3 = h_mid*t
    A_4 = H_1*t

    #calculate the z coordinate of the wingbox
    z_centroid = ((h_low+h_mid/2)*A_3+h/2*A_1+H_1/2*np.sin(beta_2)*A_4+A_2*(h-H_2/2*np.sin(beta_1)))/(A_1+A_2+A_3+A_4)

    return z_centroid

def get_J(y: float, t:float) -> float:
    '''returns the polar moment of inertia for a given thickness t at a location y along the span'''
    c_r = 3.49 #root chord[m]
    c = c_r-c_r*(1-0.372)/12*y #formula for chord
    # t = 1.5*10**-3 #thickness
   
    A_enclosed= 0.5*(0.114*c + 0.063*c)*0.55*c #enclosed area of the wingbox
    perimeter= (0.114*c + 2*0.551*c + 0.063*c) #contour of the wingbox

    J = 4*A_enclosed**2/(perimeter/t)

    return(J)

def diagram(t: float) -> None:
    '''Get the diagram for Ixx as a function of y along the span for a thickness t'''
    y_axis = np.linspace(0,11.98,100)
    ixx_lst=[]
    #get the ixx for each y location
    for y in y_axis:
        ixx_lst.append(get_ixx(y, t))

    #plot the values
    plt.plot(y_axis, ixx_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Moment of inertia [m^4]")
    plt.title(f"Moment of ineratia for a thickness of {t*1e3:.1f} [mm]")
    plt.show()

if __name__=="__main__":
    diagram(2.4*1e-3)