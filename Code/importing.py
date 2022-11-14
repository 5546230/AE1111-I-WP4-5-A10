import numpy as np
from scipy import interpolate

def get_lst(filename: str) -> np.ndarray:
    '''import the data file from XFLR5 and extract the values'''
    #get a numpy array of the data with the header and footer skipped
    lst = np.genfromtxt(
        filename, 
        delimiter=",",
        skip_header= 21,
        skip_footer=2523
    )

    #transpose to get colums
    lst = lst.T

    #store all paramters in it's own lists
    ylst = lst[0]
    clst = lst[1]
    ailst = lst[2]
    Cllst = lst[3]
    Cdilst = lst[5]
    Cmlst = lst[7]

    #return the lists!
    return ylst, clst, ailst, Cllst, Cdilst, Cmlst