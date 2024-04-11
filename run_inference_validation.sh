
project=201
dataset=Dataset201_ADPKDCystLiver
cd /home/mina/Projects/nnUNetFrame/dataset/nnUNet_raw/nnUNet_raw_data/"$dataset"/

mkdir pred_nnUnet_valid_2d pred_nnUnet_valid_3dfullres pred_nnUnet_valid

cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__2d/fold_0/validation/* pred_nnUnet_valid_2d
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__2d/fold_1/validation/* pred_nnUnet_valid_2d
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__2d/fold_2/validation/* pred_nnUnet_valid_2d
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__2d/fold_3/validation/* pred_nnUnet_valid_2d
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__2d/fold_4/validation/* pred_nnUnet_valid_2d

rm pred_nnUnet_valid_2d/summary.json

cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_0/validation/* pred_nnUnet_valid_3dfullres
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_1/validation/* pred_nnUnet_valid_3dfullres
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_2/validation/* pred_nnUnet_valid_3dfullres
cp -r /home/mina/Projects/nnUNetFrame/dataset/nnUNet_results/"$dataset"/nnUNetTrainer__nnUNetPlans__3d_fullres/fold_3/validation/* pred_nnUnet_valid_3dfullres

rm pred_nnUnet_valid_2d/summary.json
Dataset201_ADPKDCystLiver cp pred_nnUnet_train_2d/dataset.json pred_nnUnet_valid_2d
Dataset201_ADPKDCystLiver cp pred_nnUnet_train_2d/plan.json pred_nnUnet_valid_2d

rm pred_nnUnet_valid_3dfullres/summary.json
Dataset201_ADPKDCystLiver cp pred_nnUnet_train_3dfullres/dataset.json pred_nnUnet_valid_3dfullres


nnUNetv2_ensemble -i pred_nnUnet_valid_3dfullres pred_nnUnet_valid_2d -o pred_nnUnet_valid
