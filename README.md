# Deep Learning-based Liver Cyst Segmentation in ADPKD Patients

This repository contains the code for liver cyst segmentation in ADPKD (Autosomal Dominant Polycystic Kidney Disease) patients using a neural network-based UNet architecture. The model is designed to provide swift and precise segmentation of liver cysts from MRI images.

## Tutorial

This work is based on the nnUNet framework, a self-configuring medical image segmentation network. For more information about the nnUNet architecture and how to train a model, refer to the following resources:

- [nnUNet Paper](https://www.nature.com/articles/s41592-020-01008-z)
- [nnUNet GitHub Page](https://github.com/MIC-DKFZ/nnUNet)

## Installation

To install nnUNet and start working with it, you can use pip:
```bash
pip install nnunetv2
```

To clone the nnUNet repository and set it up for modification, use the following commands:

git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e.


For more detailed installation instructions, refer to the [installation instructions](https://github.com/MIC-DKFZ/nnUNet/blob/master/documentation/installation_instructions.md) provided in the nnUNet documentation:


# Pre-processing
Before training the model, you will need to preprocess the data:

- Convert DICOM files to NIfTI format using /main/dicom2nifti.py.
- Preprocess the data using /main/data_conversion_liver_file.py to convert the training/validation and test sets to the format required by the nnUNet framework.

# Training
To train the model using both 2D and 3D methods, execute the /home/run_training.sh script.

## Inference
To perform inference on the test set using the trained model, run /home/run_inference.py.
For a sanity check, run /home/run_inference_validation.sh to see the model outcomes on the validation set.

## Evaluation
To evaluate the model's performance, use the following scripts:

- /home/evaluate_predictions.py to evaluate the model outcome.
- /home/evaluate_biomarkers.py to extract biomarkers from the model output and ground truth.
- /home/evaluate_observers.py to assess inter-observer, intra-observer, and reliability of manual labeling.

