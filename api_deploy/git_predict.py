from __future__ import division
import cv2
# import numpy as np
from os import walk
import os
import extra_functions
import numpy as np
from keras.models import model_from_json
from keras.models import load_model
import matplotlib.pyplot as plt
from datetime import date
from keras import backend as K
from keras.backend import binary_crossentropy
# import tensorflow as tf
from PIL import Image,ImageFilter
import tensorflow as tf
import os
import keras
import matplotlib.image as mpimg
# from segmentation_models.losses import bce_jaccard_loss
# from segmentation_models.metrics import iou_score
batch_size =2
smooth = 1e-12

def get_session():
    config=tf.ConfigProto()
    config.gpu_options.allow_growth = True
    # config.gpu_options.per_process_gpu_memory_fraction = 0.3
    return tf.Session(config=config)


def jaccard_coef(y_true, y_pred):
    intersection = K.sum(y_true * y_pred, axis=[0,1,2])
    sum_ = K.sum(y_true + y_pred, axis=[0,1,2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_int(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))

    intersection = K.sum(y_true * y_pred_pos, axis= [0,1,2])
    sum_ = K.sum(y_true + y_pred_pos, axis=[0,1,2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_loss(y_true, y_pred):
    return -K.log(jaccard_coef(y_true, y_pred)) + binary_crossentropy(y_pred, y_true)


def read_model():
    # json_name = 'architecture_8_50_buildings_3_' + cross + '.json'
    # weight_name = 'model_weights_8_50_buildings_3_' + cross + '.h5'
    # model = model_from_json(open(os.path.join('cache', json_name)).read())
    # model.load_weights(os.path.join('cache', weight_name))
    # keras.backend.tensorflow_backend.set_session(get_session())
    # K.set_session(get_session())
    tf.keras.backend.set_session(get_session())
    # session = keras.backend.get_session()
    # session=get_session()
    # init = tf.global_variables_initializer()
    # session.run(init)
    with tf.device('/gpu:0'):
    # keras.backend.tensorflow_backend.set_session(get_session())
    #     tf.keras.backend.set_session(get_session())
    #     sess=get_session()
    #     K.set_session(sess)
    #     graph = tf.get_default_graph()
        model = load_model('/mnt/vol1/Deployment_projects/satellite_image_segmentation/45.h5', custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                                                         'jaccard_coef_int': jaccard_coef_int,
                                                                         'jaccard_coef': jaccard_coef},compile=False)
    # model = load_model('/mnt/vol1/PycharmProjects/segmentation_models-master/Linknet_bce_loss/2/12.h5',
    #                    custom_objects={'bce_jaccard_loss': bce_jaccard_loss,'iou_score':iou_score})
    graph=tf.compat.v1.get_default_graph()
    return model,graph

def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x

def predict(model,image_id,graph,image_size):
    threshold = 0.3
    # sess=K.get_session()
    # with graph.as_default():
    model = load_model('/mnt/vol1/Deployment_projects/satellite_image_segmentation/45.h5',
                           custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                           'jaccard_coef_int': jaccard_coef_int,
                                           'jaccard_coef': jaccard_coef}, compile=False)
      # tf.keras.backend.set_session(get_session())
      # keras.backend.tensorflow_backend.set_session(get_session())
      # K.set_session(get_session())
      # session = keras.backend.get_session()
      # init = tf.global_variables_initializer()
      # session.run(init)
    with tf.device('/gpu:0'):
        # image = extra_functions.read_image_test(image_id)
        # image = mpimg.imread('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id+'.png')[:,:,:3]
        im = Image.open('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id+'.png')
        # os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id+'.png')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
        # image=image.filter(ImageFilter.EDGE_ENHANCE)
        # img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
        image = np.array(image)
        image = image.astype(np.float32)
        image = image / 255;
        predicted_mask = extra_functions.make_prediction_cropped(model, image, batch_size, size=image_size)

        image_v = flip_axis(image, 0)
        predicted_mask_v = extra_functions.make_prediction_cropped(model, image_v, batch_size, size=image_size)

        image_h = flip_axis(image, 1)
        predicted_mask_h = extra_functions.make_prediction_cropped(model, image_h, batch_size, size=image_size)

        image_s = image.swapaxes(0, 1)
        predicted_mask_s = extra_functions.make_prediction_cropped(model, image_s, batch_size, size=image_size)
        new_mask = np.power(predicted_mask *
                            flip_axis(predicted_mask_v, 0) *
                            flip_axis(predicted_mask_h, 1) *
                            predicted_mask_s.swapaxes(0, 1), 0.25)
        new_mask[new_mask >= threshold] = 1;
        new_mask[new_mask < threshold] = 0;
        # plt.imshow(np.squeeze(new_mask, -1) * 255)
        # plt.show()
        # """code to save the predicted image as jpg"""
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/"+ image_id+'_mask.jpg',
                   np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)
    # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)

