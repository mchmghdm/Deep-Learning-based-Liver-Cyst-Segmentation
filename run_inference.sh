#!/bin/bash

dataset = Dataset105_ADPKDCyst
project = 105

cd /home/mina/Projects/nnUNetFrame/dataset/nnUNet_raw/nnUNet_raw_data/"$dataset"/

nnUNetv2_predict -i imagesTr -o pred_nnUnet_train_2d -d "$project" -c 2d -f "0" "1" "2" "3" "4" --save_probabilities

nnUNetv2_predict -i imagesTr -o pred_nnUnet_train_3dfullres -d "$project" -c 3d_fullres -f "0" "1" "2" "3" "4" --save_probabilities

nnUNetv2_ensemble -i pred_nnUnet_train_2d pred_nnUnet_train_3dfullres -o pred_nnUnet_train