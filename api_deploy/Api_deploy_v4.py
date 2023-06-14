import traceback
from flask import Flask, request,Response
app = Flask(__name__)
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
#from keras.models import load_model
# import detect_batch_old
# import detect_blur
import json
import geoio
import io

import cv2
from skimage import io



from api_deploy.geotiff import gdal_convert
import os

from api_deploy.pixel_to_lat_lon import geojson
from api_deploy.pixel_to_lat_lon_pixelsvalues_geojson import geojson1,geojson2
#from api_deploy.predict import predict,read_model,read_model_Rd
from api_deploy.vegetation import predict_veg
from api_deploy.Soil import predict_soil
from api_deploy.Ocean import predict_water,predict_water1
import tensorflow as tf
from api_deploy.predict01 import *



if not (os.path.exists('Logs')):
    os.makedirs('Logs/',exist_ok=False)
log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/'+log_filename, when='MIDNIGHT', backupCount=7)

formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

# logger = logging.getLogger('werkzeug')
logger = logging.getLogger('gunicorn.error')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logger.level)
logger.addHandler(handler)

logger.propagate = False




try:
     model,graph=read_model()
     model1,graph1 = read_model_Rd()
#    # model1,graph1=read_model("/mnt/vol1/Deployment_projects/satellite_image_segmentation/roadnet_models/83.h5")
#     # global graph
#     # graph=tf.get_default_graph()
#     #model = load_model("/mnt/vol1/Deployment_projects/satellite_image_segmentation/45.h5",custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
#                                                                     # 'jaccard_coef_int': jaccard_coef_int,
#                                                                      #'jaccard_coef': jaccard_coef},compile=False)
except Exception as e:
     print(e)
     logger.error(msg="model is not loaded")



'''to check the name of the GPU'''
#import tensorflow as tf
if tf.test.gpu_device_name():
    print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))
else:
   print("Please install GPU version of TF")




'''building footprints two function : -------func1 and func2----------'''

def func2(image,key):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN JPG FORM  & GEOTAG : 0 '''
    path = os.getcwd()
    print("The current working directory is %s" % path)
    print("creating a new directory now:")

    '''Directory'''
    directory = "uploads01"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    '''image name without extension'''
    in_file=image.filename[:-4]
    image_name = in_file


    '''to read image from postman in bgr fotmat'''
    print("going to read image")
    image_name_bgr = io.imread(image)


    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)

    '''prediction : mask will be generated:'''
    print("going to start prediction")
    if key=="FP":
        mask = predict01(path1,model, image_name, graph, (512, 512))
        print("prediction done : masks created")
    elif key=='RD':
        mask = predict_RD(path1,model1, image_name, graph1, (256, 256))
        print(" prediction done: road masks created")
    elif key =="VG":
        mask = predict_veg(path1,image_name)
        print(" prediction done: Vegetation masks created")
    elif key=="S":
        mask = predict_soil(path1,image_name)
    elif key=="W":
        mask = predict_water(path1)

    '''To create the goejson file use this function'''
    resp = geojson2(path1,image_name)
    print("geojson created at the location you mentioned")
    print(resp)
    return resp






@app.route('/satellite_FP/',methods=['POST'])  # Single Api
def FP():
    print ("Welcome to satellite image segmentation")
    resp=Response(status=200,content_type='application/json')
    image = request.files['file']  # Single image path
    #image = request.files.get('file', '')
    #image.save('/home/ceinfo/Desktop/testing/test_image1.jpg')


    try:
        if(request.content_type!=None):
             if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1=image.filename
                    get1=get1[-3:]
                    geotag=request.form.get('geotag')
                    if ( get1== 'tif' and geotag=="1"):
                        print("it is a tiff image")
                        resp=func1(image,'FP')
                        return resp

                    elif( get1=="jpg" and geotag=="0"):
                        print("it is a jpg")
                        resp=func2(image,'FP')
                        return resp
                else:
                    resp.status_code = 400
                    return resp
             else:
                 resp.status_code = 400
                 return resp
        else:
            resp.status_code = 400
            #print(e)
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        print(e)
        return resp




@app.route('/satellite_VEG/',methods=['POST'])
def VEG():
    print("Welcome to satellite image segmentation-VEGETATION:")
    resp = Response(status=200, content_type='application/json')
    image = request.files['file']  # Single image path
    # image = request.files.get('file', '')
    # image.save('/home/ceinfo/Desktop/testing/test_image1.jpg')

    try:
        if (request.content_type != None):
            if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1 = image.filename
                    get1 = get1[-3:]
                    geotag = request.form.get('geotag')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image, 'VG')
                        return resp

                    elif (get1 == "jpg" and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'VG')
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            # print(e)
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        print(e)
        return resp



@app.route('/satellite_SOIL/',methods=['POST'])
def Soil():
    resp = Response(status=200, content_type='application/json')

    # try:
    image = request.files['file']  # Single image path
    print(image)

    try:
        if (request.content_type != None):
            if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1 = image.filename
                    get1 = get1[-3:]
                    geotag = request.form.get('geotag')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image, 'S')
                        return resp

                    elif (get1 == "jpg" and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'S')
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            # print(e)
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        print(e)
        return resp



@app.route('/satellite_RD/',methods=['POST'])
def roads():
    print("welcome to satellite image segmentation")
    resp = Response(status=200, content_type='application/json')

    # try:
    image = request.files['file']  # Single image path

    try:
        if (request.content_type != None):
            if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1 = image.filename
                    get1 = get1[-3:]
                    geotag = request.form.get('geotag')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image,'RD')
                        return resp

                    elif (get1 == "jpg" and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image,'RD')
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            # print(e)
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        print(e)
        return resp




















@app.route('/satellite_WATER/',methods=['POST'])
def water():

        resp = Response(status=200, content_type='application/json')

        #try:
        image = request.files['file']  # Single image path

        try:
            if (request.content_type != None):
                if request.content_type.startswith('multipart/form-data'):
                    if 'file' and 'geotag' in request.form.keys():
                        get1 = image.filename
                        get1 = get1[-3:]
                        geotag = request.form.get('geotag')
                        if (get1 == 'tif' and geotag == "1"):
                            print("it is a tiff image")
                            resp = func1(image, 'W')
                            return resp

                        elif (get1 == "jpg" and geotag == "0"):
                            print("it is a jpg")
                            resp = func2(image, 'W')
                            return resp
                    else:
                        resp.status_code = 400
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                # print(e)
                return resp
        except Exception as e:
            logger.error(msg=str(e), status_code=500)
            resp.status_code = 500
            print(e)
            return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=False)