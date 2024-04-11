#!/bin/bash

for fold in 0 1 2 3 4; do
  nnUNetv2_train 105 2d $fold > training_log_$fold.txt 2>&1 
done

for fold in 0 1 2 3 4; do
  nnUNetv2_train 105 3d_fullres $fold > training_log_$fold.txt 2>&1 
done
  
  