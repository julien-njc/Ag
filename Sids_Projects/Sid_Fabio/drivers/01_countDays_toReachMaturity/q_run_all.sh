#!/bin/bash

cd /home/hnoorazar/sid/sidFabio/00_cumGDD_separateLocationsModels/qsubs

for runname in 1 15 30 45 60 75 90 105 120 135 150 165 180 195 210 225 240 
do
qsub ./q_model_dyn_$runname.sh
qsub ./q_obs_dyn_$runname.sh
done
