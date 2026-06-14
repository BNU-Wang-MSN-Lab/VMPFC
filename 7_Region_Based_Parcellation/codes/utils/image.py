import numpy as np
import nibabel as nib



def select_left_side(image):
    affine = image.affine
    data = image.get_fdata()
    i, j, k = np.indices(data.shape)
    voxels = np.column_stack((i.flatten(), j.flatten(), k.flatten()))
    coords = nib.affines.apply_affine(affine, voxels)
    coords = coords[:, 0].reshape(data.shape)
    right_mask = coords > 0

    new_data = image.get_fdata().copy()
    new_data[right_mask] = 0
    new_img = nib.Nifti1Image(new_data, affine)
    return new_img


