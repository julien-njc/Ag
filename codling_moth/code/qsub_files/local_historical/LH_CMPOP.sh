#!/bin/bash
#v#!/usr/bin/env Rscript
# job name

#PBS -N LH_CMPOP
#PBS -l nodes=1:ppn=1,walltime=70:00:00
#PBS -l mem=10gb
#PBS -q hydro
#PBS -e LH_CMPOP_e.txt
#PBS -o LH_CMPOP_o.txt
#PBS -m abe
cd $PBS_O_WORKDIR

# First we ensure a clean running environment:
module purge

# Load modules (if needed)
module load R/R-3.2.2_gcc


/home/hnoorazar/cleaner_codes/drivers/local_historical/LH_CMPOP.R historical

exit 0
