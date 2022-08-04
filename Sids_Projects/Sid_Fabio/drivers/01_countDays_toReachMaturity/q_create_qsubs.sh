#!/bin/bash

cd /home/hnoorazar/sid/sidFabio/01_countDays_toReachMaturity

outer=1
for veg_type in tomato
do
  for model_type in observed
  do
      for start_doy in 1 15 30 45 60 75 90 105 120 135 150 165 180 195 210 225 240 255 270 285 300 315 330 345 360
      do
        cp q_countDatsMaturity.sh            ./qsubs/q_countDatsMaturity$outer.sh
        sed -i s/outer/"$outer"/g            ./qsubs/q_countDatsMaturity$outer.sh
        sed -i s/veg_type/"$veg_type"/g      ./qsubs/q_countDatsMaturity$outer.sh
        sed -i s/model_type/"$model_type"/g  ./qsubs/q_countDatsMaturity$outer.sh
        sed -i s/start_doy/"$start_doy"/g    ./qsubs/q_countDatsMaturity$outer.sh
        let "outer+=1" 
      done
  done
done


