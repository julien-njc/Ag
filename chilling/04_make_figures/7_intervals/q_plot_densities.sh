#!/bin/bash

#PBS -V

#PBS -N plot_densities

#PBS -l nodes=1:dev:ppn=1,walltime=01:00:00
#PBS -l mem=5gb
#PBS -q hydro

#PBS -k o
  ##PBS -j oe
#PBS -e /home/hnoorazar/chilling_codes/current_draft/03_make_figures/7_intervals/error/plot_densities.e
#PBS -o /home/hnoorazar/chilling_codes/current_draft/03_make_figures/7_intervals/error/plot_densities.o

#PBS -m abe
cd /home/hnoorazar/chilling_codes/current_draft/03_make_figures/7_intervals/

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

Rscript --vanilla ./plot_densities.R

echo
echo "----- DONE -----"
echo

exit 0
