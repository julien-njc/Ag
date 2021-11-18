#!/bin/bash

cd /home/hnoorazar/NASA/03_regularize_fillGap/qsubs/
for runname in {1..8}
do
qsub ./q_train_JFD$runname.sh
done
