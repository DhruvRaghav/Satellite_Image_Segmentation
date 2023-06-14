from __future__ import division
import extra_functions
import numpy as np
from keras.models import load_model
import matplotlib.pyplot as plt
from keras import backend as K
from keras.backend import binary_crossentropy
from PIL import Image,ImageFilter
import tensorflow as tf
from tensorflow import keras
import os
import cv2
batch_size =2
smooth = 1e-12
import base64
import json

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
    # json_name = 'architecture_8_50_buildings_3_' + cross + '.json'
    # weight_name = 'model_weights_8_50_buildings_3_' + cross + '.h5'
    # model = model_from_json(open(os.path.join('cache', json_name)).read())
    # model.load_weights(os.path.join('cache', weight_name))
    tf.keras.backend.set_session(get_session())

    with tf.device('/gpu:0'):


        model = load_model('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/45.h5', custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                                                         'jaccard_coef_int': jaccard_coef_int,
                                                                         'jaccard_coef': jaccard_coef},compile=False)
    graph=tf.get_default_graph()

    return model,graph

def read_model_Rd():
        # json_name = 'architecture_8_50_buildings_3_' + cross + '.json'
        # weight_name = 'model_weights_8_50_buildings_3_' + cross + '.h5'
        # model = model_from_json(open(os.path.join('cache', json_name)).read())
        # model.load_weights(os.path.join('cache', weight_name))
    tf.keras.backend.set_session(get_session())


    with tf.device('/gpu:0'):
        # model1 = load_model('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/roadnet_models/100.h5', custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
        #                                                                  'jaccard_coef_int': jaccard_coef_int,
        #                                                                  'jaccard_coef': jaccard_coef},compile=False)
        model1 = load_model('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/25.h5',
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
        # print("Mask is going to get saved at location :  %s" % path1)

        im = Image.open(path1+"/"+image_id+'.jpg')
       # os.remove(path1+"/"+image_id+'.jpg')
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
        # """code to save the predicted image as jpg"""
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)




    # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)

def predictOBJECT(path1,model,image_id,graph,image_size):
    threshold = 0.3
    with graph.as_default():
     with tf.device('/gpu:0'):
        # print("Mask is going to get saved at location :  %s" % path1)

        im = Image.open(path1+"/"+image_id+'.jpg')
       # os.remove(path1+"/"+image_id+'.jpg')
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
        # """code to save the predicted image as jpg"""
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)




    # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)






def predict_FP_Tif_PL(path1,model,image_id,graph,image_size):
    threshold = 0.3
    with graph.as_default():
     with tf.device('/gpu:0'):
        print("Mask is going to get saved at location :  %s" % path1)

        im = Image.open(path1+"/"+image_id+'.jpeg')
        print(image_id)
        #os.remove(path1+"/"+image_id+'.jpeg')
        image = im.convert('RGB')
        print("1")
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
        # """code to save the predicted image as jpg"""
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)
    # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)


def predict_RD(path1,model1,image_id,graph1,image_size,bounds):
    threshold = 0.3
    with graph1.as_default():
     with tf.device('/gpu:0'):
        im = Image.open(path1 + "/" + image_id + '.jpg')
        # os.remove(path1 + "/" + image_id + '.jpg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
        # image=image.filter(ImageFilter.EDGE_ENHANCE)
        # img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
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
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)
        #plt.imsave(path1 +"/"+image_id+'_mask.png',np.squeeze(new_mask, -1)*255, cmap='gray', dpi=1)
        # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)

        with open(path1 + "/" + image_id + '.jpg', "rb") as r1:
            converted_string = base64.b64encode(r1.read())
            # converted_string.decode("utf-8")
            # print(converted_string)
            # print(converted_string.decode('utf-8'))

        with open('encode.bin', "wb") as file:
            file.write(converted_string)

        with open(path1 + "/" + image_id + '_mask.png', "rb") as r:
            converted_string_1 = base64.b64encode(r.read())
            # converted_string_1.decode("utf-8")
            # print(converted_string_1)
            # print(converted_string.decode('utf-8'))

        with open('encode_1.bin', "wb") as file:
            file.write(converted_string_1)

        c = {"1": converted_string, "2": converted_string_1}
        json_str = json.dumps(
            {'I M A G E': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8')),
             "BOUNDS": bounds})

        return json_str



def predict_RD_Tif_PL(path1,model1,image_id,graph1,image_size):
    threshold = 0.3
    with graph1.as_default():
     with tf.device('/gpu:0'):
        im = Image.open(path1 + "/" + image_id + '.jpeg')
        #os.remove(path1 + "/" + image_id + '.jpeg')
        image = im.convert('RGB')
        image=image.filter(ImageFilter.SHARPEN)
        # image=image.filter(ImageFilter.EDGE_ENHANCE)
        # img=cv2.cvtColor(img,cv2.COLOR_RGBA2RGB)
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
        # os.makedirs("/home/prateek/Downloads/satellite_image/" + str(date.today()) + "/overlays", exist_ok=True)
        plt.imsave(path1+"/"+image_id+'_mask.png',np.squeeze(new_mask, -1) * 255, cmap='gray', dpi=1)
        #plt.imsave(path1 +"/"+image_id+'_mask.png',np.squeeze(new_mask, -1)*255, cmap='gray', dpi=1)
        # return cv2.cvtColor(np.squeeze(new_mask, -1) * 255,cv2.COLOR_GRAY2RGB)




def postprocessing(image_path,mask_path,path1,in_file, bounds):
                 print("postprocessed")
                 image = cv2.imread(image_path)
                 image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

                 maskpath = mask_path
                 mask = cv2.imread(maskpath )

                 merge = cv2.bitwise_and(image, mask)

                 merge = cv2.cvtColor(merge, cv2.COLOR_RGB2GRAY)
                 threshold = cv2.threshold(merge, 90, 255, cv2.THRESH_BINARY)[1]

                 erosion = cv2.erode(threshold, None, iterations=2)
                 dilation = cv2.dilate(erosion, None, iterations=2)  # final mask

                 plt.imsave(path1 + "/" + in_file + '_mask.png',dilation, cmap='gray', dpi=1)




                 with open(path1 + "/" + in_file + '.jpg',"rb") as r1:
                     converted_string = base64.b64encode(r1.read())
                     # converted_string.decode("utf-8")
                 #print(converted_string)
                 # print(converted_string.decode('utf-8'))

                 # with open('encode.bin', "wb") as file:
                 #     file.write(converted_string)




                 with open(path1 + "/" + in_file + '_mask.png', "rb") as r:
                     converted_string_1 = base64.b64encode(r.read())
                     # converted_string_1.decode("utf-8")
                 #print(converted_string_1)
                 # print(converted_string.decode('utf-8'))

                 # with open('encode_1.bin', "wb") as file:
                 #     file.write(converted_string_1)


                 # c={"1":converted_string,"2":converted_string_1}
                 json_str = json.dumps({'I M A G E': converted_string.decode('utf-8'),'M A S K':converted_string_1.decode(('utf-8')),"BOUNDS":bounds})
                 print(type(json_str))
                 return json_str



def changeImageSize(maxWidth,maxHeight,im):
    print(im.size)
    widthRatio = maxWidth / im.size[0]
    heightRatio = maxHeight / im.size[1]

    newWidth = int(widthRatio * im.size[0])
    newHeight = int(heightRatio * im.size[1])

    newImage = im.resize((newWidth, newHeight))
    return newImage


def postprocessingOBJECT(image_path, mask_path, path1, in_file):
    print("postprocessed")
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    maskpath = mask_path
    mask = cv2.imread(maskpath)

    merge = cv2.bitwise_and(image, mask)

    merge = cv2.cvtColor(merge, cv2.COLOR_RGB2GRAY)
    threshold = cv2.threshold(merge, 90, 255, cv2.THRESH_BINARY)[1]

    erosion = cv2.erode(threshold, None, iterations=2)
    dilation = cv2.dilate(erosion, None, iterations=2)  # final mask

    plt.imsave(path1 + "/" + in_file + '_mask.png', dilation, cmap='gray', dpi=1)

    '''----------------------------------------------------------------------------------'''
    im2 = Image.open(path1 + "/" + in_file + '_mask.png')
    im = Image.open(image_path)

    # Make the images of uniform size
    print("1")
    #image3 = changeImageSize(800, 500, im)
    print("2")
    #image4 = changeImageSize(800, 500, im2)

    # Make sure images got an alpha channel
    print("3")
    image5 = im.convert("RGBA")
    image6 = im2.convert("RGBA")

    # Display the images
    # image5.show()
    # image6.show()

    # alpha-blend the images with varying values of alpha
    # alphaBlended1 = Image.blend(image5, image6, alpha=.2)
    alphaBlended2 = Image.blend(image5, image6, alpha=.4)
    print("4")

    # Display the alpha-blended images
    # alphaBlended1.show()
    # alphaBlended2.show()

    # os.makedirs("/home/ceinfo/Desktop/50_new/FP_ASUTOSH/overlay/" + "(overlays)", exist_ok=True)
    # print("5")
    # # plt.imsave("/mnt/vol1/DhruvRaghav/2021(improved models)/pythonProject/images/MGIS VISION/building_model/bhuvan/banglore/(overlays)" + image_id, np.squeeze(alphaBlended2) * 255, cmap='gray', dpi=1)
    # print("6")

    # alpha = 0.6
    # new_mask = np.squeeze(new_mask, -1)
    # color_mask = np.dstack((new_mask, new_mask, new_mask))
    #
    # image = image - image * (color_mask * 0.3)
    # image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
    # print(image)

    plt.imsave(path1 + "/" + in_file + 'overlay.png', alphaBlended2,
               dpi=1)

    '''----------------------------------------------------------------------------------'''

    with open(path1 + "/" + in_file + 'overlay.png', "rb") as r1:
        converted_string = base64.b64encode(r1.read())
        # converted_string.decode("utf-8")
    # print(converted_string)
    # print(converted_string.decode('utf-8'))

    # with open('encode.bin', "wb") as file:
    #     file.write(converted_string)

    with open(path1 + "/" + in_file + '_mask.png', "rb") as r:
        converted_string_1 = base64.b64encode(r.read())
        # converted_string_1.decode("utf-8")
    # print(converted_string_1)
    # print(converted_string.decode('utf-8'))

    # with open('encode_1.bin', "wb") as file:
    #     file.write(converted_string_1)

    # c={"1":converted_string,"2":converted_string_1}
    json_str = json.dumps(
        {'I M A G E': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8')),
         })
    print(type(json_str))
    return json_str


if __name__ == '__main__':
    predict_FP_Tif_PL("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads2/", "sat_image_1")