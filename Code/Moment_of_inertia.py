import math
import numpy as np

def get_ixx(y: float) -> float:
    c_r = 3.49 #root chord[m]
    c = c_r-c_r*(1-0.372)/12*y #formula for chord
    t = 1*10**-3 #thickness

    A_stringer = 2 #TBD
    d_stringer = 2 #TBD
    nr = 0 #number of stringers
    
    h_up = 0.114*c-0.096*c #
    h_mid = 0.0808*c #height right side
    h_low = 0.0331*c
    h_1 = 0.114*c-0.0808*c
    h_2 = 0.0331*c
    h = 0.114*c #height left side
    l = 0.55*c #lenght

    H = 0.551*c
    beta_1=math.atan(h_up/l) #top angle
    beta_2=math.atan(h_2/l) #bottom angle

    A_1 = h*t 
    A_2 = H*t
    A_3 = h_mid*t
    A_4 = H*t

    z_centroid = ((h_1-h_mid/2)*A_3+h/2*A_1+H/2*np.sin(beta_2)*A_4+A_2*(h-H/2*np.sin(beta_1)))/(A_1+A_2+A_3+A_4)#(2*h_2/3*A_3+(h_2+h_mid/2)*A_2+(h_1+h_up/3)*A_1)/(A_1+A_2+A_3)

    I_xx_1 = 1/12*t*h**3 + A_1*(h/2-z_centroid)**2
    I_xx_2 = 1/12*t*H**3*math.sin(beta_1)**2+A_2*(h-H/2*np.sin(beta_1)-z_centroid)**2
    I_xx_3 = 1/12*t*h_mid**3+A_3*(h_1-h/2-z_centroid)**2
    I_xx_4 = 1/12*y*H**3*math.sin(beta_2)**2 + A_4*(z_centroid-H/2*np.sin(beta_2))**2



    I_xx = I_xx_1 + I_xx_2 + I_xx_3 + I_xx_4 + nr*A_stringer*d_stringer**2
    return(I_xx)


def get_J(y: float) -> float:
    c_r = 3.49 #root chord[m]
    c = c_r-c_r*(1-0.372)/12*y #formula for chord
    t = 1*10**-3 #thickness
   
    A_enclosed= 0.5*(0.114*c + 0.063*c)*0.55*c #enclosed area of the wingbox
    perimeter= (0.114*c + 2*0.551*c + 0.063*c) #contour of the wingbox

    J = 4*A_enclosed**2/(perimeter/t)

    return(J)

