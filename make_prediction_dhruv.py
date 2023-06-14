from __future__ import division
import cv2
import numpy as np
from os import walk
import os
import extra_functions
import numpy as np
# from keras.models import model_from_json
from keras.models import load_model
import matplotlib.pyplot as plt
from datetime import date
from keras import backend as K
from keras.backend import binary_crossentropy
import tensorflow as tf
import matplotlib.image as mpimg

# from segmentation_models.losses import bce_jaccard_loss
# from segmentation_models.metrics import iou_score
batch_size = 2
smooth = 1e-12
#mooth = 1e-12


def jaccard_coef(y_true, y_pred):
    intersection = K.sum(y_true * y_pred, axis=[0, 1, 2])
    sum_ = K.sum(y_true + y_pred, axis=[0, 1, 2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_int(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))

    intersection = K.sum(y_true * y_pred_pos, axis=[0, 1, 2])
    sum_ = K.sum(y_true + y_pred_pos, axis=[0, 1, 2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_loss(y_true, y_pred):
    return -K.log(jaccard_coef(y_true, y_pred)) + binary_crossentropy(y_pred, y_true)


def read_model(cross=''):
    # json_name = 'architecture_8_50_buildings_3_' + cross + '.json'
    # weight_name = 'model_weights_8_50_buildings_3_' + cross + '.h5'
    # model = model_from_json(open(os.path.join('cache', json_name)).read())
    # model.load_weights(os.path.join('cache', weight_name))
    # keras.backend.tensorflow_backend.set_session(get_session())
    with tf.device('/gpu:0'):
        # model = load_model(
        # '/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/snapshots/2020-07-16/2/100.h5',
        # custom_objects = {'jaccard_coef_loss': jaccard_coef_loss,'jaccard_coef_int': jaccard_coef_int,'jaccard_coef': jaccard_coef},compile=False)
        model = load_model(
            '/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/snapshots/2022-09-05/2/06.h5',
            custom_objects={'jaccard_coef_loss': jaccard_coef_loss, 'jaccard_coef_int': jaccard_coef_int,
                            'jaccard_coef': jaccard_coef}, compile=False)
    #                    custom_objects={'bce_jaccard_loss': bce_jaccard_loss,'iou_score':iou_score})

    return model


model = read_model()
print(model.summary())

data_path = '/home/ceinfo/Desktop/habit__test/'
num_channels = 3
num_mask_channels = 1
threshold = 2

ids = []
test_ids = []
for (dirpath, dirnames, filenames) in walk(data_path):
    print(filenames)
    ids.extend(filenames)
    break

for i in ids:
    if 'jpg' or 'png' in i:
        test_ids.append(i)
print("Number of images: ", len(test_ids))

result = []


def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x


def read_image_test(data_path, image_id):
    # images on which testing is to be done. supply fresh images.

    '''for building preprocessed images '''
    img = mpimg.imread(data_path + image_id)[:, :, :3]

    '''for roads preprocessed images '''
    # img=mpimg.imread('/home/ceinfo/Desktop/Images_Extraction/STATE_IMAGE/UP/'+image_id)[:,:,:3]

    img = img.astype(np.float32)
    img = img / 255;
    return img


for image_id in test_ids:
    print("Predicting: ", image_id)
    with tf.device('/gpu:0'):
        image = read_image_test(data_path, image_id)
        predicted_mask = extra_functions.make_prediction_cropped(model, image, batch_size, size=(512, 512))

        image_v = flip_axis(image, 0)
        predicted_mask_v = extra_functions.make_prediction_cropped(model, image_v, batch_size, size=(512, 512))

        image_h = flip_axis(image, 1)
        predicted_mask_h = extra_functions.make_prediction_cropped(model, image_h, batch_size, size=(512, 512))

        image_s = image.swapaxes(0, 1)
        predicted_mask_s = extra_functions.make_prediction_cropped(model, image_s, batch_size, size=(512, 512))
        new_mask = np.power(predicted_mask *
                            flip_axis(predicted_mask_v, 0) *
                            flip_axis(predicted_mask_h, 1) *
                            predicted_mask_s.swapaxes(0, 1), 0.25)
        print("helloworld",new_mask)
        new_mask[new_mask >= threshold] = 1;
        new_mask[new_mask < threshold] = 0;

        """code to save the predicted image as jpg"""
        os.makedirs("/home/ceinfo/Desktop/result_delete/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave("/home/ceinfo/Desktop/result_delete/" + str(date.today()) + '/' + image_id[:-4] + ".png",
                   np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)

        alpha = 0.6
        new_mask = np.squeeze(new_mask, -1)
        color_mask = np.dstack((new_mask, new_mask, new_mask))

        image = image - image * (color_mask * 0.3)
        image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
        # print(image)

    plt.imsave("/home/ceinfo/Desktop/result_delete/" + str(date.today()) + "/overlays/overlay_" + image_id[:-4] + ".png",
               image, dpi=1)

del (model)