import numpy as np
import pandas as pd
# import geopandas as gpd
from IPython.display import Image
# from shapely.geometry import Point, Polygon
from math import factorial
import datetime
import time
import scipy
from statsmodels.sandbox.regression.predstd import wls_prediction_std
from sklearn.linear_model import LinearRegression
from patsy import cr

from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sb

import os, os.path
import math
import sys


###########################################################


def add_human_start_time_by_system_start_time(HDF):
    """Returns human readable time (system_start_time)

    Arguments
    ---------
    HDF : dataframe

    Returns
    -------
    HDF : dataframe
        the same datafram with added column of human readable time.
    """
    HDF.system_start_time = HDF.system_start_time / 1000
    time_array = HDF["system_start_time"].values.copy()
    human_time_array = [time.strftime('%Y-%m-%d', time.localtime(x)) for x in time_array]
    HDF["human_system_start_time"] = human_time_array

    if type(HDF["human_system_start_time"]==str):
        HDF['human_system_start_time'] = pd.to_datetime(HDF['human_system_start_time'])
    return(HDF)



def _optimal_allocations(fund, log_ratio_profile, alphas):
    """Returns optimal allocations

    Arguments
    ---------
    fund : float
        Total amount of money we want to invest.

    log_ratio_profile : Array
        2D array of log rations of the stocks in the profile.
    alphas :  Array of floats
        Coefficients in the linear combination of log_ratios (please note this is not normalized!)
        of the stocks in the profile.

    Returns
    -------
    Allocations : Array
        1D array of optimial allocations
    """
    fraction_vector = 1 / linalg.norm(log_ratio_profile - np.mean(log_ratio_profile, axis=0), axis=0)
    
    # element-wise multiplication of alphas and log-ratios
    fraction_vector = np.multiply(fraction_vector[:, np.newaxis], alphas)
    C = fund / np.sum(fraction_vector)

    allocations = C * fraction_vector
    return allocations
