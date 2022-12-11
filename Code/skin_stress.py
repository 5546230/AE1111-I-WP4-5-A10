import numpy as np
import scipy as sp
from Moment_of_inertia import get_ixx
from load_case import LoadCase
from interpolation import *
#test
I = get_ixx(4, 2*10**-3)
c = get_c(4)
print(I, c)