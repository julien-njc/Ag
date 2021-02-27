#!/bin/bash

#PBS -V
#PBS -N collect_the_rain
#PBS -l mem=10gb

#PBS -l nodes=1:ppn=1,walltime=2:00:00
#PBS -q fast

#PBS -k o
#PBS -e /home/hnoorazar/lagoon_codes/01_rain_snow/02_cum_rain/error/doomsday_E
#PBS -o /home/hnoorazar/lagoon_codes/01_rain_snow/02_cum_rain/error/doomsday_O
#PBS -m abe

echo
echo We are in $PWD.
echo

module purge
module load udunits/2.2.20
module load libxml2/2.9.4
module load gdal/2.1.2_gcc proj/4.9.2
module load gcc/7.3.0 r/3.5.1/gcc/7.3.0
module load gcc/7.3.0
module load r/3.5.1/gcc/7.3.0
module load r/3.5.1

cd /home/hnoorazar/lagoon_codes/01_rain_snow/02_cum_rain
Rscript --vanilla ./d_merge_last_days.R

echo
echo "----- DONE -----"
echo

exit 0
