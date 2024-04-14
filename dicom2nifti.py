import pandas as pd
import numpy as np
from ast import literal_eval
import SimpleITK as sitk
import pydicom

IOP = "IOP"
IPP = "IPP"
IPP_dist = "IPP_dist"
"""
This utilities package provides dicom sorting by slice position.
This code is based on Dr. Akshay Goel and Xinzi He's implementations for adpkd project
GitHub ADPKD-segmentation-pytorch:
    - https://github.com/aksg87/adpkd-segmentation-pytorch
In which the two functions can be found in the file:
    - adpkd_segmentation/inference/inference_utils.py
As you may find in this file, IOP_IPP_dicomsort accepts a pandas DataFrame
with the following attributes:
    - 'IOP': ImageOrientationPatient of each DICOM slice
    - 'IPP': ImagePositionPatient of each DICOM slice
    - 'dcm_paths': the file path to each DICOM slice
The orientation normal vector is computed with crossproduct()
The distance calculated at each slice is then computed by taking the
dot product between the normal vector and ImagePositionPatient.
Finally, the dicom files are sorted by the previously computed slice distance.
We then return this sorted pandas dataframe.
"""


def crossproduct(cosines):
    assert len(cosines) == 6, "check for correct dimension"

    # Initialize patient orientation normal vector
    normal = [0, 0, 0]

    # cross product to find normal vector
    normal[0] = cosines[1] * cosines[5] - cosines[2] * cosines[4]
    normal[1] = cosines[2] * cosines[3] - cosines[0] * cosines[5]
    normal[2] = cosines[0] * cosines[4] - cosines[1] * cosines[3]

    return normal


def IOP_IPP_dicomsort(dicom_dataframe: pd.DataFrame) -> pd.DataFrame:


    dicom_dataframe[IPP_dist] = ""

    try:
        cosines = [round(x) for x in dicom_dataframe[IOP].iloc[0]]
        normal = crossproduct(cosines)

        for i in dicom_dataframe.index:
            positions = [
                x for x in literal_eval(str(dicom_dataframe.at[i, IPP]))
            ]
            dicom_dataframe.at[i, IPP_dist] = sum(
                n * p for (n, p) in zip(normal, positions)
            )

    except ValueError as e:
        print("sorting error with:", dicom_dataframe[IOP].iloc[0])
        print(e)

    distances = list(dicom_dataframe[IPP_dist])

    sorted_indices = np.argsort(distances)
    slice_map = {
        distances[idx]: pos
        for idx, pos in zip(sorted_indices, range(len(distances)))
    }
    dist_slice_pos = dicom_dataframe[IPP_dist].map(slice_map)

    # add correct slice position
    for i in dicom_dataframe.index:
        dicom_dataframe.at[i, "slice_pos"] = dist_slice_pos.get(i)

    dicom_dataframe.sort_values("slice_pos", inplace=True)
    return dicom_dataframe


def dicom2nifty(dicom_folder_path, nifty_path):
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(dicom_folder_path)
    # reader.SetFileNames(dicom_names)

    dcms = [pydicom.read_file(p) for p in dicom_names]
    IOPs = [d.ImageOrientationPatient for d in dcms]
    IPPs = [d.ImagePositionPatient for d in dcms]

    dicom_data = {"dcm_paths": dicom_names, IOP: IOPs, IPP: IPPs}
    sorted_dataframe = IOP_IPP_dicomsort(pd.DataFrame(dicom_data))
    sorted_dicom_names = [str(p) for p in sorted_dataframe["dcm_paths"]]

    reader.SetFileNames(sorted_dicom_names)
    image = reader.Execute()
    # Saving Data
    sitk.WriteImage(image, str(nifty_path))

def dicom_file_names_read(dicom_folder_path):
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(dicom_folder_path)
    # reader.SetFileNames(dicom_names)

    dcms = [pydicom.read_file(p) for p in dicom_names]
    IOPs = [d.ImageOrientationPatient for d in dcms]
    IPPs = [d.ImagePositionPatient for d in dcms]

    dicom_data = {"dcm_paths": dicom_names, IOP: IOPs, IPP: IPPs}
    sorted_dataframe = IOP_IPP_dicomsort(pd.DataFrame(dicom_data))
    sorted_dicom_names = [str(p) for p in sorted_dataframe["dcm_paths"]]

    return sorted_dicom_names

if __name__ == "__main__":
    dicom_folder_path = ".../DICOM/files/"
    nifty_path = ".../cyst_training/DICOM_FileName/"
    dicom2nifty(dicom_folder_path, nifty_path)


