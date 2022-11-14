import numpy as np

def get_lst(filename: str)->np.ndarray:
    '''import the data file'''
    #get a numpy array of the data with the header and footer skipped
    lst = np.genfromtxt(
        filename, 
        skip_footer=True, 
        skip_header=True
    )
    return lst

