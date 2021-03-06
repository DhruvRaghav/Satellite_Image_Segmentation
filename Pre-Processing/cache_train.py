"""
Script that caches train data for future training
"""


from __future__ import division
from os import walk
import os
import extra_functions
import h5py
import numpy as np
from datasets1 import SlippyMapTiles
'''to change the extention in folder'''
''' for f in *.tif; do mv -- "$f" "${f%.tif}.tiff"; done'''
#The mask you"hv generated in data preparation phase or  if  you already have the mask
#insert the path of it in this data_path'''

'''***************for roads*************'''
#data_path = '/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/rd_masks/'


'''**************for building footprints***********'''
# data_path='/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/training images/satellite_image_with_masks/FP_Mask_3/'
data_path='/home/ceinfo/Documents/training_data_satellite_images/road/masks/'
def cache_train():

    fp_files = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        fp_files.extend(filenames)
        break

    print("Number of Training images: ", len(fp_files))
    print("Processing...")
    # new_data = SlippyMapTiles('/mnt/vol1/PycharmProjects/robosat-master/datasets/training/images','/mnt/vol1/PycharmProjects/robosat-master/datasets/training/labels')
    num_channels = 3
    num_mask_channels = 1
    # image_rows = 3705
    # image_cols = 4800
    image_rows = 1500
    image_cols = 1500
    num_train = len(fp_files)

    '''***************for roads*************'''
    f = h5py.File(os.path.join('cache', 'train_rd_new.h5'), 'w')



    '''***************for building *************'''
    #f = h5py.File(os.path.join('cache', 'train_fp_dhruv.h5'), 'w')

    imgs = f.create_dataset('train', (num_train, image_rows, image_cols,num_channels), dtype=np.float16)
    imgs_mask = f.create_dataset('train_mask', (num_train, image_rows, image_cols,num_mask_channels), dtype=np.uint8)

    ids = []
    i = 0

    for image_id in sorted(fp_files):
        print(image_id)
        image = extra_functions.read_image(image_id)
        mask = extra_functions.read_mask(image_id)
        height, width, _ = image.shape

        imgs[i] = image
        imgs_mask[i] = mask

        ids += [image_id]
        i += 1
    # for images in new_data:
    #     imgs[i]=images[0]
    #     imgs_mask[i]=images[1]
    #     ids +=[images[2]]
    #     i+=1


    # fix from there: https://github.com/h5py/h5py/issues/441
    f['train_ids'] = np.array(ids).astype('|S9')

    f.close()
    print("Training Images Cached Successfully.")

if __name__ == '__main__':
    cache_train()
