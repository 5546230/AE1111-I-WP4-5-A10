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
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t_f, t_r, t, n_stringers, m*a_stringer) #Pa; flexure formula #On purpose 3*
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
        K = 1000
    elif (0.5 < slenderness) and (slenderness < 1):
        K = -83.333*(slenderness)**3+199.29*(slenderness)**2-160.67*(slenderness)+47.914
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
    n_0 = 6 #staring n value
    n_list = [6, 4, 2, 0] #number of ribs to check
    n = lambda x: n_0
    n_prev = n(0)-2
    m0 = 0.204 #starting m value
    t0 = 0.002 #m - starting t value

    #iteration values
    dt = 0.0001
    dm = 0.001
    dy = 0.01 #m

    #t is set
    t = lambda x: t0
    t_prev = t0
    
    m = m0
    #start of iteration
    y1_0 = 0.66 #m
    y2 = y1_0 + dy #m

    span_lim = 4 #runs until this spanwise location
    no_ribs_placed = 2 #places this many ribs (max 4). ALSO CHANGE "ind_out" ARRAY ACCORDINGLY

    n_rib = 0
    ribs = []

    if y1_0 == 0:
        m_lim = 0.4
    else:
        m_lim = m0

    # OUTPUT
    output = np.array([["n", "m", "t [mm]", "mass [kg]", "n_ribs", "rib 1 [mm]", "rib 2 [mm]", "t_stringer [mm]", "a [mm]"]])

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

        while t(0) < 0.015:
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
                n_u = n(y2)//2 #initial stringer arrangement should be kept
                K = stress_crit(y1, y2, t, n_u, n_0, y1_0)[1]
                slenderness = stress_crit(y1, y2, t, n_u, n_0, y1_0)[2]
                s_av = av_skin_stress(y1, y2, t_f, t_r, t(y1), a_stringer, load_max_compr, n(y1), m)
                s_crit = stress_crit(y1, y2, t, n_u, n_0, y1_0)[0]

                if s_av*1.05 < s_crit:
                    y2 += dy
                    s_av = av_skin_stress(y1, y2, t_f, t_r, t(y1), a_stringer, load_max_compr, n(y1), m)
                    s_crit = stress_crit(y1, y2, t, n_u, n_0, y1_0)[0]
                else: #Places a rib
                    y1 = y2
                    y2 = y1 + dy
                    ribs.append(y1)
                    s_av = av_skin_stress(y1, y2, t_f, t_r, t(y1), a_stringer, load_max_compr, n(y1), m)
                    s_crit = stress_crit(y1, y2, t, n_u, n_0, y1_0)[0]
                if y2 > span_lim-0.1:
                    ribs.append(span_lim-0.1)
                    y1 = span_lim-0.1
                    y2 = y1+dy
                if len(ribs)==no_ribs_placed:
                    mass =  mass_config_per_length(n(y1), m, y1_0, ribs[no_ribs_placed-1], t(y1), a_stringer)*(ribs[no_ribs_placed-1]-y1_0) + mass_remaining(ribs[no_ribs_placed-1])
                    ind_out = np.array([[int(n(y1)), m, round(t(y1)*10**3, 4), round(mass, 5), mass_bay(y1_0, ribs[no_ribs_placed-1], int(n(y1)), m, t(y1), a_stringer), round(ribs[0], 3)*10**3, round(ribs[no_ribs_placed-1], 3)*10**3, round(ribs[0], 3)*10**3, round(ribs[0], 3)*10**3]])
                    output = np.concatenate((output,ind_out))
                    n_rib = 0
                    y1 = y1_0 #m
                    y2 = y1 + dy #m
                    ribs = []
                    break
                
            t = lambda x: t_prev + dt
            t_prev += dt
            ribs = []
        counter += 1
    
    print(output[0,:])
    output = np.delete(output, 0, 0)
    output = output.astype(float)
    output = output[output[:, 3].argsort()]
    #output = output.astype(int)
    print(output)
    print(output[0,:])
    print(mass_config_per_length(output[0,0],output[0,1]*10**-2, y1_0, output[0,6]*10**-3, output[0,2]*10**-3, a_stringer)*(output[0,6]*10**-3-y1_0))

    with open('output.txt', 'w') as filehandle:
        json.dump(output.tolist(), filehandle)
    
    #ribs_list = np.array([0.64, 2.22, 2.61, 3.70, 4.00, 5.51, 5.34, 6.24, 7.04, 7.74, 8.05])
    #option1 = design_option_column((output[0, 1]*10**-2)*a_stringer, output[0, 0], 10, ribs_list, 0.007, t_f, t_r)
    #option1.generate_plot()

    #K = 0.0364*(slenderness)**2 - 0.3815*(slenderness) + 4.2206 <- scrap

    ### config data ### - log your simulation here
    #n = 6
    #m = 0.82
    #ribs = np.array([0, 0.33, 0.66,])
    #t_lst = np.array([13.7e-3, ])
    #list of the upper limits of the thickness values above. Make sure they have the same length
    #y_lst = np.array([0.66, ])
    #masses = [123.5, ]

    ###########