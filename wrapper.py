import json
from datetime import datetime
from flask import Flask, request,Response
app = Flask(__name__)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import io
from skimage import io
from api_deploy.geotiff import gdal_convert
# from geotiff import gdal_convert_1
from api_deploy.pixel_to_lat_lon import *
from api_deploy.predict01 import *
from api_deploy.FP_pixel import *
# from datetime import datetime
from tensorflow import keras

import os, time, sys
# import requests
# import io
from skimage import io
from flask import Flask, request, Response
app = Flask(__name__)
import os


try:
     model,graph=read_model()
     model1,graph1 = read_model_Rd()

except Exception as e:
     print(e)


@app.route('/satellite_FP_1/', methods=['POST'])
def satellite_FP_1():

    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():
            #print(request)




            static_file = request.files['file']

            filename = static_file.filename

            content_type = static_file.content_type



            '''======================'''


            image = request.files['file']  # Single image path
            print(image)
            geotag = request.form.get('geotag')
            scale = int(request.form.get('scale'))
            print('start', datetime.datetime.now())
            print("geotag :", geotag, "scale :", scale)
            if (geotag == "2" and ('bounds' in request.form.keys())):
                print('func 3')
                bounds = eval(request.form.get('bounds'))
                print(bounds)

                '''------------------------------'''
                path = os.getcwd()
                print(path)
                directory = "uploads04"
                parent_dir = path
                path1 = os.path.join(parent_dir, directory)
                print(path1)

                '''----------------------------------------------------------------------------------------'''

                '''automatic deletes the output folder after a day'''
                # automatic_deletion()

                '''----------------------------------------------------------------------------------------'''

                try:
                  os.makedirs(path1, exist_ok=True)
                except OSError as error:
                     pass
                # in_file=image.filename[:-4]
                in_file = image.filename.split('.')[0] + str(datetime.datetime.now())
                print(in_file)
                in_file = in_file.replace('.', '_').replace(' ', '_')
                # print(in_file)

                image_name = in_file

                # print("going to read image")
                image_name_bgr = io.imread(image)

                image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
                status = cv2.imwrite(path1 + "/" + in_file + ".jpg", image_name_rgb)
                # print("Image written to file-system : ", status)
                # print(datetime.datetime.now())

                '''prediction : mask will be generated:'''
                # print("going to start prediction")
                key="FP"
                if key == "FP" and scale <= 100:

                    '''old mask'''
                    mask = predict01(path1, model, image_name, graph, (512, 512))
                    # print("prediction done : masks created")

                    '''..............post processing on mask ......................'''
                    '''Image path'''
                    image_path = path1 + "/" + in_file + '.jpg'
                    # print("image path")

                    '''mask path'''
                    mask_path = path1 + "/" + in_file + '_mask.png'
                    # print(mask_path)
                    mask = postprocessing(image_path, mask_path, path1, in_file)
                    print(datetime.datetime.now())

                elif key == "FP" and scale > 100:
                    mask = predict_fp_pixel(path1, image_name)
                    # print("prediction done : masks created")
                    print(datetime.datetime.now())

                elif key == 'RD':
                    mask = predict_RD(path1, model1, image_name, graph1, (256, 256))
                    # print(" prediction done: road masks created")

                '''------------------------------'''

            '''======================'''


            url = 'http://10.10.21.120:7007/satellite_FP/'

            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"]= request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)
            headers = {}
            filename1 = filename.split('.')[1]
            filename1 = filename1.lower()
            print('file', filename1)
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Somethin;g went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"]= request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads('{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500

        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500


@app.route('/satellite_RD_1', methods=['GET', 'POST'])
def satellite_RD_1():
    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():

            static_file = request.files['file']
            filename = static_file.filename
            content_type = static_file.content_type
            url = 'http://10.10.21.228:7007/satellite_RD/'
            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"] = request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)

            headers = {}
            filename1 = filename.split('.')[1]
            filename1 = filename1.lower()
            print('file', filename1)
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"]= request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads('{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500


        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500


@app.route('/satellite_VEG_1', methods=['GET', 'POST'])
def satellite_VEG_1():
    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type'in request.form.keys():

            static_file = request.files['file']
            filename = static_file.filename
            content_type = static_file.content_type
            url = 'http://10.10.21.228:7006/satellite_VEG/'
            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"] = request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)

            headers = {}
            filename1 = filename.split('.')[1]
            filename1 = filename1.lower()
            print('file', filename1)
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"]= request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads('{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500

        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500


@app.route('/satellite_SOIL_1', methods=['GET', 'POST'])
def satellite_Soil_1():
    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():

            static_file = request.files['file']
            filename = static_file.filename
            content_type = static_file.content_type
            url = 'http://10.10.21.228:7006/satellite_SOIL/'
            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"] = request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)

            headers = {}
            filename1 = filename.split('.')[1]
            filename1 = filename1.lower()
            print('file', filename1)
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"] = request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads(
                            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500

        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500


@app.route('/satellite_WATER_1', methods=['GET', 'POST'])
def satellite_Water_1():
    print('1')
    values = {}
    if request.method == 'POST':
        if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():
            print('in')
            static_file = request.files['file']
            filename = static_file.filename
            content_type = static_file.content_type
            url = 'http://10.10.21.120:228/satellite_WATER/'
            files = [('file', (filename, static_file.read(), content_type))]
            values["geotag"] = request.form['geotag']
            values["scale"] = request.form['scale']
            values["img_type"] = request.form['img_type']
            print(values)

            headers = {}
            filename1 = filename.split('.')[1]

            print('file', filename1)
            filename1=filename1.lower()
            if (filename1 == "tiff" or filename1 == "tif") and values["geotag"] == "1" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)
                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "0" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                r = requests.request("POST", url, files=files, data=values, headers=headers)
                if r.status_code == 200:
                    return json.loads(r.text)

                else:
                    return json.loads(
                        '{"error": "Something went wrong while processing image", "status_code": 500}'), 500

            elif (filename1 == "jpg" or filename1 == "jpeg" or filename1 == "png") and values["geotag"] == "2" and int(values["scale"])>0 and values["img_type"] in ["bhuwan", "google"]:
                if 'bounds' in request.form.keys():
                    values["bounds"] = request.form['bounds']
                    r = requests.request("POST", url, files=files, data=values, headers=headers)
                    if r.status_code == 200:
                        return json.loads(r.text)
                    else:
                        return json.loads(
                            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500
                else:
                    return json.loads(
                        '{"error": "Image Bounds Required", "status_code": 500}'), 500
            else:
                return json.loads('{"error": "Invalid parameter values", "status_code": 500}'), 500

        else:
            return json.loads('{"error": "Invalid Inputs parameters", "status_code": 500}'), 500





if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=False)