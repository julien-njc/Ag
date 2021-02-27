#!/bin/bash
#v#!/usr/bin/env Rscript

#PBS -N merge_CMPOP_USA
#PBS -l nodes=1:ppn=1,walltime=70:00:00
#PBS -l mem=20gb
#PBS -q hydro
#PBS -e E_merge_CMPOP_USA.txt
#PBS -o o.txt
#PBS -m abe
cd $PBS_O_WORKDIR

# Ensure a clean running environment:
module purge

# Load modules (if needed)
module load R/R-3.2.2_gcc

./d_merge_USA_hist_CMPOP.R rcp45 CMPOP

exit 0
