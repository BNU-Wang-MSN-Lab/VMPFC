import os
from os import mkdir
import numpy as np
import matplotlib.pyplot as plt
import time
from PIL import Image
import h5py
import shutil

def resize_image(img, size):
    resized_img = img.resize((size, size), Image.ANTIALIAS)
    return resized_img

def get_smaller(path_in, path, size=227):
    if not os.path.exists(path):
        os.mkdir(path)

    list_image = os.listdir(path_in)
    list_image.sort()  
    print(list_image)

    for item in list_image:
        image = Image.open(os.path.join(path_in, item))
        try:
            smaller = resize_image(image, size)
        except OSError as e:
            print(f"Error loading image: {e}")
            continue
        smaller.save(os.path.join(path, item))
        
def createData(path):
    pics = os.listdir(path)
    pics.sort()  
    all_data = []

    for item in pics:
        print(item)
        try:
            img = Image.open(os.path.join(path, item))
            img_array = np.array(img)
            
            
            if img_array.ndim == 2:
                img_array = np.stack((img_array,)*3, axis=-1)
            elif img_array.shape[2] == 4:  
                img_array = img_array[:, :, :3]

            all_data.append(img_array)
        except Exception as e:
            print(f"{item} pic precessing error: {e}")
    return np.array(all_data)

def createSet(hf, name, data):
    hf.create_dataset(name, data=data)

dataset_name = 'Parade'
category = 'social'
in_path = f"./{category}/{dataset_name}"              
path_new = f'./{category}/resized_{dataset_name}'     

get_smaller(in_path, path=path_new)
hf = h5py.File(f'./{category}/h5py_resize/{dataset_name}.h5', 'w')                
all_data = createData(path_new)
print(all_data.shape)

createSet(hf, 'stimuli', all_data)
hf.close()
print('done!')


