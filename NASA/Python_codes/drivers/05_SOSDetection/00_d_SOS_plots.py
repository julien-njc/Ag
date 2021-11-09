####
#### Nov 8, 2021
####


# import matplotlib.backends.backend_pdf
import csv
import numpy as np
import pandas as pd
# from IPython.display import Image
import datetime
from datetime import date
import time
import scipy
import scipy.signal
import os, os.path
import matplotlib

from patsy import cr

# from pprint import pprint
import matplotlib.pyplot as plt
import seaborn as sb

from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

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
eleven_colors = ["gray", "lightcoral", "red", "peru",
                 "darkorange", "gold", "olive", "green",
                 "blue", "violet", "deepskyblue"]

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
####################################################################################
###
###                   Aeolus Directories
###
####################################################################################
raw_dir = "/data/hydro/users/Hossein/NASA/01_raw_GEE/"
data_dir = "/data/hydro/users/Hossein/NASA/05_SG_TS/"
SOS_plot_dir = "/data/hydro/users/Hossein/NASA/06_SOS_plots/"

output_dir = SOS_plot_dir + str(int(onset_cut*10)) + "_EOS" + str(int(offset_cut*10)) + "/"
os.makedirs(output_dir, exist_ok=True)

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
if randCount == "all":
    f_name = "04_SG_int_Grant_Irr_2008_2018_" + indeks + "_" + ".csv"
else:
    f_name = "04_SG_int_Grant_Irr_2008_2018_" + indeks + "_" + str(randCount) + "randomfields.csv"

a_df = pd.read_csv(data_dir + f_name, low_memory=False)
a_df['human_system_start_time'] = pd.to_datetime(a_df['human_system_start_time'])

f_names = ["L5_T1C2L2_Scaled_int_Grant_Irr_2008_2018_2cols_102008-01-01_2012-05-05.csv", 
           "L7_T1C2L2_Scaled_int_Grant_Irr_2008_2018_2cols_10_2008-01-01_2021-09-23.csv",
           "L8_T1C2L2_Scaled_int_Grant_Irr_2008_2018_2cols_10_2008-01-01_2021-10-14.csv"]

L5 = pd.read_csv(data_dir + f_names[0], low_memory=False)
L7 = pd.read_csv(data_dir + f_names[1], low_memory=False)
L8 = pd.read_csv(data_dir + f_names[2], low_memory=False)

if indeks == "NDVI":
    NoVI = "EVI"
else:
    NoVI = "NDVI"

L5.drop([NoVI], axis=1, inplace=True)
L5 = L5[L5[indeks].notna()]

L7.drop([NoVI], axis=1, inplace=True)
L7 = L7[L7[indeks].notna()]

L8.drop([NoVI], axis=1, inplace=True)
L8 = L8[L8[indeks].notna()]

IDs = np.sort(L5[IDcolName].unique())
raw_df = pd.concat([L5, L7, L8])
del(L5, L7, L8)
raw_df['human_system_start_time'] = pd.to_datetime(raw_df['human_system_start_time'])
########################################

a_df = rc.initial_clean(df = a_df, column_to_be_cleaned = indeks)
raw_df = rc.initial_clean(df = raw_df, column_to_be_cleaned = indeks)

### List of unique polygons
polygon_list = a_df['ID'].unique()
print ("_____________________________________")
print("len(polygon_list)")
print (len(polygon_list))
print ("_____________________________________")

counter = 0

for ID in polygon_list:
    if (counter%100 == 0):
        print ("_____________________________________")
        print ("counter: " + str(counter))
        print (ID)

    curr_SG = a_df[a_df['ID'] == ID].copy()
    curr_raw = raw_df[raw_df['ID'] == ID].copy()    
    
    ################################################################
    # Sort by DoY (sanitary check)
    curr_SG.sort_values(by=['human_system_start_time'], inplace=True)
    curr_raw.sort_values(by=['human_system_start_time'], inplace=True)

    curr_SG.reset_index(drop=True, inplace=True)
    curr_raw.reset_index(drop=True, inplace=True)

    ################################################################
    
    fig, axs = plt.subplots(1, 3, figsize=(20,12),
                            sharex='col', sharey='row',
                            gridspec_kw={'hspace': 0.1, 'wspace': .1});

    (ax1, ax2, ax3) = axs;
    ax1.grid(True); ax2.grid(True); ax3.grid(True);

    ncp.SG_clean_SOS(raw_dt = curr_raw,
                     SG_dt = curr_SG,
                     idx = indeks,
                     ax = ax1,
                     onset_cut = onset_cut, 
                     offset_cut = offset_cut);

    ncp.SG_clean_SOS(raw_dt = curr_raw,
                     SG_dt = curr_SG,
                     idx = indeks,
                     ax = ax2,
                     onset_cut = onset_cut, 
                     offset_cut = offset_cut);

    ncp.SG_clean_SOS(raw_dt = curr_raw,
                     SG_dt = curr_SG,
                     idx = indeks,
                     ax = ax3,
                     onset_cut = onset_cut, 
                     offset_cut = offset_cut);

    fig_name = plot_path + given_county + "_" + plant + "_SF_year_" + str(SF_year) + "_" + ID + '.png'

    os.makedirs(plot_path, exist_ok=True)

    plt.savefig(fname = fig_name, dpi=100, bbox_inches='tight')
    plt.close('all')
    counter += 1


print ("done")
end_time = time.time()
print(end_time - start_time)


