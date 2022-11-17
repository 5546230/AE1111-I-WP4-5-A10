import numpy as np

def ISA_rho(h: float) -> float:
    '''Calculate the density at a altitude in meters via ISA '''
    #define constants
    g = 9.80665
    R = 287.0
    T0 = 288.15
    P0 = 101325
    a_lst = [0,-0.0065,0,0.001,0.0028,0,-0.0028,-0.002]
    h_lst = [0,11000,20000,32000,47000,51000,71000,86000]

    # initialize variables
    h_left = h
    t=T0
    p=P0

    #isa loop
    for i in range(0,len(h_lst)-1):
        a=a_lst[i+1]
        h_ref = min(h, h_lst[i+1])
        if a==0:
            p*=np.exp(g/(R*t)*(h_lst[i]-h_ref))
        else:
            t -= a * (h_lst[i]-h_ref)
            p*= (1-a*(h_lst[i]-h_ref)/T0)**(-g/(a*R))

        if h_ref == h:
            return p/(R*t)
