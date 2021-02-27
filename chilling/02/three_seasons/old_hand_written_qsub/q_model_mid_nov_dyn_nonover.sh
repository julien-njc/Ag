#!/bin/bash

#PBS -V
#PBS -N mod_dyn_mid_nov_nonover

#PBS -l nodes=1:ppn=1,walltime=99:00:00
#PBS -l mem=10gb
#PBS -q hydro
#PBS -t 1-72

#PBS -k o
  ##PBS -j oe
#PBS -e /home/hnoorazar/chilling_codes/current_draft/02/three_seasons/error/m_mid_nov_non.e
#PBS -o /home/hnoorazar/chilling_codes/current_draft/02/three_seasons/error/m_mid_nov_non.o

## Define path for reporting
#PBS -m abe

echo
echo We should be in mid_nov and we are in the $PWD directory
echo

cd $PBS_O_WORKDIR

echo
echo We are now in $PWD.
echo

dir_list=()
while IFS= read -d $'\0' -r file ; do
dir_list=("${dir_list[@]}" "$file")
done < <(find /data/hydro/users/Hossein/chill/data_by_core/dynamic/01/mid_nov/modeled/ -mindepth 2 -maxdepth 2 -type d -print0)

echo
echo "${dir_list[@]}"
echo

# First we ensure a clean running environment:
module purge

# Load R
module load udunits/2.2.20
module load libxml2/2.9.4
module load gdal/2.1.2_gcc proj/4.9.2
module load gcc/7.3.0 r/3.5.1/gcc/7.3.0

# new job for each directory index, up to max arrayid
cd ${dir_list[((${PBS_ARRAYID} - 1))]}

Rscript --vanilla /home/hnoorazar/chilling_codes/current_draft/02/three_seasons/d_modeled.R "dynamic" "non_overlap" "mid_nov"

echo
echo "----- DONE -----"
echo

exit 0
