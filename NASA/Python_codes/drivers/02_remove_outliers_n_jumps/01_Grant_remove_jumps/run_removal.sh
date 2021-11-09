#!/bin/bash

cd /home/hnoorazar/NASA/02_remove_outliers_n_jumps/01_Grant_remove_jumps/qsubs/
for runname in {1..2}
do
qsub ./q_$runname.sh
done
