import math
import numpy as np
from matplotlib import pyplot as plt

def get_ixx(y: float, t_f: float, t_r: float, t_s: float, n_stringer: int = 0, A_stringer: float = 0.000625) -> float:
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

    A_1 = h*t_f 
    A_2 = H_2*t_s
    A_3 = h_mid*t_r
    A_4 = H_1*t_s

    #calculate the z coordinate of the wingbox
    z_centroid = ((h_low+h_mid/2)*A_3+h/2*A_1+H_1/2*np.sin(beta_2)*A_4+A_2*(h-H_2/2*np.sin(beta_1)))/(A_1+A_2+A_3+A_4)
    
    #calculate the moment of inertia components
    I_xx_1 = 1/12*t_f*h**3 + A_1*(h/2-z_centroid)**2
    I_xx_2 = 1/12*t_s*H_2**3*math.sin(beta_1)**2+A_2*(h-H_2/2*np.sin(beta_1)-z_centroid)**2
    I_xx_3 = 1/12*t_r*h_mid**3 + A_3*(h_low+h_mid/2-z_centroid)**2
    I_xx_4 = 1/12*t_s*H_1**3*math.sin(beta_2)**2 + A_4*(z_centroid-H_1/2*np.sin(beta_2))**2

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

def get_J(y: float, t_f: float, t_r: float, t_s: float) -> float:
    '''returns the polar moment of inertia for a given thickness t at a location y along the span'''
    c_r = 3.49 #root chord[m]
    c = c_r-c_r*(1-0.372)/12*y #formula for chord
    # t = 1.5*10**-3 #thickness
   
    A_enclosed= 0.5*(0.114*c + 0.063*c)*0.55*c #enclosed area of the wingbox

    J = 4*A_enclosed**2/(0.063*c*t_r+0.114*c*t_f+(0.5505+0.55069)*c*t_s)

    return(J)

def ixx_diagram(t: float, n_stringers: int, A_stringer: float, name: str) -> None:
    '''Get the diagram for Ixx as a function of y along the span for a thickness t'''
    y_axis = np.linspace(0,11.98,100)
    ixx_lst=[]
    #get the ixx for each y location
    for y in y_axis:
        ixx_lst.append(get_ixx(y, t, n_stringers, A_stringer))

    #plot the values
    fig=plt.figure()
    fig.set_figwidth(8)
    plt.plot(y_axis, ixx_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Moment of Inertia [m^4]")
    plt.title(f"Moment of Inertia for a thickness of {t*1e3:.1f} [mm], with {n_stringers} stringers of area {A_stringer*1e6:.1f} [mm^2]")
    plt.xlim(0,12)
    plt.ylim(0)
    plt.grid()
    plt.savefig(name, format="svg", transparent = True)

def J_diagram(t: float, name: str) -> None:
    '''Get the diagram for Ixx as a function of y along the span for a thickness t'''
    y_axis = np.linspace(0,11.98,100)
    J_lst=[]
    #get the ixx for each y location
    for y in y_axis:
        J_lst.append(get_J(y, t))

    #plot the values
    fig=plt.figure()
    fig.set_figwidth(8)
    plt.plot(y_axis, J_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Polar Moment of Inertia [m^4]")
    plt.title(f"Polar Moment of Inertia for a thickness of {t*1e3:.1f} [mm]")
    plt.xlim(0,12)
    plt.ylim(0)
    plt.grid()
    plt.savefig(name, format="svg", transparent = True)

def torsional_stiffness_diagram(t: float, name: str) -> None:
    '''Get the diagram for Ixx as a function of y along the span for a thickness t'''
    y_axis = np.linspace(0.0001,11.98,1000)
    G = 68e9*3/8
    tor_lst=[]
    #get the ixx for each y location
    for y in y_axis:
        tor_lst.append(get_J(y, t))

    tor_lst=np.array(tor_lst)*G/y_axis

    #plot the values
    fig=plt.figure()
    fig.set_figwidth(8)
    plt.plot(y_axis, tor_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Torsional stiffness [Nm/rad]")
    plt.title(f"Torsional stiffness for a thickness of {t*1e3:.1f} [mm]")
    plt.yscale('log')
    plt.xlim(0,12)
    plt.ylim(0)
    plt.grid()
    # plt.show()
    plt.savefig(name, format="svg", transparent = True)
    plt.cla()

if __name__=="__main__":
    # ixx_diagram(2*1e-3, 4, 0.035**2)
    # J_diagram(4*1e-3, "polar1.svg")
    # J_diagram(1.5*1e-3, "polar2.svg")
    # J_diagram(2*1e-3, "polar3.svg")
    # ixx_diagram(4*1e-3, 0, 0,"inertia1.svg")
    # ixx_diagram(1.5*1e-3, 2, 0.065**2, "inertia2.svg")
    # ixx_diagram(2*1e-3, 4, 0.035**2, "inertia3.svg")
    torsional_stiffness_diagram(4*1e-3,"stiffness1.svg")
    torsional_stiffness_diagram(1.5*1e-3, "stiffness2.svg")
    torsional_stiffness_diagram(2*1e-3, "stiffness3.svg")