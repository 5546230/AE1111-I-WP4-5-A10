import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *
from Weight_diagram import get_Weight, fuel_weight

#background info is on page 671 in pdf "73 Bruhn analysis and design of flight vehicles.pdf"

#assumed distance from NA is the upper left corner of the wing box (conservative)
def skin_stress(y, t_f, t_r, t, a_stringer, load_max_compr, n_stringers):
    sigma = load_max_compr.z2_moment(y)*(0.5*0.114)*get_c(y)/get_ixx(y, t_f, t_r, t, n_stringers, m*a_stringer) #Pa; flexure formula #On purpose 3*
    return sigma

def av_skin_stress(y1, y2, t_f, t_r, t, a_stringer):
    sigma_av = 0.5*(skin_stress(y1, t_f, t_r, t, a_stringer)+skin_stress(y2, t_f, t_r, t, a_stringer))
    return sigma_av

#def ratio():
    ratio = []
    for i in range(5, int(b/2)+1):
        r = skin_stress(5)/skin_stress(i+1)
        ratio.append(r)
    return ratio

def stress_crit(y1, y2, t):
    slenderness = ((n_u+1)*(y2-y1))/(0.55*get_c(y1)) #a over b
    K = 0.0364*(slenderness)**2 - 0.3815*(slenderness) + 4.2206 #for linearly varying moment
    sigma_crit = ( ((t**2)*E*(np.pi**2)) / (12*(1-nu**2)) ) * ( ((n_u+1) / (0.55*get_c(y1)))**2 ) * K
    return sigma_crit, K

def mass_remaining(y_0):
    m_r = sp.integrate.quad(get_Weight-fuel_weight, y_0, 12)[0]
    return m_r

if __name__=="__main__":
    #data
    b = 24 #m
    E = 68e9 #Pa
    nu = 0.33 #-

    #default is option 3
    design_option = str(3)
    #design_option = str(input("Design option (1, 2 or 3):", ))

    # INPUT
    n = 4
    m = 0.1 # < 1 makes much more sense
    t = 0.004 #m
    iterated = False

    # OUTPUT
    output = np.array()
    ind_out= [[], #n
    [],  #m
    [],  #t
    []]  #mass/length

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
    a = (m*a_stringer/(2*t_stringer)) * 10**3 #mm

    #load case for maximum compression in upper skin panels
    load_max_compr = LoadCase(2.62*1.5, 16575.6*9.80665, 250.79, 12500)

    ######### thickness iteration ##########
    # iterates on thickness if needed
    sigma_yield = 271*10**6
    s = skin_stress(0, t, a_stringer)
    #print(s)

    while s > sigma_yield:
        iterated = True
        t += 0.0001
        #print(get_ixx(0, t, n_stringers, m*a_stringer))
        s = skin_stress(0, t, a_stringer)

    ##########

    ########## Rib placement ##########
    # iterated thickness and stringer area carries through

    dy = 0.1 #m
    y1 = 0 #m
    y2 = y1 + dy #m

    s_av = av_skin_stress(y1, y2, t, a_stringer)
    s_crit, K = stress_crit(y1, y2, t)

    n_rib = 0

    #print(s_av*10**-6)
    #print(stress_crit(y1, y2, t)[0]*10**-6, "\n", K, "\n")

    for n in range(4,22, 2):
        while m < 1.5:
            while t < 0.02:
                while y2 < b/4:
                    if s_av < s_crit:
                        #print("Average stress ", int(s_av*10**-6), "\n")
                        #print("Critical sress", int(s_crit*10**-6), "\n")
                        y2 += dy
                        s_av = av_skin_stress(y1, y2, t, a_stringer)
                        s_crit = stress_crit(y1, y2, t)[0]
                    else:
                        print("\n", "Average stress ", int(s_av*10**-6),)
                        print("Critical sress", int(s_crit*10**-6),)
                        print("Rib at ", round(y2, 3), " m spanwise")
                        n_rib += 1
                        y1 = y2
                        y2 = y1 + dy
                        s_av = av_skin_stress(y1, y2, t, a_stringer)
                        s_crit = stress_crit(y1, y2, t)[0]

    print("\n", "Number of ribs: ", n_rib)

    print("\n", "a = ", round(a, 3), " mm")

    print("\n", "thickness", round(t*10**3, 3), " mm")
    #print("270 000 000 >", s)
    #print("mass/unit length", 2700*(n_stringers*a_stringer+1.101*get_c(0)*t), "\n")


    #Work in progress

    ###########