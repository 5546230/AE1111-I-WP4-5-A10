import numpy as np

def get_lst(filename: str)->np.ndarray:
    '''import the data file'''
    #get a numpy array of the data with the header and footer skipped
    lst = np.genfromtxt(
        filename, 
        skip_footer=True, 
        skip_header=True
    )

    #store all paramters in it's own lists
    ylst = lst[0]
    clst = lst[1]
    ailst = lst[2]
    Cllst = lst[3]
    Cdilst = lst[5]
    Cmlst = lst[7]

    #return the lists
    return ylst, clst, ailst, Cllst, Cdilst, Cmlst
