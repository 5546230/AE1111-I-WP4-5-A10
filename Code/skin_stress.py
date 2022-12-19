import json
import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *
from Weight_diagram import get_mass
from matplotlib import pyplot as plt

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"
#Commented lines are sometimes for debug

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

def stress_crit(y1, y2, t, n_u):
    if n_u == 6:
        slenderness = ((n_u+1)*(y2-y1))/(0.55*get_c(y1))
    else:
        slenderness = (0.5*(n_u+1)*(y2-y1))/(0.55*get_c(y1)) #a over b
    K = max(3.9617*np.e**(-0.046*slenderness), 3) #for linearly varying moment
    sigma_crit = ( ((t**2)*E*(np.pi**2)) / (12*(1-nu**2)) ) * ( ((n_u+1) / (0.55*get_c(y1)))**2 ) * K
    return sigma_crit, K

def mass_remaining(y_0):
    m_r = sp.integrate.quad(get_mass, y_0, 12)[0]
    return m_r

def mass_config_per_length(n, m, y1, y2, t):
    m_config = 2700*(n*m*a_stringer+1.101*get_c(0.5*(y1+y2))*t) #assumes that m/l at the middle of the bay is the avg m/l
    return m_config

if __name__=="__main__":
    ###IMPORT HERE TO PREVENT CIRCULAR IMPORTATION###
    from column_buckling import *
    #data
    b = 24 #m
    E = 68e9 #Pa
    nu = 0.33 #-

    #default is option 3
    design_option = str(3)
    #design_option = str(input("Design option (1, 2 or 3):", ))

    ################# INPUT ###################
    n = 4
    m0 = 0.07 # < 1 makes much more sense
    t0 = 0.002 #m
    iterated = False

    # OUTPUT
    output = np.array([["n", "m", "t [mm]", "mass [kg]", "n_ribs", "rib 1 [mm]", "rib 2 [mm]", "t_stringer [mm]", "a [mm]"]])

    #design options parameters (n_stringers, t, ...)
    designs = {
        "1":dict(t = 4, n_stringers = 0, a_stringer = 0),
        "2":dict(t = 1.5, n_stringers = 2, a_stringer = (65e-3)**2),
        "3":dict(t = 2, n_stringers = n, a_stringer = (35e-3)**2)
    }

    n_stringers = designs[design_option]["n_stringers"]
    n_u = n_stringers//2
    #t = designs[design_option]["t"]*1e-3 #m
    a_stringer = designs[design_option]["a_stringer"] #m^2

    t_f = 5.5*10**-3 #mm
    t_r = 4*10**-3 #mm

    #assumed stringer thickness just for the sake of understanding what is going on. Has nothing to do with actual stringer thickness
    t_stringer = 0.005 #m
    # calculated stringer side length (approx.) for similar reasons as above
    a = (m0*a_stringer/(2*t_stringer)) * 10**3 #mm

    #load case for maximum compression in upper skin panels
    load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    ########## Rib placement ##########
    # iterated thickness and stringer area carries through
    dt = 0.0001
    dm = 0.02
    dy = 0.01 #m

    #t is set
    t = t0
    #n is set
    #m starts from 0.1
    m = m0
    y1_0 = 8.05 #m
    y2 = y1_0 + dy #m

    #s_av = av_skin_stress(y1, y2, t0, a_stringer)
    #s_crit, K = stress_crit(y1, y2, t0)

    n_rib = 0
    ribs = []

    s_av = av_skin_stress(y1_0, y2, t_f, t_r, t, a_stringer, load_max_compr, n, m0)
    s_crit = stress_crit(y1_0, y2, t, n_u)[0]

    for n in range(4,12, 2):
        m = m0
        while m < 0.08:
            t = t0
            ######### thickness iteration ##########
            # iterates on thickness if needed
            sigma_yield = 271*10**6
            s = skin_stress(y1_0, t_f, t_r, t, a_stringer, load_max_compr, n, m)
            #print(s)

            while s > sigma_yield:
                iterated = True
                t += 0.0001
                #print(get_ixx(0, t, n_stringers, m*a_stringer))
                s = skin_stress(y1_0, t_f, t_r, t, a_stringer, load_max_compr, n, m)

            ##########
            while t < 0.012:
                y1 = y1_0 #m
                y2 = y1 + dy #m
                while y2 < 12:
                    n_u = 12//2 #initial stringer arrangement should be kept
                    K = stress_crit(y1, y2, t, n_u)[1]
                    s_av = av_skin_stress(y1, y2, t_f, t_r, t, a_stringer, load_max_compr, n, m)
                    s_crit = stress_crit(y1, y2, t, n_u)[0]
                    if s_av < s_crit:
                        #print("Average stress ", int(s_av*10**-6), "\n")
                        #print("Critical sress", int(s_crit*10**-6), "\n")
                        y2 += dy
                        s_av = av_skin_stress(y1, y2, t_f, t_r, t, a_stringer, load_max_compr, n, m)
                        s_crit = stress_crit(y1, y2, t, n_u)[0]
                    else: #Places a rib
                        #print("\n", "Average stress ", int(s_av*10**-6),)
                        #print("Critical sress", int(s_crit*10**-6),)
                        #print("R ib at ", round(y2, 3), " m spanwise")
                        #n_rib += 1
                        y1 = y2
                        y2 = y1 + dy
                        ribs.append(y1)
                        s_av = av_skin_stress(y1, y2, t_f, t_r, t, a_stringer, load_max_compr, n, m)
                        s_crit = stress_crit(y1, y2, t, n_u)[0]
                    if len(ribs)==2:
                        a = ((m*a_stringer+t_stringer**2)/(2*t_stringer))
                        mass =  mass_config_per_length(n, m, y1_0, ribs[1], t)*(ribs[1]-y1_0) + mass_remaining(ribs[1])
                        ind_out = np.array([[int(n), round(m*10**2, 3), round(t*10**3, 4), round(mass, 5), int(n_rib), round(ribs[0], 3)*10**3, round(ribs[1], 3)*10**3, round(ribs[0], 3)*10**3, round(ribs[0], 3)*10**3]])
                        output = np.concatenate((output,ind_out))
                        n_rib = 0
                        y1 = y1_0 #m
                        y2 = y1 + dy #m
                        ribs = []
                        break
                t += dt
                ribs = []
            m += dm
    
    print(output[0,:])
    output = np.delete(output, 0, 0)
    output = output.astype(float)
    output = output[output[:, 3].argsort()]
    #output = output.astype(int)
    print(output)
    print(output[0,:])
    print(mass_config_per_length(output[0,0],output[0,1]*10**-2, y1_0, output[0,6]*10**-3, output[0,2]*10**-3)*(output[0,6]*10**-3-y1_0))

    #mass_stored = (5000, 1)
    #r, c = output.shape[0], output.shape[1]
#
    #for i in range(1, r):
    #    mass_local = float(output[i, 3])
    #    if mass_local < mass_stored[0]:
    #        mass_stored = (mass_local, i) 
    
    #print(output[mass_stored[1]])

    with open('output.txt', 'w') as filehandle:
        json.dump(output.tolist(), filehandle)
    
    ribs_list = np.array([0.64, 2.22, 2.61, 3.70, 4.00, 5.51, 5.34, 6.24, 7.04, 7.74, 8.05])
    option1 = design_option_column((output[0, 1]*10**-2)*a_stringer, output[0, 0], 10, ribs_list, 0.007, t_f, t_r)
    option1.generate_plot()

    #print("\n", "Number of ribs: ", n_rib)

    #print("\n", "a = ", round(a, 3), " mm")

    #print("\n", "thickness", round(t*10**3, 3), " mm")
    #print("270 000 000 >", s)
    #print("mass/unit length", 2700*(n_stringers*a_stringer+1.101*get_c(0)*t), "\n")


    #Work in progress
    #K = 0.0364*(slenderness)**2 - 0.3815*(slenderness) + 4.2206 <- scrap

    ###########