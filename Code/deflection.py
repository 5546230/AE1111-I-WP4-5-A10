from Moment_of_inertia import get_ixx
from load_case import LoadCase
import scipy as sp
import numpy as np
from scipy import interpolate
from matplotlib import pyplot as plt

def get_deflection(y: float, load: LoadCase, t_s: float, t_f: float, t_r:float, n_stringer: int, A_stringer: float) -> float:
    '''the relation between the moment, moment of inertia and the second derivative of the deflection'''
    moment = load.z2_moment(y)
    ixx = get_ixx(y, t_f, t_r, t_s(y), n_stringer, A_stringer)
    E = 68e9
    return (-moment/(E*ixx))

def get_t(n_stringer: int, A_stringer: float) -> tuple:
    '''calculate the minimum thickness for the deflection through an iterative process'''
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    y_axis = np.linspace(0,11.98,100)
    t = 1.5e-3
    t_lst = [] 
    defl_lst = []
    #start the iteration
    for iteration in np.arange(99999):
        #integrate twice to get the deflection
        defl = []
        for y in y_axis:
            defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= (load, t, n_stringer, A_stringer))
            defl.append(defl_val)

        #interpolate to be able to integrate again
        defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")

        deflection, _ = sp.integrate.quad(defl_func, 0, 11.98)

        t_lst.append(t)
        defl_lst.append(deflection)

        #check if deflection within limits
        if deflection>=-23.5*0.15 and deflection<=-23.5*0.149:
            return t, deflection, t_lst, defl_lst
        
        #update the thickness
        t*=deflection/-23.5/0.15

def diagram(t_s, t_f:float, t_r: float, n_stringer, A_stringer: float, name: str):
    '''Get a deflection diagram for a thickness of t'''
    defl = []
    y_axis = np.linspace(0,11.98,100)
    load = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)
    # load = LoadCase(-1.5, 16575.6*9.80665, 156.42, 12500)


    for y in y_axis:
        defl_val, _ = sp.integrate.quad(get_deflection, 0, y, args= (load, t_s,t_f, t_r, n_stringer(y), A_stringer))
        defl.append(defl_val)

    defl_func = sp.interpolate.interp1d(y_axis, defl, kind="linear")
    defl_lst= []
    for y in y_axis:
        deflection, _ = sp.integrate.quad(defl_func, 0, y)
        defl_lst.append(deflection)
    print(defl_lst[-1])
    fig = plt.figure()
    fig.set_figwidth(8)
    plt.plot(y_axis, defl_lst)
    plt.xlabel("Spanwise location [m]")
    plt.ylabel("Deflection [m]")
    # plt.title(f"Deflection for a thickness of {t*1e3:.1f} [mm], with {n_stringer} stringers of area {A_stringer*1e6:.1f} [mm^2] for n = {load.n:.2f}")
    plt.xlim(0,12)
    plt.ylim(None,0)
    plt.grid()
    plt.savefig(name, format="svg", transparent = True)
    plt.cla()
    
if __name__=="__main__":
    # t,_,_,_=get_t(0,0)
    # print(t)
    # _,_, t_lst, defl_lst = get_t(0,0)
    # iter_lst = np.arange(len(t_lst))
    # print(t_lst, defl_lst)
    # fig, axs = plt.subplots(2, sharex= True)    
    # fig.suptitle("The change of the deflection and thickness for the iterations")

    # axs[0].plot(iter_lst, t_lst)
    # axs[0].set_xbound(0, iter_lst[-1])
    # axs[0].set_ylabel("Thickness [mm]")

    # axs[1].plot(iter_lst, defl_lst)
    # axs[1].set_ylabel("Deflection [m]")
    # axs[1].set_xlabel("Iteration")
    # plt.show()
    # # print(t)
    # diagram(4*1e-3, 0,0, "deflection1_1.svg")
    # diagram(1.5*1e-3, 2, (65*1e-3)**2, "deflection2_1.svg")
    # diagram(2*1e-3, 4, (35*1e-3)**2, "deflection3_1.svg")
    #OPTION2:
    t_f = 5.5e-3
    t_r = 4e-3
    a_stringer = (35e-3)**2
    m = 0.362
    n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])
    t_s = sp.interpolate.interp1d(y_lst, t_lst, kind="next", fill_value="extrapolate")

    diagram(t_s, t_f, t_r, n, m*a_stringer, "./Figures/deflection_design.svg")    