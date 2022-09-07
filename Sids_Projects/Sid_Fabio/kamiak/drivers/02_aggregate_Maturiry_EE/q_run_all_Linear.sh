#!/bin/bash

cd /home/h.noorazar/Sid/sidFabio/02_aggregate_Maturiry_EE/qsubs

for runname in {1..180}
do
sbatch ./q_countDaysMaturity$runname.sh
done
