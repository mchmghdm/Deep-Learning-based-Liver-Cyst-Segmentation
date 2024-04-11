import multiprocessing
import os
from copy import deepcopy
from multiprocessing import Pool
from typing import Tuple, List, Union, Optional

import pdb

import numpy as np
import cc3d
from batchgenerators.utilities.file_and_folder_operations import subfiles, join, save_json, load_json, \
    isfile
from nnunetv2.configuration import default_num_processes
from nnunetv2.imageio.base_reader_writer import BaseReaderWriter
from nnunetv2.imageio.reader_writer_registry import determine_reader_writer_from_dataset_json, \
    determine_reader_writer_from_file_ending
from nnunetv2.imageio.simpleitk_reader_writer import SimpleITKIO
# the Evaluator class of the previous nnU-Net was great and all but man was it overengineered. Keep it simple
from nnunetv2.utilities.json_export import recursive_fix_for_json_export
from nnunetv2.utilities.plans_handling.plans_handler import PlansManager

import nibabel as nib


def compute_biomarkers_on_folder(folder: str , mode , label) -> dict:
    """
    output_file must end with .json; can be None
    """
    pdb.set_trace()
    
    if mode=='cyst':
      files = subfiles(folder, suffix=file_ending, join=False)
  
      files_paths = [join(folder, i) for i in files]
     
      result_dict= dict()
    
      for i , subject in enumerate(list(zip(files))):
          key = subject[0]
          
          print('here')
          print(key)
          
          #result_dict[key] = count_num_of_cysts(files_paths[i])
          #result_dict[key]['cyst_volume'] = total_volume_cyst(files_paths[i])
    
          if key not in result_dict:
            result_dict[key] = {}
          
          result_dict[key]['cyst_count'] = count_num_of_cysts(files_paths[i] , label)
          result_dict[key]['cyst_volume'] = total_volume_cyst(files_paths[i] , label)
          
    elif mode == 'liver':
      
      files = subfiles(folder, suffix=file_ending, join=False)
  
      files_paths = [join(folder, i) for i in files]
     
      result_dict= dict()
      
      for i , subject in enumerate(list(zip(files))):
          key = subject[0]
          
          print('here')
          print(key)
          
          
          if key not in result_dict:
            result_dict[key] = {}
            
          result_dict[key]['liver_volume'] = total_volume_liver(files_paths[i] , label)
          
    #elif mode == 'both':
      #for i , subject in enumerate(list(zip(cyst_folder,liver_folder))):
       #   key = subject[0]
        #  result_dict[key]['liver_volume'] = total_volume_cyst(files_paths[i])
         # result_dict[key]['cyst_count'] = count_num_of_cysts(files_paths[i])
          #result_dict[key]['cyst_volume'] = total_volume_cyst(files_paths[i])
          #result_dict[key]['cyst_fraction'] = cyst_fraction(files_paths[i])
          
    print (result_dict)
        
    return result_dict

    

def count_num_of_cysts(cyst_mask , label):
    
    # Load your binary 3D image (assuming it's already thresholded)

    pdb.set_trace()
    
    nifti_image = nib.load(cyst_mask)
    nifti_data = nifti_image.get_fdata()
    
    #nifti_data[nifti_data==1]=0
    #nifti_data[nifti_data==2]=0
    #nifti_data[nifti_data==3]=0
    #nifti_data[nifti_data==label]=1

    
    
    # Perform connected component labeling
       
    nifti_data = nifti_data.astype(np.uint8)
  
    connectivity = 18 # only 4,8 (2D) and 26, 18, and 6 (3D) are allowed
    labels_out , cyst_count  = cc3d.connected_components(nifti_data, connectivity=connectivity , return_N=True)
    
  
    print(cyst_count)
    
    return(cyst_count)

def total_volume_cyst (cyst_mask , label):
    
    # Load your binary 3D image (assuming it's already thresholded)

    
    # Perform connected component labeling
    pdb.set_trace()
    
    
    nifti_image = nib.load(cyst_mask)
    nifti_data = nifti_image.get_fdata()
    
    #nifti_data[nifti_data==1]=0
    #nifti_data[nifti_data==8]=0
    #nifti_data[nifti_data==25]=0
    #nifti_data[nifti_data==label]=1

    print(f'Cyst label is {np.unique(nifti_data)}')
    
    cyst_vol = np.sum(nifti_data)
  
    print(cyst_vol)
    
    return(cyst_vol)

def total_volume_liver (liver_mask , label):
    
    # Load your binary 3D image (assuming it's already thresholded)

    
    # Perform connected component labeling
    pdb.set_trace()
    
    nifti_image = nib.load(liver_mask)
    nifti_data = nifti_image.get_fdata()
    
    print(f'Liver label is {np.unique(nifti_data)}')
    
    nifti_data[nifti_data==1.0]=0
    nifti_data[nifti_data==2.0]=0
    nifti_data[nifti_data==3.0]=0
    nifti_data[nifti_data==label]=1
    nifti_data[nifti_data==5.0]=0
    nifti_data[nifti_data==6.0]=0
    nifti_data[nifti_data==7.0]=0
    nifti_data[nifti_data==8.0]=0
    nifti_data[nifti_data==9.0]=0
    nifti_data[nifti_data==10.0]=0
    nifti_data[nifti_data==11.0]=0
    nifti_data[nifti_data==12.0]=0
    nifti_data[nifti_data==13.0]=0
    nifti_data[nifti_data==15.0]=0
    nifti_data[nifti_data==17.0]=0
    
    print(f'Liver label is {np.unique(nifti_data)}')
     
    liver_vol = np.sum(nifti_data)
  
    print(liver_vol)
    
    return(liver_vol)
    
def cyst_fraction(liver_mask , cyst_mask):
    
    liver_volume = total_volume_liver (liver_mask, label)

    cyst_volume = total_volume_cyst (cyst_mask , label)
    
    return ((cyst_volume/liver_volume)*100)
    


if __name__ == '__main__':
    
    #folder_MR = ''
    
    folder_cyst_mask =  '/home/mina/PLD_all_patients/reproducibility/Scan2_Cyst/'


    #folder_liver_mask = '/home/mina/PLD_all_patients/reproducibility/Scan2_Organ/'

    folder = folder_cyst_mask
    mode = 'cyst' 
    
    label = 1.0 # for external test set liver mask cysts are 26
    
    file_ending = '.nii.gz'
 
    compute_biomarkers_on_folder(folder , mode , label) 
    
    