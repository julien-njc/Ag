#!/bin/bash

cd /home/hnoorazar/sid/sidFabio/01_countDays_toReachMaturity/qsubs

for runname in {1..180}
do
qsub ./q_countDatsMaturity$runname.sh
done
