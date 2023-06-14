from __future__ import division

import matplotlib.image as mpimg
import numpy as np
import cv2

def flip_axis1(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x

def read_image(image_id):
    #path of images whose preprocessing is already done . Contains image with tab files

    '''for bulding footprint preprocessed images '''
    img=mpimg.imread('/mnt/vol2/desktop_sep/7_sep/training_images/'+image_id)


    '''for roads preprocessed images '''
    #img=mpimg.imread('/home/ceinfo/Documents/training_data_satellite_images/road/images/'+image_id)
    img = img.astype(np.float16)
    img = img/255;
    return img

def read_image_test(image_id):
    #images on which testing is to be done. supply fresh images.

    '''for building preprocessed images '''
    #img=mpimg.imread('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/training images/test_imgs/'+image_id)[:,:,:3]

    '''for roads preprocessed images '''
    img=mpimg.imread('/mnt/vol2/desktop_sep/7_sep/training_images/'+image_id)[:,:,:3]

    img = img.astype(np.float32)
    img = img/255;
    return img


def read_mask(i):
    '''for building preprocessed images '''
    #mask = cv2.imread('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/training images/satellite_image_with_masks/FP_Mask_3/'+i)

    '''for roads preprocessed images '''
    mask = cv2.imread('/mnt/vol2/desktop_sep/7_sep/uploads03/' + i)

    mask=cv2.cvtColor(mask,cv2.COLOR_BGR2GRAY)
    mask = np.expand_dims(mask,axis=-1)
    mask = mask/255
    mask[mask<0.5]=0
    mask[mask>=0.5]=1
    mask = np.array(mask,dtype=np.uint8)
    return mask

def make_prediction_cropped(model, image, batch_size, size = (288,288), num_channels=3, num_masks=1):
    
    height = image.shape[0]
    width = image.shape[1]
    ##pad the image with mirrors
    image = np.concatenate([image,flip_axis1(image, 1)],axis=1)
    image = np.concatenate([image,flip_axis1(image,0)],axis=0)
    
    ##count number of patches required from the image
    if(height%size[0]==0):

        h_num = int(height/size[0])
    else:
        h_num = int(height/size[0]) + 1

    if(width%size[1]==0):
        w_num = int(width/size[1])
    else:
        w_num = int(width/size[1]) + 1
    
    patches = np.zeros(shape=(h_num*w_num,size[0],size[1],num_channels))
    
    n = 0
    for i in range(h_num):
        for j in range(w_num):
            patches[n] = image[i*size[0]:i*size[0]+size[0],j*size[1]:j*size[1]+size[1],:]
            n += 1
    
    prediction = model.predict(patches,batch_size=batch_size)

    predicted_mask = np.zeros(shape = (h_num*size[0], w_num*size[1],num_masks))


    n = 0
    for i in range(h_num):
        for j in range(w_num):
            predicted_mask[i*size[0]:i*size[0]+size[0],j*size[1]:j*size[1]+size[1],:] = prediction[n]
            n += 1
    return predicted_mask[:height, :width,:]
