#!/bin/bash

for fold in 0 1 2 3 4; do
  nnUNetv2_train 211 3d_fullres $fold > training_log_LIVER_$fold.txt 2>&1 
done
  
  