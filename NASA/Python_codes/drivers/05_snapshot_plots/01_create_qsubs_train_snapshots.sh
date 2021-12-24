#!/bin/bash
cd /home/hnoorazar/NASA/05_snapshot_plots/

outer=1

for county in AdamBenton2016 FranklinYakima2018 Grant2017 Monterey2014 Walla2015
do
  for TOA_or_corrected in TOA corrected
  do
    cp 02_train_snapshot_template.sh ./qsubs/q_train_$outer.sh
    sed -i s/outer/"$outer"/g    ./qsubs/q_train_$outer.sh
    sed -i s/TOA_or_corrected/"$TOA_or_corrected"/g  ./qsubs/q_train_$outer.sh
    sed -i s/county/"$county"/g  ./qsubs/q_train_$outer.sh
    let "outer+=1" 
  done
done