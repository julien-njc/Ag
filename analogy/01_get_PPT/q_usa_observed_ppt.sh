#!/bin/bash

#PBS -V
#PBS -N get_USA_obs_PPT

#PBS -l nodes=1:dev:ppn=1, mem=4gb
#PBS -l walltime=05:00:00
#PBS -q hydro

## Define path for output & error logs
#PBS -k o
  ##PBS -j oe
#PBS -e /home/hnoorazar/analog_codes/get_ppt/error/USA_obs_E
#PBS -o /home/hnoorazar/analog_codes/get_ppt/error/USA_obs_O

## Define path for reporting
#PBS -m abe

echo
echo We are in the $PWD directory
echo

cd /data/hydro/jennylabcommon2/metdata/historical/UI_historical/VIC_Binary_CONUS_to_2016

echo
echo We are now in $PWD.
echo

# First we ensure a clean running environment:
module purge

# Load R
module load udunits/2.2.20
module load libxml2/2.9.4
module load gdal/2.1.2_gcc proj/4.9.2
module load gcc/7.3.0 r/3.5.1/gcc/7.3.0

Rscript --vanilla /home/hnoorazar/analog_codes/get_ppt/d_get_usa_observed_ppt.R

echo
echo "----- DONE -----"
echo

exit 0
