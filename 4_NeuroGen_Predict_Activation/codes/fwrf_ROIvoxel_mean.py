import sys
import os
import numpy as np
import h5py
from scipy.io import loadmat
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns
fpX = np.float32
import src.numpy_utility as pnu
from src.plots import display_candidate_loss
from src.file_utility import save_stuff, flatten_dict, embed_dict
from src.torch_fwrf import get_value
import torch
import torchvision
import torchvision.transforms as transforms
import torch.optim as optim
import time
import torch.nn.functional as F
import torch.nn as nn
from torchvision import models
from torch.utils.data import DataLoader,Dataset
import argparse

parser = argparse.ArgumentParser(prog='encoding model', 
	description='input subject ID and gpu, output saved parameters',
	usage='python fwrf_ROIvoxel_mean.py --subj i --gpu j')

parser.add_argument('--subj', default = '1', type=int)
parser.add_argument('--gpu', default = '0', type=int)
parser.add_argument('--gpu_devices', default = "0", type = str, help = 'Device IDs')
args = parser.parse_args()


os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_devices

nsd_root = "../data_neurosynth/"
stim_root = nsd_root + "stimuli/"
meanROIbeta_root = nsd_root
exp_design_file = nsd_root + "experiments/nsd_expdesign.mat"

print ('#device:', torch.cuda.device_count())
print ('device#:', torch.cuda.current_device())
print ('device name:', torch.cuda.get_device_name(torch.cuda.current_device()))

torch.manual_seed(time.time())
device = torch.device("cuda:%d"%args.gpu) #cuda
torch.backends.cudnn.enabled=True

print ('\ntorch:', torch.__version__)
print ('cuda: ', torch.version.cuda)

subject = args.subj
saveext = ".png"
savearg = {'format':'png', 'dpi': 120, 'facecolor': None}
timestamp = time.strftime('%b-%d-%Y_%H%M', time.localtime())
model_name = 'dnn_fwrf'

output_dir = nsd_root + "output/S%02d/%s_%s/" % (subject,model_name,timestamp)
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

print ("Time Stamp: %s" % timestamp)

exp_design = loadmat(exp_design_file)
ordering = exp_design['masterordering'].flatten() - 1 # zero-indexed ordering of indices (matlab-like to python-like)

image_data_set = h5py.File(stim_root + "S%d_stimuli_227.h5py"%subject, 'r')
image_data = np.copy(image_data_set['stimuli']).astype(np.float32) / 255.
image_data_set.close()

print (image_data.shape)
print (image_data.dtype)
print (np.min(image_data[0]), np.max(image_data[0]))

trials = np.array([27750, 27750, 21750, 20250, 27750, 21750, 27750, 20250])  #the trials available so far
data_size = trials[subject-1]
ordering_data = ordering[:data_size]
shared_mask = ordering_data<1000  # the first 1000 indices are the shared indices

val_size = np.sum(shared_mask)
trn_size = data_size - val_size
print ("Validation size =", val_size, ", Training size =", trn_size)

stim_data = image_data[ordering_data]  # reduce to only the samples available thus far
trn_stim_data = stim_data[~shared_mask]
val_stim_data = stim_data[shared_mask]
val_image_data = image_data[:1000]

print ('cudnn:', torch.backends.cudnn.version())
print ('dtype:', torch.get_default_dtype())
ROIs = ['social','value','emotion']
print(ROIs)
roi_num = len(ROIs)
roi_data = np.zeros([data_size, roi_num])

n = 0
del_idx = []
for roi in ROIs:
    roi_data[:,n] = np.genfromtxt(meanROIbeta_root + 'roiavgbeta/subj%02d/meanbeta_'%subject + roi + '.txt')
    if np.isnan(np.sum(roi_data[:,n])):
    	del_idx.append(n)
    n += 1

roi_data = np.delete(roi_data, del_idx, axis=1) 
trn_roi_data = roi_data[~shared_mask]
val_roi_data = roi_data[shared_mask]

from torchmodel.models.alexnet import Alexnet_fmaps
_fmaps_fn = Alexnet_fmaps().to(device)

_x = torch.tensor(image_data[:100]).to(device) # the input variable.
_fmaps = _fmaps_fn(_x)
for k,_fm in enumerate(_fmaps):
    print (_fm.size())  

from src.torch_feature_space import filter_dnn_feature_maps

_fmaps_fn, lmask, fmask, tuning_masks = filter_dnn_feature_maps(image_data, _fmaps_fn, batch_size=100, fmap_max=512)
_x = torch.tensor(image_data[:100]).to(device) 
_fmaps = _fmaps_fn(_x)
for k,_fm in enumerate(_fmaps):
    print (_fm.size())   

from src.rf_grid    import linspace, logspace, model_space, model_space_pyramid
from src.torch_fwrf import learn_params_ridge_regression, get_predictions

aperture = np.float32(1)
nx = ny = 11
smin, smax = np.float32(0.04), np.float32(0.4)
ns = 8
models = model_space_pyramid(logspace(ns)(smin, smax), min_spacing=1.4, aperture=1.1*aperture)
print ('candidate count = ', len(models))


sample_batch_size = 200
voxel_batch_size = 500
holdout_size = 3000
lambdas = np.logspace(3.,7.,9, dtype=np.float32)

from src.torch_fwrf import  learn_params_ridge_regression, get_predictions, Torch_fwRF_voxel_block

best_losses, best_lambdas, best_params = learn_params_ridge_regression(
    trn_stim_data, trn_roi_data, _fmaps_fn, models, lambdas, \
    aperture=aperture, _nonlinearity=None, zscore=True, sample_batch_size=sample_batch_size, \
    voxel_batch_size=voxel_batch_size, holdout_size=holdout_size, shuffle=False, add_bias=True)
print ([p.shape if p is not None else None for p in best_params])

param_batch = [p[:voxel_batch_size] if p is not None else None for p in best_params]
_fwrf_fn = Torch_fwRF_voxel_block(_fmaps_fn, param_batch, _nonlinearity=None, input_shape=image_data.shape, aperture=1.0)

voxel_pred = get_predictions(val_image_data, _fmaps_fn, _fwrf_fn, best_params, sample_batch_size=sample_batch_size)

val_voxel_pred = voxel_pred[ordering[:data_size][shared_mask]]
val_cc  = np.zeros(shape=(val_voxel_pred.shape[1]), dtype=fpX)
for v in tqdm(range(val_voxel_pred.shape[1])):    
    val_cc[v] = np.corrcoef(val_roi_data[:,v], val_voxel_pred[:,v])[0,1]  
val_cc = np.nan_to_num(val_cc)

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
model_params = {
    'lmask': lmask,
    'fmask': fmask,
    'tuning_masks': tuning_masks,
    'aperture': aperture,
    'val_size': val_size,
    'trn_size': trn_size,
    'shared_mask': shared_mask,
    'image_order': ordering_data,
    'params': best_params,
    'lambdas': lambdas, 
    'best_lambdas': best_lambdas,
    'val_cc': val_cc,
    }

print (timestamp)
save_stuff(output_dir + "model_params", flatten_dict(model_params))

ROIs_label =  ['social','value','emotion']
ROIs_label = np.delete(ROIs_label,del_idx)
plt.figure(figsize=(16,6))
plt.bar(ROIs_label,val_cc)
plt.savefig(output_dir + 'acc.png')
print('Done!')
