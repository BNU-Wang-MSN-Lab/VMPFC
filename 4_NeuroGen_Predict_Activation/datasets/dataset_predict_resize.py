import argparse
import time
import torch
from torch import nn
import numpy as np
import os
import cv2
from PIL import Image
import h5py
from visualize import center_crop, save_image, save_gif
from encoding import load_encoding
from src.file_utility import save_stuff, flatten_dict, embed_dict
from encoding import Torch_filter_fmaps
import matplotlib.pyplot as plt
import pandas as pd

parser = argparse.ArgumentParser(prog='dataset screening',
                                 description='Input the images and get the brain response prediction',
                                 usage='python dataset_predict_resize.py --subj i --gpu j')

parser.add_argument('--subj', default = '1', type=int)
parser.add_argument('--gpu', default = '0', type=int)
args = parser.parse_args()
subject = args.subj

torch.backends.cudnn.enabled=True
device = torch.device("cuda:%d"%args.gpu if torch.cuda.is_available() else "cpu")
voxel_batch_size = 500

from torchmodel.models.alexnet import Alexnet_fmaps
from src.torch_fwrf import  get_predictions, Torch_fwRF_voxel_block

def load_encoding(subject, model_name='dnn_fwrf', device=torch.device("cpu")):
    voxel_batch_size = 20

    output_dir = "../model_trainning/output/S%02d/model/" % (subject)
    model_params_set = h5py.File(output_dir + 'model_params.h5py', 'r')
    model_params = embed_dict({k: np.copy(d) for k, d in model_params_set.items()})
    model_params_set.close()

    _fmaps_fn = Alexnet_fmaps().to(device)
    _fmaps_fn = Torch_filter_fmaps(_fmaps_fn, model_params['lmask'], model_params['fmask'])

    params = [p[:voxel_batch_size] if p is not None else None for p in model_params['params']]

    _fwrf_fn = Torch_fwRF_voxel_block(_fmaps_fn, params, _nonlinearity=None, input_shape=(1,3,227,227), aperture=1.0)
    
    with torch.no_grad():
        _fwrf_fn.load_voxel_block(*[p[0:voxel_batch_size] if p is not None else None for p in model_params['params']])

    return _fmaps_fn, _fwrf_fn, params

mean_acc_total = []
sample_batch_size = 100

dataset_name = 'Parade'
image_data_set = h5py.File(f'./social/h5py_resize/{dataset_name}.h5', 'r') 
image_data = np.array(np.copy(image_data_set['stimuli']).astype(np.float32) / 255).transpose(0,3,1,2)
print(image_data.shape)
image_data_set.close()

fmaps_fn, fwrf_fn, best_params = load_encoding(subject=args.subj, model_name='dnn_fwrf')
voxel_pred = get_predictions(image_data, fmaps_fn, fwrf_fn, best_params, sample_batch_size=sample_batch_size)
print(voxel_pred)

##--------------------------------------------------------------------------------------------------------------
test=pd.DataFrame(data=voxel_pred)
output_dir = './predicted_activations/social/s%01d'%subject
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

act_dir = output_dir + f'/{dataset_name}.csv'  
test.to_csv(act_dir,encoding='gbk')
