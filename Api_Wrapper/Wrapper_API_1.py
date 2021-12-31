import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
# import io as python_io
# import numpy as np
from flask import Flask, request, jsonify,Response
# from flask_cors import CORS
import json
import logging
import traceback
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
from datetime import datetime
import requests
import warnings
from skimage import io
import cv2
import numpy as np
from PIL import Image
import flask
from flask import render_template, json, jsonify, request
import numpy as np
import cv2
# import tensorflow.python.util.deprecation as deprecation
# deprecation._PRINT_DEPRECATION_WARNINGS = False
# from gunicorn.glogging import Logger
# logging.getLogger("tensorflow.error").setLevel(logging.ERROR)
app = Flask(__name__)

if(os.path.exists('./Logs')):
    os.makedirs('./Logs', exist_ok=True)
logger = logging.getLogger('gunicorn.workers')

# logger = logging.getLogger('gunicorn')
# logger = logging.getLogger('__name__')
log_filename = datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/' + log_filename, when='MIDNIGHT', backupCount=7)
formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger.setLevel(logger.level)
# app.logger.handlers = logger.handlers
# app.logger.setLevel(logger.level)
handler.setLevel(logging.INFO)
# handler.setStream(logging.StreamHandler)
handler.setFormatter(formatter)

# logger.setLevel(logging.INFO)
logger.addHandler(handler)

logger.propagate = False

@app.route('/Satellite_Segmentation_FP', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def wrap_FP():
    print('calling1')
    image = request.files['file']
    print(type(image))
    #if request.method == 'POST' and 'file' in request.files:
    #photo = request.files['photo']
    in_memory_file = io.BytesIO()
    image.save(in_memory_file)
    data = np.fromstring(in_memory_file.getvalue(), dtype=np.uint8)
    color_image_flag = 1
    img = cv2.imdecode(data, color_image_flag)
    print(type(img))
    '''to read image from postman in bgr fotmat'''
    print("going to read image")
    #image_name_bgr = io.imread(image)

    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    #image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    #status = cv2.imwrite("/mnt/vol1/Dhruv/1111.jpg", image_name_rgb)
    #print("Image written to file-system : ", status)

    #FileStream file = newFileStream("/mnt/vol1/Dhruv/1111.jpg", FileMode.Open)
    #img=image.open("/mnt/vol1/Dhruv/1111.jpg")
    #img= Image.open("/mnt/vol1/Dhruv/1111.jpg")

    # read image file string data
    #filestr = request.files['file'].read()
    #file = request.files['image']

    #filestr = file.read()

    # convert string data to numpy array
    #npimg = numpy.fromstring(filestr, numpy.uint8)
    #img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

    # convert numpy array to image
    from PIL import Image as im

    #img=im.fromarray(npimg)
    #print(type(img))
    # if 'file' not in request.files:
          #  errors.append({'file': 'please provide file'})
    resp = Response(status=200, mimetype='application/json',content_type='application/json')
    try:
        if(request.content_type!=None):
            print('calling2')
            if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    #file = request.files['file']
                    #print(file)
                    geotag=request.form.get('geotag')
                    print(geotag)
                    #get1 = file.filename
                    # get1 = get1[-3:]
                    # image_name_BGR = io.imread(file)
                    # image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                    # status = cv2.imwrite('/home/ceinfo/Desktop/image_10/1111.jpg', image_name_RGB)

                    #print(file)
                    #print(geotag)
                    if(image!=None):
                        print('calling3')
                        API_ENDPOINT = "http://10.10.21.120:7005/satellite_FP/"
                        print('calling4')
                        # data to be sent to api
                        data = {'file':[img],'geotag': [1]}

                        print(data)
                        print(type(data))
                        print('calling5')

                        # import json
                        # import urllib2
                        #
                        # data = {
                        #     'files': [12, 3, 4, 5, 6]
                        # }
                        #
                        # req = urllib2.Request('http://example.com/api/posts/create')
                        # req.add_header('Content-Type', 'application/json')
                        #
                        # response = urllib2.urlopen(req, json.dumps(data))
                        # sending post request and saving response as response object
                        r = requests.post(url=API_ENDPOINT, data=data.tostring)
                        #response = requests.post(test_url, data=img_encoded.tostring(), headers=headers)

                        #r = requests.get(url=API_ENDPOINT, data=data)
                        #print(r.text)
                        print(r.text)
                        print(r.json)
                    return r
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        return resp


@app.route('/Satellite_Segmentation_RD', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def wrap_RD():
    print('calling2')

    # if 'file' not in request.files:
          #  errors.append({'file': 'please provide file'})
    resp = Response(status=200, mimetype='application/json',content_type='application/json')
    try:
        if(request.content_type!=None):
            print('calling2')
            if request.content_type.startswith('multipart/form-data'):
                if 'file' in request.files.keys():
                    file = request.files['file']
                    geotag=request.args.get('geotag')
                    # get1 = file.filename
                    # get1 = get1[-3:]
                    image_name_BGR = io.imread(file)
                    image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                    # status = cv2.imwrite('/home/ceinfo/Desktop/image_10/1111.jpg', image_name_RGB)
                    print('calling1')
                    print(file)
                    print(geotag)
                    if(file!=None):
                        print('calling')
                        # return'Hi'
                        API_ENDPOINT = "http://10.10.21.159:7005/satellite_RD/"

                        # data to be sent to api
                        data = {'file':image_name_RGB,'geotag': 1}

                        # sending post request and saving response as response object
                        r = requests.post(url=API_ENDPOINT, data=data)
                        print(r.text)
                    return 'Hello'
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        return resp

@app.route('/Satellite_Segmentation_Soil', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def wrap_Soil():
    print('calling2')

    # if 'file' not in request.files:
          #  errors.append({'file': 'please provide file'})
    resp = Response(status=200, mimetype='application/json',content_type='application/json')
    try:
        if(request.content_type!=None):
            print('calling2')
            if request.content_type.startswith('multipart/form-data'):
                if 'file' in request.files.keys():
                    file = request.files['file']
                    geotag=request.args.get('geotag')
                    # get1 = file.filename
                    # get1 = get1[-3:]
                    image_name_BGR = io.imread(file)
                    image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                    # status = cv2.imwrite('/home/ceinfo/Desktop/image_10/1111.jpg', image_name_RGB)
                    print('calling1')
                    print(file)
                    print(geotag)
                    if(file!=None):
                        print('calling')
                        # return'Hi'
                        API_ENDPOINT = "http://10.10.21.159:7005/satellite_Soil/"

                        # data to be sent to api
                        data = {'file':image_name_RGB,'geotag': 1}

                        # sending post request and saving response as response object
                        r = requests.post(url=API_ENDPOINT, data=data)
                        print(r.text)
                    return 'Hello'
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        return resp

@app.route('/Satellite_Segmentation_VEG', methods=['POST'])
# @cross_origin(headers=["Content-Type", "Authorization"])
def wrap_Veg():
    print('calling2')

    # if 'file' not in request.files:
          #  errors.append({'file': 'please provide file'})
    resp = Response(status=200, mimetype='application/json',content_type='application/json')
    try:
        if(request.content_type!=None):
            print('calling2')
            if request.content_type.startswith('multipart/form-data'):
                if 'file' in request.files.keys():
                    file = request.files['file']
                    geotag=request.args.get('geotag')
                    # get1 = file.filename
                    # get1 = get1[-3:]
                    image_name_BGR = io.imread(file)
                    image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                    # status = cv2.imwrite('/home/ceinfo/Desktop/image_10/1111.jpg', image_name_RGB)
                    print('calling1')
                    print(file)
                    print(geotag)
                    if(file!=None):
                        print('calling')
                        # return'Hi'
                        API_ENDPOINT = "http://10.10.21.159:7005/satellite_VEG/"

                        # data to be sent to api
                        data = {'file':image_name_RGB,'geotag': 1}

                        # sending post request and saving response as response object
                        r = requests.post(url=API_ENDPOINT, data=data)
                        print(r.text)
                    return 'Hello'
                else:
                    resp.status_code = 400
                    return resp
            else:
                resp.status_code = 400
                return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
