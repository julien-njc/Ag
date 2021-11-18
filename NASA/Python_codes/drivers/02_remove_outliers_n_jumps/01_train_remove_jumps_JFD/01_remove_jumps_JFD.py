####
#### Nov 16, 2021
####

"""
  Regularize the EVI and NDVI of fields in individual years for training set creation.
"""

import csv
import numpy as np
import pandas as pd
from math import factorial
import scipy
import scipy.signal
import os, os.path
from datetime import date
import datetime
import time
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
county = sys.argv[2]
print ("Terminal Arguments are: ")
print (indeks)
print (county)
print ("__________________________________________")

if indeks == "NDVI":
    NoVI = "EVI"
else:
    NoVI = "NDVI"

IDcolName = "ID"
####################################################################################
###
###                   Aeolus Directories
###
####################################################################################
data_base = "/data/hydro/users/Hossein/NASA/"
data_dir = data_base + "/02_outliers_removed/"
output_dir = data_base + "/03_jumps_removed/"
os.makedirs(output_dir, exist_ok=True)

print ("data_dir is: " +  data_dir)
print ("output_dir is: " + output_dir)
########################################################################################
###
###                   process data
###
########################################################################################

f_name = "noOutlier_" + county + "_" +  indeks + ".csv"
out_name = output_dir + "NoJump_" + county + "_" + indeks + "_JFD.csv"

an_EE_TS = pd.read_csv(data_dir + f_name, low_memory=False)
an_EE_TS['human_system_start_time'] = pd.to_datetime(an_EE_TS['human_system_start_time'])
an_EE_TS["ID"] = an_EE_TS["ID"].astype(str)

########################################################################################
###
### List of unique polygons
###
IDs = an_EE_TS[IDcolName].unique()
print(len(IDs))

########################################################################################
###
###  initialize output data.
###

output_df = pd.DataFrame(data = None,
                         index = np.arange(an_EE_TS.shape[0]), 
                         columns = an_EE_TS.columns)

counter = 0
row_pointer = 0

for a_poly in IDs:
    if (counter % 1000 == 0):
        print (counter)
    curr_field = an_EE_TS[an_EE_TS[IDcolName]==a_poly].copy()
    
    ################################################################
    # Sort by DoY (sanitary check)
    curr_field.sort_values(by=['human_system_start_time'], inplace=True)
    curr_field.reset_index(drop=True, inplace=True)
    
    ################################################################
    no_Outlier_TS = nc.correct_big_jumps_1DaySeries_JFD(dataTMS_jumpie = curr_field, 
                                                        give_col = indeks, 
                                                        maxjump_perDay = 0.018)

    output_df[row_pointer: row_pointer + curr_field.shape[0]] = no_Outlier_TS.values
    counter += 1
    row_pointer += curr_field.shape[0]

####################################################################################
###
###                   Write the outputs
###
####################################################################################
output_df.drop_duplicates(inplace=True)
output_df.to_csv(out_name, index = False)

end_time = time.time()
print(end_time - start_time)





