####
#### Nov. 19, 2021
####
import csv
import numpy as np
import pandas as pd
import datetime
import time
import os, os.path
# from patsy import cr

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

####################################################################################
###
###                   Aeolus Directories
###
####################################################################################
SF_data_dir = "/data/hydro/users/Hossein/NASA/000_shapefile_data_part/"
data_dir = "/data/hydro/users/Hossein/NASA/06_SOS_tables/"

output_dir = "/data/hydro/users/Hossein/NASA/07_2crop_acr/"
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
acr_df_cols = ["ID"]
acr_df = pd.DataFrame(data = None)


for county in ["AdamBenton2016", "FranklinYakima2018", "Grant2017", "Monterey2014", "Walla2015"]:
    for thresh in [3, 4, 5]:
        SF_data = pd.read_csv(SF_data_dir + county + ".csv")
        SF_data["ID"] = SF_data["ID"].astype(str)

        #
        # Fucking California has different column names. Replace the names
        #
        if county == "Monterey2014":
            SF_data.rename(columns={'Crop2014': 'CropTyp', 'Acres':'ExctAcr'}, inplace=True)
            SF_data['county'] = "Monterey"

        SF_data = SF_data[["ID", "CropTyp", "ExctAcr", "county"]]

        SC_df = pd.read_csv(data_dir + "SC_train_" + county + "_" + indeks + str(thresh) + "_JFD.csv")
        SC_df['human_system_start_time'] = pd.to_datetime(SC_df['human_system_start_time'])
        SC_df["ID"] = SC_df["ID"].astype(str) # Monterays ID will be read as integer, convert to string

        ##
        ## subset the only proper year.
        ##
        print("No rows before filtering correct year {}.".format(len(SC_df)))

        SC_df = SC_df[SC_df.human_system_start_time.dt.year == int(county[-4:])]
        print("No rows after filtering correct year {}.".format(len(SC_df)))

        SC_df['threshold'] = thresh/10
        SC_df['year'] = SC_df.human_system_start_time.dt.year

        SC_df = SC_df[["ID", "season_count", "year", "threshold"]]
        
        """
           Some fields are double-cropped. So, they are present twice in the table!
           Drop duplicates so we count them once.
        """
        SC_df.drop_duplicates(inplace=True)

        SC_df = pd.merge(SC_df, SF_data, on=['ID'], how='left')
        #
        # Fields with more than or equal 2 growing cycles are 2, less than 2 is single-cropped
        #
        SC_df['season_count'] = np.where(SC_df['season_count']>=2, 2, 1)

        acr_df = pd.concat([acr_df, SC_df])

acr_df = acr_df.groupby(['county', 'CropTyp', 'year', 'season_count', 'threshold']).sum()
acr_df.reset_index(inplace=True)
acr_df.sort_values(by=['threshold', 'county', 'CropTyp', 'year', 'season_count'], inplace=True)
acr_df.dropna(inplace=True)
out_name = output_dir + "doubleAcr_perCounty_perCrop_" + indeks + "_JFD.csv"
acr_df.to_csv(out_name, index = False)



acr_df = acr_df.groupby(['county', 'year', 'season_count', 'threshold']).sum()
acr_df.reset_index(inplace=True)
acr_df.sort_values(by=['threshold', 'county', 'year', 'season_count'], inplace=True)
acr_df.dropna(inplace=True)

out_name = output_dir + "doubleAcr_perCounty_" + indeks + "_JFD.csv"
acr_df.to_csv(out_name, index = False)



print ("done")
end_time = time.time()
print ("it took {:.0f} minutes to run this code.".format((end_time - start_time)/60))



