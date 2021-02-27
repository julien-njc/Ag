#!/bin/bash
#!/usr/bin/env Rscript

#PBS -N pest_window_400F
#PBS -l nodes=1:ppn=1,walltime=99:00:00
#PBS -l mem=5gb
#PBS -q hydro
#PBS -e E_pest_window_400F.txt
#PBS -o O_pest_window_400F.txt
#PBS -m abe
cd $PBS_O_WORKDIR
# Ensure a clean running environment:
module purge
# Load modules (if needed)
module load R/R-3.2.2_gcc 

./pest_window_400F.R

exit 0
