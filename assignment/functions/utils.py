# Utility functions for processing .csv data in assignment 6
import os
import glob
import natsort
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# get_files function:
def get_files(path_pattern): 
    """"files in data folder and end with ext .csv format """
    if isinstance(path_pattern,list):
        path_pattern = os.path.join(*path_pattern)
        
    files = natsort.natsorted(glob.glob(path_pattern))
    if not files:
        raise FileNotFoundError('pattern could not detectfiles(s)')
    
    return files

#DATA ALLIGNMENT- add following- find_middle() - find the middle index of input data column and returns it
#realign_data() - Center data around maximum or center of shortest column, padding with 0's, returns 1) a new dataframe with realigned columns and 2) the amount each column was shifted

#returns middle rounding down 
def find_middle(in_column):
    """find middle indx in column
    
    Args:
        in_column ([type]): [array or dataframe column]
    """
    middle = float(len(in_column))/2
    return int(np.floor(middle))

def realign_data(in_data, align='max'):
    """
    centers data around max or center of shortest column, pad with 0's
    
    Args:
        in_data: array of input data
        align (str): "max" or "center", max will provide shifts to align maximum of input data, wheras "center" will shift to middle index
        
    Returns:
        d - new dataframe with realigned data
        shifts - how each entry was shifted
    """
    x, y = in_data.shape
    d = pd.DataFrame(0, index=np.arange(x), columns=np.arange(y))
    
    shifts = np.zeros(y)
    #find longest length
    ind_longest = np.argmin((in_data == 0).astype(int).sum(axis=0).values)
    #find_ longest peak
    peak_longest = np.argmax(in_data.loc[:, ind_longest].values)
    #call middle function to find center point 
    mid_longest = find_middle(in_data.index[in_data[ind_longest]!=0].values)
                                            
    for column in in_data:                    
        if align == 'max':
            peak = np.argmax(in_data[column].values)
            pdiff = peak_longest - peak #how much to shift 
            d[column] = in_data[column].shift(periods=pdiff, fill_value=0)
            assert np.argmax(d[column]) == peak_longest
            shifts[column] = pdiff
        elif align == "center":
            mid = find_middle(in_data[column].values)
            mdiff = mid_longest - mid
            d[column] = in_data[column].shift(periods=mdiff, fill_value=0)
            assert find_middle(d[column]) == mid_longest
            shifts[column] = mdiff
    return d, shifts


