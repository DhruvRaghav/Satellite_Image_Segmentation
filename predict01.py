from __future__ import division
import extra_functions
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
from keras import backend as K
from keras.backend import binary_crossentropy
from PIL import Image,ImageFilter
import tensorflow as tf
batch_size =2
smooth = 1e-12

def get_session():
    config=tf.ConfigProto()
    config.gpu_options.allow_growth = True
    config.gpu_options.per_process_gpu_memory_fraction = 0.3
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
    tf.keras.backend.set_session(get_session())

    with tf.device('/gpu:0'):
        model = load_model('Building_model.h5', custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                                                         'jaccard_coef_int': jaccard_coef_int,
                                                                         'jaccard_coef': jaccard_coef},compile=False)
    graph=tf.get_default_graph()

    return model,graph

def read_model_Rd():
    tf.keras.backend.set_session(get_session())


    with tf.device('/gpu:0'):
        model1 = load_model('Road_model.h5',
                            custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                            'jaccard_coef_int': jaccard_coef_int,
                                            'jaccard_coef': jaccard_coef}, compile=False)

    graph1=tf.get_default_graph()
    return model1,graph1

def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x

def predict01(path1,model,image_id,graph,image_size):
    threshold = 0.3
    with graph.as_default():
     with tf.device('/gpu:0'):
        im = Image.open(path1+"/"+image_id+'.jpg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
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
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)




def predict_FP_Tif_PL(path1,model,image_id,graph,image_size):
    threshold = 0.3
    with graph.as_default():
     with tf.device('/gpu:0'):
        print("Mask is going to get saved at location :  %s" % path1)

        im = Image.open(path1+"/"+image_id+'.jpeg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
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
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)


def predict_RD(path1,model1,image_id,graph1,image_size):
    threshold = 0.3
    with graph1.as_default():
     with tf.device('/gpu:0'):
        im = Image.open(path1 + "/" + image_id + '.jpg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
        image = np.array(image)
        image = image.astype(np.float32)
        image = image / 255;
        predicted_mask = extra_functions.make_prediction_cropped(model1, image, batch_size, size=image_size)

        image_v = flip_axis(image, 0)
        predicted_mask_v = extra_functions.make_prediction_cropped(model1, image_v, batch_size, size=image_size)

        image_h = flip_axis(image, 1)
        predicted_mask_h = extra_functions.make_prediction_cropped(model1, image_h, batch_size, size=image_size)

        image_s = image.swapaxes(0, 1)
        predicted_mask_s = extra_functions.make_prediction_cropped(model1, image_s, batch_size, size=image_size)
        new_mask = np.power(predicted_mask *
                            flip_axis(predicted_mask_v, 0) *
                            flip_axis(predicted_mask_h, 1) *
                            predicted_mask_s.swapaxes(0, 1), 0.25)
        new_mask[new_mask >= threshold] = 1;
        new_mask[new_mask < threshold] = 0;
        # """code to save the predicted image as jpg"""
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)



def predict_RD_Tif_PL(path1,model1,image_id,graph1,image_size):
    threshold = 0.3
    with graph1.as_default():
     with tf.device('/gpu:0'):
        im = Image.open(path1 + "/" + image_id + '.jpeg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
        image = np.array(image)
        image = image.astype(np.float32)
        image = image / 255;
        predicted_mask = extra_functions.make_prediction_cropped(model1, image, batch_size, size=image_size)

        image_v = flip_axis(image, 0)
        predicted_mask_v = extra_functions.make_prediction_cropped(model1, image_v, batch_size, size=image_size)

        image_h = flip_axis(image, 1)
        predicted_mask_h = extra_functions.make_prediction_cropped(model1, image_h, batch_size, size=image_size)

        image_s = image.swapaxes(0, 1)
        predicted_mask_s = extra_functions.make_prediction_cropped(model1, image_s, batch_size, size=image_size)
        new_mask = np.power(predicted_mask *
                            flip_axis(predicted_mask_v, 0) *
                            flip_axis(predicted_mask_h, 1) *
                            predicted_mask_s.swapaxes(0, 1), 0.25)
        new_mask[new_mask >= threshold] = 1;
        new_mask[new_mask < threshold] = 0;
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)