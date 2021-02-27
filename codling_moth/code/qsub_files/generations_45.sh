#!/bin/bash
#v#!/usr/bin/env Rscript

#PBS -N gen_45
#PBS -l nodes=1:ppn=1,walltime=99:00:00
#PBS -l mem=10gb
#PBS -q hydro
#PBS -e /home/hnoorazar/cleaner_codes/qsub_files/error/E_gen_45.txt
#PBS -o /home/hnoorazar/cleaner_codes/qsub_files/error/gen_45.txt
#PBS -m abe
cd $PBS_O_WORKDIR

# Ensure a clean running environment:
module purge

# Load modules (if needed)
module load R/R-3.2.2_gcc

/home/hnoorazar/cleaner_codes/drivers/d_generations.R rcp45

exit 0
