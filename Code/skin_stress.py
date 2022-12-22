import json
import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *
from Weight_diagram import get_mass
from matplotlib import pyplot as plt

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"

#assumed distance from NA is the upper left corner of the wing box (conservative)
def skin_stress(y, t_f, t_r, t, a_stringer, load_max_compr, n_stringers, m):
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t_f, t_r, t, n_stringers, m*a_stringer) #Pa; flexure formula #On purpose
    return sigma

def av_skin_stress(y1, y2, t_f, t_r, t, a_stringer, load_max_compr, n_stringers, m):
    sigma_av = 0.5*(skin_stress(y1, t_f, t_r, t, a_stringer, load_max_compr, n_stringers, m)+skin_stress(y2, t_f, t_r, t, a_stringer, load_max_compr, n_stringers, m))
    return sigma_av

#def ratio():
    ratio = []
    for i in range(5, int(b/2)+1):
        r = skin_stress(5)/skin_stress(i+1)
        ratio.append(r)
    return ratio

def stress_crit(y1, y2, t, n_u, n_0, y1_0):
    original = n_0//2
    E = 68e9 #Pa
    nu = 0.33 #-
    if y1_0 == 0:
        b = (0.55*get_c(y1))/(n_u+1)
    else:    
        if n_u == original:    #change n_u value according to the results of the root simulations               
            b = (0.55*get_c(y1))/(n_u+1)
        elif n_u > 0: #it can only be less compared to the root case, so that's fine
            b = (2*0.55*get_c(y1))/(original+1)
        else:
            b = 0.55*get_c(y1)
    slenderness = ((y2-y1))/(b) #a over b
    if slenderness < 0.5:
        K = 12
    elif (0.5 < slenderness) and (slenderness < 1):
        K = 1250*(slenderness)**4-3750*(slenderness)**3+4197.5*(slenderness)**2-2081.5*(slenderness)+391
    elif slenderness > 1:
        K = max(3.9617*np.e**(-0.046*slenderness), 3) #for linearly varying moment
    if __name__=="__main__":
        sigma_crit = ( ((t(y1)**2)*E*(np.pi**2)) / (12*(1-nu**2)) ) * ( (1/b)**2 ) * K
    else:
        sigma_crit = ( ((t**2)*E*(np.pi**2)) / (12*(1-nu**2)) ) * ( (1/b)**2 ) * K
    return sigma_crit, K, slenderness

def mass_remaining(y_0):
    m_r = sp.integrate.quad(get_mass, y_0, 12)[0]
    return m_r

def mass_config_per_length(n, m, y1, y2, t, a_stringer):
    m_config = 2700*(n*m*a_stringer+1.101*get_c(0.5*(y1+y2))*t) #assumes that m/l at the middle of the bay is the avg m/l
    return m_config

if __name__=="__main__":
    ###IMPORT HERE TO PREVENT CIRCULAR IMPORTATION###
    from column_buckling import *
    from compressive_strength import design_option_compr
    from mass_calc import mass_bay
    #data
    b = 24 #m
    E = 68e9 #Pa
    nu = 0.33 #-

    #default is option 3
    design_option = str(3)
    #design_option = str(input("Design option (1, 2 or 3):", ))

    ################# INPUT ###################
    n_0 = 2 #staring n value
    n_list = [2, 0] #number of ribs to check
    n = lambda x: n_0
    n_prev = n(0)-2
    m0 = 0.362 #starting m value
    t0 = 0.002 #m - starting t value

    #iteration values
    dt = 0.0001
    dm = 0.001
    dy = 0.005 #m
    tolerance = 0.95

    #t is set
    t = lambda x: t0
    t_prev = t0
    
    m = m0
    #start of iteration
    #################
    y1_0 = 9.745 #m STARTING VALUE
    #################
    y2 = y1_0 + dy #m

    span_lim = 12 #runs until this spanwise location
    no_ribs_placed = 2 #places this many ribs (max 4). ALSO CHANGE "ind_out" ARRAY ACCORDINGLY

    n_rib = 0
    ribs = []
    ratio = []

    if y1_0 == 0:
        m_lim = 0.4
    else:
        m_lim = m0

    #########################################

    # OUTPUT
    output = np.array([["n", "m", "t [mm]", "mass [kg]", "m_bay [kg]", "rib 1 [mm]", "rib 2 [mm]", "rib 3 [mm]", "rib 4 [mm]", "r1"]])

    #design options parameters (n_stringers, t, ...)
    designs = {
        "1":dict(t = 4, n_stringers = 0, a_stringer = 0),
        "2":dict(t = 1.5, n_stringers = 2, a_stringer = (65e-3)**2),
        "3":dict(t = 2, n_stringers = n, a_stringer = (45e-3)**2)
    }

    n_stringers = designs[design_option]["n_stringers"]
    n_u = int(n(0)/2)
    #t = designs[design_option]["t"]*1e-3 #m
    a_stringer = designs[design_option]["a_stringer"] #m^2

    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    #load case for maximum compression in upper skin panels
    load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    counter = 0

    for i in n_list:
        n = lambda x: i
        if counter == len(n_list):
            break
        
        t = lambda x: t0
        t_prev = t0
        current_option = design_option_compr(m*a_stringer, n, 10, t_f, t_r, t, 1, load_max_compr)
        while not current_option.test(y1_0):
            #if n(0)<=n_0-2:
            #    n= lambda x: n_prev + 2
            #    n_prev+=2
            if m<m_lim:
                m+=dm
            else:
                t = lambda x: t_prev+dt
                t_prev = t_prev+dt
            current_option = design_option_compr(m*a_stringer, n, 10, t_f, t_r, t, 1, load_max_compr)

        ##########
        n_prev = n(0)
        t_prev = t(0)

        while t(0) < 0.008:
            #check if amount of stringers can be reduced
            #n_two = lambda x: n(x)-2
            #while design_option_compr(m*a_stringer, n_two, 10, t_f, t_r, t, 1, load_max_compr).test(y1_0):
            #    if n_two(0)>=0:
            #        n = lambda x: n_prev - 2
            #        n_prev -= 2
            #        n_two = lambda x: n(x)-2
            #    else:
            #        break


            #check if m can be reduced
            if y1_0 == 0:
                while design_option_compr((m-dm)*a_stringer, n, 10, t_f, t_r, t, 1, load_max_compr).test(y1_0):
                    if m-2*dm>0.005 and n(0)>0:
                        m-=dm
                    else:
                        break

            print(n(0), m, t(0))  
            y1 = y1_0 #m
            y2 = y1 + dy #m
            while y2 < span_lim:
                n_u = n(y1)//2 #initial stringer arrangement should be kept
                K = stress_crit(y1, y2, t, n_u, n_0, y1_0)[1]
                slenderness = stress_crit(y1, y2, t, n_u, n_0, y1_0)[2]
                
                s_av = av_skin_stress(y1, y2, t_f, t_r, t(y1), a_stringer, load_max_compr, n(y1), m)
                s_crit = stress_crit(y1, y2, t, n_u, n_0, y1_0)[0]
                
                delta_K = stress_crit(y1, y2-dy, t, n_u, n_0, y1_0)[1] - stress_crit(y1, y2, t, n_u, n_0, y1_0)[1]
                if (1.05*s_av) < s_crit:
                    y2 += dy
                    s_av = av_skin_stress(y1, y2, t_f, t_r, t(y1), a_stringer, load_max_compr, n(y1), m)
                    s_crit = stress_crit(y1, y2, t, n_u, n_0, y1_0)[0]
                else: #Places a rib
                    #print("Rib placement", n(y1), m, t(y1), "ratio: ", s_av/s_crit, "DK: ", delta_K, "K: ", K, "Rib at: ", y2, "\n")
                    #print("Moment y1: ", load_max_compr.z2_moment(y1), "Moment y2: ", load_max_compr.z2_moment(y2), "\n")
                    print(K)
                    y1 = y2
                    y2 = y1 + dy
                    ribs.append(y1)
                    ratio.append(s_crit/s_av)
                if y2 > span_lim-0.1:
                    ribs.append(span_lim-0.1)
                    ratio.append(s_av/s_crit)
                    y1 = span_lim-0.1
                    y2 = y1+dy
                if len(ribs)==no_ribs_placed:
                    mass =  mass_config_per_length(n(y1), m, y1_0, ribs[no_ribs_placed-1], t(y1), a_stringer)*(ribs[no_ribs_placed-1]-y1_0) + mass_remaining(ribs[no_ribs_placed-1])
                    ind_out = np.array([[int(n(y1)), m, round(t(y1)*10**3, 4), round(mass, 5), mass_bay(y1_0, ribs[no_ribs_placed-1], int(n(y1)), m, t(y1), a_stringer), round(ribs[0], 3)*10**3, round(ribs[no_ribs_placed-1], 3)*10**3, round(ribs[no_ribs_placed-1], 3)*10**3, round(ribs[no_ribs_placed-1], 3)*10**3, ratio[0]]])
                    output = np.concatenate((output,ind_out))
                    n_rib = 0
                    y1 = y1_0 #m
                    y2 = y1 + dy #m
                    ribs = []
                    ratio = []
                    break
                
            t = lambda x: t_prev + dt
            t_prev += dt
            ribs = []
            ratio = []
        counter += 1
    
    print(output[0,:])
    output = np.delete(output, 0, 0)
    output = output.astype(float)
    
    output = np.delete(output, np.where(output[:, 9] < tolerance)[0], 0)
    
    output = np.delete(output, np.where( (output[:, 6] - output[:, 5]) < 100)[0], 0)
    
    output = output[output[:, 3].argsort()]
    #output = output.astype(int)
    print(output)
    print(output[0,:])
    print(mass_config_per_length(output[0,0],output[0,1], y1_0, output[0,no_ribs_placed+4]*10**-3, output[0,2]*10**-3, a_stringer)*(output[0,no_ribs_placed+4]*10**-3-y1_0))

    with open('output.txt', 'w') as filehandle:
        json.dump(output.tolist(), filehandle)

    #K = 0.0364*(slenderness)**2 - 0.3815*(slenderness) + 4.2206 <- scrap

    ### config data ### - log your simulation here
    #n = lambda x: 6 if x<8.885 else 4 if x< 9.41 else 2
    #m = 0.362
    #ribs = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.65, 7.81, 7.975, 8.145, 8.305, 8.47, 8.66, 8.885, 9.145, 9.41, 9.745, 10.105, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 4.4e-3, 5.2e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 8.145, 8.885, 12])
    #masses = [109, 86, 59, 49, 61, 48, 53, 47, 46, 49, 26, 27, 19, 11, 59]

    #1
    #[6.00000000e+00 3.62000000e-01 1.27000000e+01 7.72274320e+02 1.09153884e+02 3.75000000e+02 7.70000000e+02 3.75000000e+02 3.75000000e+02 9.55832064e-01]
    #2
    #[6.00000000e+00 3.62000000e-01 1.18000000e+01 6.74525860e+02 8.63318001e+01 1.09000000e+03 1.44500000e+03 1.09000000e+03 1.09000000e+03 9.56436892e-01]
    #3
    #[6.00000000e+00 3.62000000e-01 1.06000000e+01 5.92869060e+02 5.91286542e+01 1.70500000e+03 1.97000000e+03 1.70500000e+03 1.70500000e+03 9.54706094e-01]
    #4 
    #[6.00000000e+00 3.62000000e-01 9.70000000e+00 5.35490910e+02 4.91774899e+01 2.21000000e+03 2.45500000e+03 2.21000000e+03 2.21000000e+03 9.65836744e-01]
    #5 
    #[6.00000000e+00 3.62000000e-01 8.80000000e+00 4.85712660e+02 6.09564247e+01 2.68000000e+03 2.90500000e+03 3.13000000e+03 2.68000000e+03 1.01576697e+00]
    #6
    #[6.00000000e+00 3.62000000e-01 7.70000000e+00 4.20858500e+02 4.78402525e+01 3.33500000e+03 3.54000000e+03 3.74500000e+03 3.33500000e+03 1.03571907e+00]
    #8
    #[6.00000000e+00 3.62000000e-01 7.00000000e+00 3.67078990e+02 5.32451974e+01 3.94000000e+03 4.13500000e+03 4.32500000e+03 4.51500000e+03 1.09754032e+00]
    #9 
    #[6.00000000e+00 3.62000000e-01 6.60000000e+00 3.09280620e+02 4.67361015e+01 4.70000000e+03 4.88500000e+03 5.07000000e+03 5.25500000e+03 9.78594146e-01]
    #10
#-> #[6.00000000e+00 3.62000000e-01 6.60000000e+00 2.61219000e+02 4.56493779e+01 5.44000000e+03 5.63000000e+03 5.82000000e+03 6.01000000e+03 1.03098633e+00]
    #11
#-> #[6.00000000e+00 3.62000000e-01 6.60000000e+00 2.17772470e+02 4.94959605e+01 6.20500000e+03 6.40500000e+03 6.62000000e+03 6.87000000e+03 1.01117467e+00]
    #12
    #[6.00000000e+00 3.62000000e-01 4.70000000e+00 1.64405810e+02 2.63526420e+01 7.02500000e+03 7.18000000e+03 7.33500000e+03 7.49000000e+03 9.61122803e-01]
    #13
#-> #[6.00000000e+00 3.62000000e-01 4.70000000e+00 1.36212440e+02 2.67686483e+01 7.65000000e+03 7.81000000e+03 7.97500000e+03 8.14500000e+03 9.73792750e-01]
    #14
    #[6.00000000e+00 3.62000000e-01 4.40000000e+00 1.08621370e+02 2.76331045e+01 8.30500000e+03 8.47000000e+03 8.66000000e+03 8.88500000e+03 1.02501005e+00]
    #15
    #[4.00000000e+00 3.62000000e-01 5.20000000e+00 8.21566500e+01 1.90145088e+01 9.14500000e+03 9.41000000e+03 9.41000000e+03 9.41000000e+03 9.93897960e-01]
    #16
    #[2.00000000e+00 3.62000000e-01 5.20000000e+00 6.32902600e+01 1.05723409e+01 9.41500000e+03 9.74500000e+03 9.74500000e+03 9.74500000e+03 1.04561007e+00]
    #17
    #[2.00000000e+00 3.62000000e-01 5.20000000e+00 6.10248900e+01 5.92697080e+01 1.01050000e+04 1.19000000e+04 1.19000000e+04 1.19000000e+04 1.04747824e+00]
    #  
    
    
    
    
    #13
    #[4.00000000e+00 3.62000000e-01 7.10000000e+00 1.49004690e+02 6.12729301e+01 7.78500000e+03 8.08000000e+03 8.38500000e+03 8.70000000e+03 9.62063700e-01]
    #14
    #[2.00000000e+00 3.62000000e-01 7.10000000e+00 9.38779400e+01 3.15391566e+01 9.06000000e+03 9.43500000e+03 9.43500000e+03 9.43500000e+03 1.00908021e+00]
    #15 
    #[2.00000000e+00 3.62000000e-01 5.60000000e+00 7.51836800e+01 7.34285026e+01 9.73500000e+03 1.19000000e+04 1.19000000e+04 1.19000000e+04 1.03843060e+00]
    #16
    # 
    #17
    # 
    ##########

    #n = 6 if x< 7.49 else 4 if #<8.7 else 2
    #m = 0.362
    #ribs = np.array([0, 0.375, 0.77, 1.090, 1.445, 1.705, 1.97, 2.21, 2.455, 2.68, 2.905, 3.13, 3.335, 3.54, 3.745, 3.94, 4.135, 4.325, 4.515, 4.7, 4.885, 5.07, 5.255, 5.44, 5.63, 5.82, 6.01, 6.205, 6.405, 6.62, 6.87, 7.025, 7.18, 7.335, 7.49, 7.785, 8.08, 8.385, 8.7, 9.06, 9.435, 9.735, 12])
    #t_lst = np.array([12.7e-3, 11.8e-3, 10.6e-3, 9.7e-3, 8.8e-3, 7.7e-3, 7.0e-3, 6.6e-3, 4.7e-3, 7.1e-3, 5.6e-3])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.77, 1.445, 1.97, 2.455, 3.13, 3.745, 4.515, 6.87, 7.49, 9.435, 12])
    #masses = [109, 86, 59, 49, 61, 48, 53, 47, 46, 49, 26, 61, 31, 73]
