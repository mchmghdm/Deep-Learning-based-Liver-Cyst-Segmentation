import os
import shutil
from pathlib import Path

import pdb  

from nnunetv2.dataset_conversion.generate_dataset_json import generate_dataset_json
from nnunetv2.paths import nnUNet_raw


def make_out_dirs(dataset_id: int, task_name="ADPKDCystLiver"):
    pdb.set_trace()
    dataset_name = f"Dataset{dataset_id:03d}_{task_name}"
    
 
    #out_dir = Path(nnUNet_raw.replace('"', "")) / dataset_name # here we have a problem 
    nnUNet_raw_path = Path('/home/mina/Projects/nnUNetFrame/dataset/nnUNet_raw/nnUNet_raw_data')
    out_dir = nnUNet_raw_path / dataset_name
    
    out_train_dir = out_dir / "imagesTr"
    out_labels_dir = out_dir / "labelsTr"
    out_test_dir = out_dir / "imagesTs"
    out_test_label_dir = out_dir / "test_gt"
    out_train_pred_dir = out_dir / "pred_nnUnet_train"
    out_test_pred_dir = out_dir / "pred_nnUnet_test"
    
    
    os.makedirs(out_dir, exist_ok=True)
    os.makedirs(out_train_dir, exist_ok=True)
    os.makedirs(out_labels_dir, exist_ok=True)
    os.makedirs(out_test_dir, exist_ok=True)
    os.makedirs(out_test_label_dir, exist_ok=True)
    os.makedirs(out_train_pred_dir, exist_ok=True)
    os.makedirs(out_test_pred_dir, exist_ok=True)
    
    return out_dir, out_train_dir, out_labels_dir, out_test_dir, out_test_label_dir


def copy_files(src_data_folder: Path, train_dir: Path, labels_dir: Path, test_dir: Path, test_label_dir: Path):
    """Copy files from the PKD_Cyst (PKDC) dataset to the nnUNet dataset folder. Returns the number of training cases."""
    # src_data_folder to be /home/mina/cyst_train/001/
    pdb.set_trace()
    patients_train = sorted([f for f in (src_data_folder / "training").iterdir() if f.is_dir()])
    patients_test = sorted([f for f in (src_data_folder / "testing").iterdir() if f.is_dir()])
  
    pdb.set_trace()
    num_training_cases = 0
    # Copy training files and corresponding labels.
    for patient_dir in patients_train:
        for file in patient_dir.iterdir():
            if file.suffix == ".gz" and "_gt" not in file.name: #and "_4d" not in file.name
                # The stem is 'patient.nii', and the suffix is '.gz'.
                # We split the stem and append _0000 to the patient part.
                shutil.copy(file, train_dir / f"{file.stem.split('.')[0]}_0000.nii.gz")
                num_training_cases += 1
            elif file.suffix == ".gz" and "liver_cyst_gt" in file.name:
                shutil.copy(file, labels_dir / file.name.replace("_liver_cyst_gt", ""))

    # Copy test files.
    for patient_dir in patients_test:
        for file in patient_dir.iterdir():
            if file.suffix == ".gz" and "_gt" not in file.name: # and "_4d" not in file.name
                shutil.copy(file, test_dir / f"{file.stem.split('.')[0]}_0000.nii.gz")
            elif file.suffix == ".gz" and "liver_cyst_gt" in file.name: # added
                shutil.copy(file, test_label_dir / file.name.replace("_liver_cyst_gt", ""))

    return num_training_cases

def convert_acdc(src_data_folder: str, dataset_id):
    pdb.set_trace()
    out_dir, train_dir, labels_dir, test_dir , test_label_dir = make_out_dirs(dataset_id=dataset_id)
  
    pdb.set_trace()
    
    num_training_cases = copy_files(Path(src_data_folder), train_dir, labels_dir, test_dir , test_label_dir)
    
    pdb.set_trace()

    generate_dataset_json(
        str(out_dir),
        channel_names={
            0: "MRI",
            # 1: "Organ_seg" # for later
        },
        
        labels={
            "background": 0,
            "liver_cyst": 1 		

        },
        file_ending=".nii.gz",
        num_training_cases=num_training_cases,
    )



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_folder",
        type=str,
        help="The downloaded ACDC dataset dir. Should contain extracted 'training' and 'testing' folders.",
    )
    parser.add_argument(
        "-d", "--dataset_id", required=False, type=int, default=27, help="nnU-Net Dataset ID, default: 27"
    )
    args = parser.parse_args()

    print(args.input_folder)
    print(args.dataset_id)

    print("Converting...")

    convert_acdc(args.input_folder, args.dataset_id)
    print(args.dataset_id)
    print("Done!")