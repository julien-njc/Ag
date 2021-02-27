#!/bin/bash

#PBS -V
#PBS -N merge_usa

#PBS -l nodes=1:ppn=1, mem=10gb
#PBS -l walltime=10:00:00
#PBS -q hydro

#PBS -k o
  ##PBS -j oe
#PBS -e /home/hnoorazar/analog_codes/01_get_ppt/error/merge_usa.e
#PBS -o /home/hnoorazar/analog_codes/01_get_ppt/error/merge_usa.o

## Define path for reporting
#PBS -m abe

echo
echo We are in the $PWD directory
echo

# First we ensure a clean running environment:
module purge

# Load R
module load udunits/2.2.20
module load libxml2/2.9.4
module load gdal/2.1.2_gcc proj/4.9.2
module load gcc/7.3.0 r/3.5.1/gcc/7.3.0

Rscript --vanilla /home/hnoorazar/analog_codes/01_get_ppt/d_merge_driver.R usa

echo
echo "----- DONE -----"
echo

exit 0
