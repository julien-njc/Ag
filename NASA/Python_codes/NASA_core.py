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

###
### These will be more generalized functions of remote_sensing_core.py
### Hence, less hard coding, which implies column/variavle wise we
### will be minimalistic. e.g. column: lastSurveydate should not be included
### here.
###

###########################################################


def correct_big_jumps_1DaySeries(dataTMS_jumpie, give_col, maxjump_perDay = 0.015):
    """
    in the function correct_big_jumps_preDefinedJumpDays(.) we have
    to define the jump_amount and the no_days_between_points.
    For example if we have a jump more than 0.4 in less than 20 dats, then
    that is an outlier detected.
    
    Here we modify the approach to be flexible in the following sense:
    if the amount of increase in NDVI is more than #_of_Days * 0.02 then 
    an outlier is detected and we need interpolation.
    
    0.015 came from the SG based paper that used 0.4 jump in NDVI for 20 days.
    That translates into 0.02 = 0.4 / 20 per day.
    But we did choose 0.015 as default
    """
    dataTMS = dataTMS_jumpie.copy()
    dataTMS = initial_clean(df = dataTMS, column_to_be_cleaned = give_col)
    dataTMS.sort_values(by=['human_system_start_time'], inplace=True)
    dataTMS.reset_index(drop=True, inplace=True)

    thyme_vec = dataTMS['human_system_start_time'].values.copy()
    Veg_indks = dataTMS[give_col].values.copy()

    time_diff = (pd.to_datetime(thyme_vec[1:]) - pd.to_datetime(thyme_vec[0:len(thyme_vec)-1])[0]).days

    Veg_indks_diff = Veg_indks[1:] - Veg_indks[0:len(thyme_vec)-1]
    jump_indexes = np.where(Veg_indks_diff > maxjump_perDay)
    jump_indexes = jump_indexes[0]


    thyme_vec = dataTMS['system_start_time'].values.copy()
    Veg_indks = dataTMS[give_col].values.copy()

    time_diff = thyme_vec[1:] - thyme_vec[0:len(thyme_vec)-1]
    time_diff_in_days = time_diff / 86400
    time_diff_in_days = time_diff_in_days.astype(int)

    Veg_indks_diff = Veg_indks[1:] - Veg_indks[0:len(thyme_vec)-1]
    jump_indexes = np.where(Veg_indks_diff > maxjump_perDay)
    jump_indexes = jump_indexes[0]

    jump_indexes = jump_indexes.tolist()

    # It is possible that the very first one has a big jump in it.
    # we cannot interpolate this. so, lets just skip it.
    if len(jump_indexes) > 0: 
        if jump_indexes[0] == 0:
            jump_indexes.pop(0)
    
    if len(jump_indexes) > 0:    
        for jp_idx in jump_indexes:
            if  Veg_indks_diff[jp_idx] >= (time_diff_in_days[jp_idx] * maxjump_perDay):
                #
                # form a line using the adjacent points of the big jump:
                #
                x1, y1 = thyme_vec[jp_idx-1], Veg_indks[jp_idx-1]
                x2, y2 = thyme_vec[jp_idx+1], Veg_indks[jp_idx+1]
                # print (x1)
                # print (x2)
                m = np.float(y2 - y1) / np.float(x2 - x1) # slope
                b = y2 - (m*x2)           # intercept

                # replace the big jump with linear interpolation
                Veg_indks[jp_idx] = m * thyme_vec[jp_idx] + b

    dataTMS[give_col] = Veg_indks
    return(dataTMS)


def initial_clean(df, column_to_be_cleaned):
    dt_copy = df.copy()
    # remove the useles system:index column
    if ("system:index" in list(dt_copy.columns)):
        dt_copy = dt_copy.drop(columns=['system:index'])
    
    # Drop rows whith NA in column_to_be_cleaned column.
    dt_copy = dt_copy[dt_copy[column_to_be_cleaned].notna()]

    if (column_to_be_cleaned in ["NDVI", "EVI"]):
        dt_copy.loc[dt_copy[column_to_be_cleaned] > 1, column_to_be_cleaned] = 1
        dt_copy.loc[dt_copy[column_to_be_cleaned] < -1, column_to_be_cleaned] = -1

    return (dt_copy)


def fill_theGap_linearLine(a_regularized_TS, V_idx="NDVI"):
    """Returns a dataframe that has replaced the missing parts of regular_TS.

    Arguments
    ---------
    regular_TS : dataframe
        A regularized (data points are squidistant from each other) dataframe
        with missing data points; -1.5 is indication of missing values.
        This dataframe is the output of the function regularize_a_field(.)
        We will assume the regular_TS is for a given unique field from a given unique satellite.

    V_idx : String
        A string indicating which column/VI should be filled in.

    Returns
    -------
    regular_TS : dataframe
        the same dataframe with missing data points filled in by linear interpolation
    """
    # a_regularized_TS = regular_TS.copy()

    TS_array = a_regularized_TS[V_idx].copy().values

    aaa = a_regularized_TS["human_system_start_time"].values[1]
    bbb = a_regularized_TS["human_system_start_time"].values[0]
    time_step_size = (aaa - bbb).astype('timedelta64[D]')/np.timedelta64(1, 'D')

    """
    -1.5 is an indicator of missing values, i.e. a gap.
    The -1.5 was used as indicator in the function regularize_movingWindow_windowSteps_2Yrs()
    """
    missing_indicies = np.where(TS_array == -1.5)[0]
    Notmissing_indicies = np.where(TS_array != -1.5)[0]

    #
    #    Check if the first or last k values are missing
    #    if so, replace them with proper number and shorten the task
    #
    left_pointer = Notmissing_indicies[0]
    right_pointer = Notmissing_indicies[-1]

    if left_pointer > 0:
        TS_array[:left_pointer] = TS_array[left_pointer]

    if right_pointer < (len(TS_array) - 1):
        TS_array[right_pointer:] = TS_array[right_pointer]
    #    
    # update indexes.
    #
    missing_indicies = np.where(TS_array == -1.5)[0]
    Notmissing_indicies = np.where(TS_array != -1.5)[0]

    # left_pointer = Notmissing_indicies[0]
    stop = right_pointer
    right_pointer = left_pointer + 1

    missing_indicies = np.where(TS_array == -1.5)[0]

    while len(missing_indicies) > 0:
        left_pointer = missing_indicies[0] - 1
        left_value = TS_array[left_pointer]
        right_pointer = missing_indicies[0]

        while TS_array[right_pointer] == -1.5:
            right_pointer += 1
        right_value = TS_array[right_pointer]

        if (right_pointer - left_pointer) == 2:
            # if there is a single gap, then we have just average of the
            # values
            # Avoid extra computation!
            #
            TS_array[left_pointer + 1] = 0.5 * (TS_array[left_pointer] + TS_array[right_pointer])
            missing_indicies = np.where(TS_array == -1.5)[0]
        else:
            # form y = ax + b
            # to see what the "x_axis" was look at the same function in remote_sensing_core.py

            # denom = (x_axis[right_pointer]-x_axis[left_pointer]).astype('timedelta64[D]')/ \
            # np.timedelta64(int(time_step_size), 'D')
            
            denom = right_pointer - left_pointer
            slope = (right_value - left_value) / denom
            
            # b = right_value - (slope * x_axis[right_pointer])
            # 150 is a random number below. 
            # The thing that matters is the number of steps, not actual values on x-axis.
            # I did it this way to avoid dealing with timestamp values and figuring out its stuff
            # Stuff means both finding out the right script and relation of timestamp to day of year stuff.
            # We can just use right_pointer itself instead of 150!
            b = right_value - (slope * right_pointer)
            TS_array[left_pointer+1 : right_pointer] = slope * np.arange(right_pointer-denom+1, right_pointer)+b
            missing_indicies = np.where(TS_array == -1.5)[0]
            
        
    a_regularized_TS[V_idx] = TS_array
    return (a_regularized_TS)



def regularize_a_field(a_df, V_idks="NDVI", interval_size=10):
    """Returns a dataframe where data points are interval_size-day apart.
       This function regularizes the data between the minimum and maximum dates
       present in the data. 

    Arguments
    ---------
    a_df : dataframe 
           of a given field for only one satellite

    Returns
    -------
    regularized_df : dataframe
    """
    if not("human_system_start_time" in a_df.columns):
        a_df = add_human_start_time_by_system_start_time(a_df)

    assert (len(a_df.ID.unique()) == 1)
    assert (len(a_df.dataset.unique()) == 1)
    #
    # see how many days there are between the first and last image
    #
    a_df_coverage_days = (max(a_df.human_system_start_time) - min(a_df.human_system_start_time)).days
    assert (a_df_coverage_days >= interval_size)

    # see how many data points we need in terms of interval_size-day intervals for a_df_coverage_days
    no_steps = a_df_coverage_days // interval_size

    # initialize output dataframe
    regular_cols = ['ID', 'dataset', 'human_system_start_time', V_idks]
    regular_df = pd.DataFrame(data = None, 
                              index = np.arange(no_steps), 
                              columns = regular_cols)

    regular_df['ID'] = a_df.ID.unique()[0]
    regular_df['dataset'] = a_df.dataset.unique()[0]


    # the following is an array of time stamps where each entry is the beginning
    # of the interval_size-day period
    regular_time_stamps = pd.date_range(min(a_df.human_system_start_time), 
                                        max(a_df.human_system_start_time), 
                                        freq=str(interval_size)+'D')

    if len(regular_time_stamps) == no_steps+1:
        regular_df.human_system_start_time = regular_time_stamps[:-1]
    elif len(regular_time_stamps) == no_steps:
        regular_df.human_system_start_time = regular_time_stamps
    else:
        raise ValueError(f"There is a mismatch between no. days needed and '{interval_size}-day' interval array!")


    # Pick the maximum of every interval_size-days
    # for row_or_count in np.arange(len(no_steps)-1):
    #     curr_time_window = a_df[a_df.human_system_start_time >= first_year_steps[row_or_count]]
    #     curr_time_window = curr_time_window[curr_time_window.doy < first_year_steps[row_or_count+1]]

    #     if len(curr_time_window)==0: 
    #         regular_df.loc[row_or_count, V_idks] = -1.5
    #     else:
    #         regular_df.loc[row_or_count, V_idks] = max(curr_time_window[V_idks])

    #     regular_df.loc[row_or_count, 'image_year'] = curr_year
    #     regular_df.loc[row_or_count, 'doy'] = first_year_steps[row_or_count]

    for start_date in regular_df.human_system_start_time:
        """
          The following will crate an array (of length 2)
          it goes from a day to 10 days later; end points of the interval_size-day interval.

                # Here we add 1 day to the right end point (end_date)
          because the way pandas/python slices the dataframe; 
          does not include the last row of sub-dataframe
        """
        dateRange = pd.date_range(start_date, 
                                  start_date + pd.Timedelta(days=interval_size-1), 
                                  freq = str(1)+'D')
        assert (len(dateRange) == interval_size)

        curr_time_window = a_df[a_df.human_system_start_time.isin(dateRange)]
        if len(curr_time_window)==0:
            regular_df.loc[regular_df.human_system_start_time == start_date, V_idks] = -1.5
        else:
            regular_df.loc[regular_df.human_system_start_time == start_date, V_idks] = max(curr_time_window[V_idks])

    return (regular_df)


def set_negatives_to_zero(df, indeks="NDVI"):
    df.loc[df[indeks] < 0 , indeks] = 0
    return (df)


def clip_outliers(df, idx="NDVI"):
    # dt_copy = df.copy()
    df.loc[df[idx] > 1, idx] = 1
    df.loc[df[idx] <- 1, idx] = -1
    return(df)


def add_human_start_time_by_system_start_time(HDF):
    """Returns human readable time (conversion of system_start_time)

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


