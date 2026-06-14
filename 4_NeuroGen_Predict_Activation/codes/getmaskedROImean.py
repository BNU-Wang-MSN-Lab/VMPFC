import sys
import os
import struct
import time as time
import numpy as np
import h5py
from scipy.stats import pearsonr
from itertools import chain
from scipy.io import loadmat
import pickle
import math
import matplotlib.pyplot as plt
import csv
from itertools import zip_longest
from src.file_utility import load_mask_from_nii, view_data
from src.load_nsd import load_betas
import argparse

parser = argparse.ArgumentParser(prog='get ROI mean for each subject', 
	description='input subject ID, output txt files',
	usage='python getmaskedROImean.py --subj i')

parser.add_argument('--subj', default = '1', type=int)
args = parser.parse_args()

beta_root = "/home/mingxue/NSD/nsddata_betas/ppdata/"  #NSD data dir
mask_root = "/home/mingxue/NSD//nsddata/ppdata/"   

roimask_dir = '/home/mingxue/NSD/MNI2FUNC_NSD/MNI2FUNC/' #ROI mask dir
roibeta_dir = '/home/mingxue/NSD/MNI2FUNC_NSD/MNI2FUNC/'  #ROImean output dir

subject = args.subj
ROIs = ['social','value','emotion']


tight_mask_full = load_mask_from_nii(mask_root + "subj%02d/func1pt8mm/brainmask.nii.gz"%subject)
brain_mask_full = tight_mask_full.flatten().astype(bool)
voxel_idx_brain = np.arange(len(brain_mask_full))[brain_mask_full]

voxel_mask = brain_mask_full 
voxel_idx = voxel_idx_brain 

beta_subj = beta_root + "subj%02d/func1pt8mm/betas_fithrf_GLMdenoise_RR/" % (subject,)  
voxel_data, filenames = load_betas(folder_name=beta_subj, zscore=True, voxel_mask=voxel_mask, up_to=-1, load_ext='.nii.gz')
print ("voxel data shape is: ", voxel_data.shape) 

# load ROI masks
for roi in ROIs:
	roimask = load_mask_from_nii(roimask_dir + 'subj%02d/'%(subject) + 'subregions_neurosynth/' + roi + '.nii')

	roimask_flatten = roimask.flatten()[brain_mask_full]
	print('roimask_flatten is :',roimask_flatten.shape)

	# apply ROI mask to shared voxel data
	masked_voxel_data = roimask_flatten * voxel_data
	print(voxel_data.shape)
	print(masked_voxel_data.shape)

	# calculate the average of the activations in the ROI
	voxel_num = np.where(roimask_flatten != 0)[0].shape[0]
	mean_activation = np.sum(masked_voxel_data, axis=1)/voxel_num
	print(mean_activation.shape)

	beta_dir = roibeta_dir + 'subj%02d/'%(subject) + 'subregions_neurosynth/' + 'roiavgbeta/' 
	if not os.path.exists(beta_dir):
		os.makedirs(beta_dir)

	np.savetxt(beta_dir+ f"meanbeta_{roi}.txt", mean_activation)
	del masked_voxel_data
	print("ROI " + roi + " is finished!")

