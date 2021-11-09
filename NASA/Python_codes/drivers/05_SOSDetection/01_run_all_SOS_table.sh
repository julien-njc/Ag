#!/bin/bash

cd /home/hnoorazar/NASA/05_SOS_detection/qsubs/
for runname in {1..10}
do
qsub ./q_$runname.sh
done
