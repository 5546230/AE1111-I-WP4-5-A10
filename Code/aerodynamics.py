import numpy as np
import scipy as sp
from scipy import interpolate
from importing import get_lst

#get the uninterolated values
filename = "Data\MainWing_a=0.00_v=10.00ms.csv"
ylst, clst, ailst, Cllst, Cdilst, Cmlst = get_lst(filename)

#interplotion function
get_cl = sp.interpolate.interp1d(ylst, Cllst, kind="cubic", fill_value="extrapolate")

