####
#### Nov. 8, 2021
####


import csv
import numpy as np
import pandas as pd
from IPython.display import Image
from math import factorial
import datetime
import time
import scipy
import scipy.signal
import os, os.path
from patsy import cr
import matplotlib.pyplot as plt
import seaborn as sb


import sys
start_time = time.time()

# search path for modules
# look @ https://stackoverflow.com/questions/67631/how-to-import-a-module-given-the-full-path
####################################################################################
###
###                      Aeolus Core path
###
####################################################################################

sys.path.append('/home/hnoorazar/NASA/')
import NASA_core as nc
import NASA_plot_core as ncp

####################################################################################
###
###      Parameters                   
###
####################################################################################

indeks = sys.argv[1]
SEOS_cut = int(sys.argv[2])
randCount = sys.argv[3]
###
### White SOS and EOS params
###
onset_cut = int(SEOS_cut)/10.0 # grab the first digit as SOS cut
offset_cut = onset_cut

print("SEOS_cut is {}.".format(SEOS_cut))
print("onset_cut is {} and offset_cut is {}.".format(onset_cut, offset_cut))

####################################################################################
###
###                   Aeolus Directories
###
####################################################################################
data_dir = "/data/hydro/users/Hossein/NASA/05_SG_TS/"
SOS_table_dir = "/data/hydro/users/Hossein/NASA/06_SOS_tables/"

output_dir = SOS_table_dir + str(int(onset_cut*10)) + "_EOS" + str(int(offset_cut*10)) + "/"
os.makedirs(output_dir, exist_ok=True)

if randCount == "all":
    f_name = "04_SG_int_Grant_Irr_2008_2018_" + indeks + "_" + ".csv"
    out_name = output_dir + "05_SOS_SG_int_Grant_Irr_2008_2018_" + indeks + ".csv"
else:
    f_name = "04_SG_int_Grant_Irr_2008_2018_" + indeks + "_" + str(randCount) + "randomfields.csv"
    out_name = output_dir + "05_SOS_SG_int_Grant_Irr_2008_2018_" + indeks + "_" + str(randCount) + "randomfields.csv"

print ("_________________________________________________________")
print ("data dir is: " + data_dir)
print ("_________________________________________________________")
print ("output_dir is: " +  output_dir)
print ("_________________________________________________________")

####################################################################################
###
###                   Read data
###
####################################################################################

a_df = pd.read_csv(data_dir + f_name, low_memory=False)
a_df['human_system_start_time'] = pd.to_datetime(a_df['human_system_start_time'])

#
# Toss perennials and alfalfa (This step will be done in creating the confusion table.)
#
# a_df = a_df[a_df['CropTyp'].isin(annual_crops.Crop_Type)]

print ("columns of a_df right after reading is: ")
print (a_df.columns)



####################################################################################
###
###                   process data
###
####################################################################################
a_df.reset_index(drop=True, inplace=True)
a_df = nc.initial_clean(df = a_df, column_to_be_cleaned = indeks)
a_df = a_df.copy()

### List of unique polygons
polygon_list = a_df['ID'].unique()

print ("_________________________________________________________")
print("polygon_list is of length {}.".format(len(polygon_list)))

# 
# 25 columns
#
SEOS_output_columns = ['ID', indeks, 'human_system_start_time', 
                       'EVI_ratio', 'SOS', 'EOS', 'season_count']

#
# The reason I am multiplying len(a_df) by 4 is that we can have at least two
# seasons which means 2 SOS and 2 EOS. So, at least 4 rows are needed.
# and the reason for 14 is that there are 14 years from 2008 to 2021.
all_poly_and_SEOS = pd.DataFrame(data = None, 
                                 index = np.arange(4*14*len(a_df)), 
                                 columns = SEOS_output_columns)
counter = 0
pointer_SEOS_tab = 0
###########
###########  Re-order columns of the read data table to be consistent with the output columns
###########
a_df = a_df[SEOS_output_columns[0:3]]

for a_poly in polygon_list:
    if (counter % 10 == 0):
        print ("_________________________________________________________")
        print ("counter: " + str(counter))
        print (a_poly)
    curr_field = a_df[a_df['ID']==a_poly].copy()
    # Sort by human_system_start_time (sanitary check)
    curr_field.sort_values(by=['human_system_start_time'], inplace=True)
    curr_field.reset_index(drop=True, inplace=True)

    # extract unique years. Should be 2008 thru 2021.
    # unique_years = list(pd.DatetimeIndex(curr_field['human_system_start_time']).year.unique())
    unique_years = curr_field['human_system_start_time'].dt.year.unique()
    
    """
    detect SOS and EOS in each year
    """
    for yr in unique_years:
        curr_field_yr = curr_field[curr_field['human_system_start_time'].dt.year == yr].copy()

        # Orchards EVI was between more than 0.3
        y_orchard = curr_field_yr[curr_field_yr['human_system_start_time'].dt.month >= 5]
        y_orchard = y_orchard[y_orchard['human_system_start_time'].dt.month <= 10]
        y_orchard_range = max(y_orchard[indeks]) - min(y_orchard[indeks])

        if y_orchard_range > 0.3:
            #######################################################################
            ###
            ###             find SOS and EOS, and add them to the table
            ###
            #######################################################################
            curr_field_yr = nc.addToDF_SOS_EOS_White(pd_TS = curr_field_yr, 
                                                     VegIdx = indeks, 
                                                     onset_thresh = onset_cut, 
                                                     offset_thresh = offset_cut)

            ##
            ##  Kill false detected seasons 
            ##
            curr_field_yr = nc.Null_SOS_EOS_by_DoYDiff(pd_TS=curr_field_yr, min_season_length=40)

            #
            # extract the SOS and EOS rows 
            #
            SEOS = curr_field_yr[(curr_field_yr['SOS'] != 0) | curr_field_yr['EOS'] != 0]
            SEOS = SEOS.copy()
            # SEOS = SEOS.reset_index() # not needed really
            SOS_tb = curr_field_yr[curr_field_yr['SOS'] != 0]
            if len(SOS_tb) >= 2:
                SEOS["season_count"] = len(SOS_tb)
                # re-order columns of SEOS so they match!!!
                SEOS = SEOS[all_poly_and_SEOS.columns]
                all_poly_and_SEOS[pointer_SEOS_tab:(pointer_SEOS_tab+len(SEOS))] = SEOS.values
                pointer_SEOS_tab += len(SEOS)
            else:
                # re-order columns of fine_granular_table so they match!!!
                curr_field_yr["season_count"] = 1
                curr_field_yr = curr_field_yr[all_poly_and_SEOS.columns]

                aaa = curr_field_yr.iloc[0].values.reshape(1, len(curr_field_yr.iloc[0]))
                
                all_poly_and_SEOS.iloc[pointer_SEOS_tab:(pointer_SEOS_tab+1)] = aaa
                pointer_SEOS_tab += 1
        else: 
            """
             here are potentially apples, cherries, etc.
             we did not add EVI_ratio, SOS, and EOS. So, we are missing these
             columns in the data frame. So, use 666 as proxy
            """
            aaa = np.append(curr_field_yr.iloc[0], [666, 666, 666, 1])
            aaa = aaa.reshape(1, len(aaa))
            all_poly_and_SEOS.iloc[pointer_SEOS_tab:(pointer_SEOS_tab+1)] = aaa
            pointer_SEOS_tab += 1

        counter += 1

####################################################################################
###
###                   Write the outputs
###
####################################################################################
all_poly_and_SEOS = all_poly_and_SEOS[0:(pointer_SEOS_tab)]
all_poly_and_SEOS.to_csv(out_name, index = False)


print ("done")
end_time = time.time()
print(end_time - start_time)


