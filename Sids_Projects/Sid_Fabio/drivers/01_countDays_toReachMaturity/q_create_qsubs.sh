#!/bin/bash

cd /home/hnoorazar/sid/sidFabio/00_cumGDD_separateLocationsModels



outer=1
for veg_type in tomato
do
  for modelName in observed
  do
    cp q_cumGDD.sh                     ./qsubs/q_cumGDD_$modelName$veg_type.sh
    sed -i s/veg_type/"$veg_type"/g    ./qsubs/q_cumGDD_$modelName$veg_type.sh
    sed -i s/modelName/"$modelName"/g  ./qsubs/q_cumGDD_$modelName$veg_type.sh
    let "outer+=1" 
  done
done


