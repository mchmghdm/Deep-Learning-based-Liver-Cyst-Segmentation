# Deep Learning-based Liver Cyst Segmentation in ADPKD Patients 
Employing an nn-UNet-based deep learning framework for swift and precise liver cyst segmentation on MRI in PLD patients. 

# Tutorial
This work is based on self-configuring medical image segmentation network, nnU-Net []. please refer to the following refrences to know more about nnUNet architecture and how to train a model. 

- The nnUNet paper: https://www.nature.com/articles/s41592-020-01008-z
- The nnUNet GitHub page: https://github.com/MIC-DKFZ/nnUNet

# Installation

# Pre-processing
To start, you will need to convert the DICOM files to nifti format using: /main/dicom2nifti.py
Then the data need to be preprocessed using /main/data_conversion_liver_file.py to convert the training/validation and test sets to the format required in nnUNet framework.

# Training
To train and unsamble of 2D and 3D methods, run this file: /home/run_training.sh

# Inference
To run model inference on the test set run: /home/run_inference.py
To see the model outcome on the validation set for a sanity check: run /home/run_inference_validation.sh


# Evaluation
To evaluate the model outcome run: /home/evaluate_predictions.py. Same file can use to compare any two predictions from example the model outcomes for the patiensts in the test-retest datasets. 

To extract biomarkers from the model output and also the ground-truth run: /home/evaluate_bimarkers.py

To run the inter-observer, intra-observer and the reliabilty of manuall labeling, run: /home/evaluate_observers.py



