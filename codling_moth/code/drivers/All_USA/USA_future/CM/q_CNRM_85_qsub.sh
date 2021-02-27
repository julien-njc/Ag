#!/bin/bash
#v#!/usr/bin/env Rscript

#PBS -N CNRM-85
#PBS -l nodes=1:ppn=6,walltime=99:00:00
#PBS -l mem=10gb
#PBS -q hydro
#PBS -e E_CNRM-CM5_85.txt
#PBS -o O.txt
#PBS -M h.noorazar@yahoo.com
#PBS -m abe
cd $PBS_O_WORKDIR

# Ensure a clean running environment:
module purge

# Load modules (if needed)
module load R/R-3.2.2_gcc

./A_all_us_future_85.R CNRM-CM5

exit 0
