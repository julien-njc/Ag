#!/bin/bash
cd /home/hnoorazar/NASA/05_SOS_detection/qsubs/

outer=1

for indeks in EVI NDVI
do
  for randCount in 100 500 all
  do
    for SEOS_cut in 3 35 4 5
    do
      cp template.sh ./qsubs/q_$outer.sh
      sed -i s/outer/"$outer"/g          ./qsubs/q_$outer.sh
      sed -i s/indeks/"$indeks"/g        ./qsubs/q_$outer.sh
      sed -i s/randCount/"$randCount"/g  ./qsubs/q_$outer.sh
      sed -i s/SEOS_cut/"$SEOS_cut"/g    ./qsubs/q_$outer.sh
      let "outer+=1" 
    done
  done
done