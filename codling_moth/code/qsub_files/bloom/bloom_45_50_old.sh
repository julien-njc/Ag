#!/bin/bash
#v#!/usr/bin/env Rscript

#PBS -N bloom_45_2015_0.5_old
#PBS -l nodes=1:ppn=1,walltime=99:00:00
#PBS -l mem=30gb
#PBS -q hydro
#PBS -e /home/hnoorazar/cleaner_codes/qsub_files/error/E_bloom_45_2015_0.5.txt
#PBS -o /home/hnoorazar/cleaner_codes/qsub_files/error/O_bloom_45_2015_0.5.txt
#PBS -m abe
cd $PBS_O_WORKDIR

# Ensure a clean running environment:
module purge

# Load modules (if needed)
module load R/R-3.2.2_gcc

/home/hnoorazar/cleaner_codes/drivers/bloom_driver_old.R rcp45 0.5

exit 0
