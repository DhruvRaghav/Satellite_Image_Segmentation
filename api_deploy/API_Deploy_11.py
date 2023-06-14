import traceback
from flask import Flask, request,Response
from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
# from keras.models import load_model
# import detect_batch_old
# import detect_blur
import json
import geoio
from api_deploy.geotiff import gdal_convert
import os
from api_deploy.pixel_to_lat_lon import geojson
from api_deploy.predict import predict,read_model,read_model_Rd
from api_deploy.vegetation import predict_veg
from api_deploy.Soil import predict_soil
from api_deploy.Ocean import predict_water,predict_water1
import tensorflow as tf
#from api_deploy.predict import *
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

app = Flask(__name__)


try:
    model,graph=read_model()
    model1,graph1 = read_model_Rd()
    # model1,graph1=read_model("/mnt/vol1/Deployment_projects/satellite_image_segmentation/roadnet_models/83.h5")
    # global graph
    # graph=tf.get_default_graph()
    #model = load_model("/mnt/vol1/Deployment_projects/satellite_image_segmentation/45.h5",custom_objects={'jaccard_coef_loss': jaccard_coef_loss,
                                                                    # 'jaccard_coef_int': jaccard_coef_int,
                                                                     #'jaccard_coef': jaccard_coef},compile=False)
except Exception as e:
    print(e)
    logger.error(msg="model is not loaded")

@app.route('/satellite_FP',methods=['POST'])  # Single Api
def FP():
    # print ("Welcome to License Plate Detection")
    resp=Response(status=200,content_type='application/json')

    # try:
    # image = request.files['file']  # Single image path


    try:
        if(request.content_type!=None):
            # if request.content_type.startswith('multipart/form-data'):
                if 'southwest'and 'northeast'and'name' and 'bounds' in request.form.keys():
                        # results = model.detect_licenseplates(image)
                        # southwest=request.form.get('southwest')[7:-1].split(',')
                        # northeast=request.form.get('northeast')[7:-1].split(',')
                        bounds=eval(request.form.get('bounds'))
                        sw_lat=bounds['_southWest']['lat']
                        sw_long=bounds['_southWest']['lng']
                        ne_lat = bounds['_northEast']['lat']
                        ne_long = bounds['_northEast']['lng']
                        southwest=[str(sw_lat),str(sw_long)]
                        northeast=[str(ne_lat),str(ne_long)]
                        print(bounds)
                        image_name=request.form.get('name')
                        # resp={'1':[southwest,northeast]}
                        print(southwest,northeast,image_name)
                        exce=gdal_convert(image_name,southwest,northeast)
                        print(exce)
                        if exce is not None:
                            # raise FileNotFoundError
                            resp.status_code = 400
                            return resp
                        mask=predict(model,image_name,graph,(512,512))
                        resp=geojson(image_name)
                        # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                        # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                        return resp
                else:
                    resp.status_code = 400
                    return resp
            # else:
            #     resp.status_code = 400
            #     return resp
        else:
            resp.status_code = 400
            print(e)
            return resp
    except Exception as e:
        logger.error(msg=str(e),status_code=500)
        resp.status_code=500
        print(e)
        return resp

    # if(image==None):
    #     response.status_code=400
    #     return response
    # try:
    #     results=model.detect_licenseplates(image)
    #     response=json.dumps({'Predictions':[{'x1':i[0],'y1':i[1],'x2':i[2],'y2':i[3]} for i in results]})
    #     return response
    # except Exception as e:
    #     logger.error(msg=str(e)+'\tTraceback\t' + '~'.join(str(traceback.format_exc()).split('\n')))
    #     response.status_code=500
    #     return response


# @app.route('/satellite_FP',methods=['POST'])  # Single Api
# def FP():
#     resp = Response(status=200, content_type='application/json')
#
#     # try:
#     # image = request.files['file']  # Single image path
#
#     try:
#         if (request.content_type != None):
#             # if request.content_type.startswith('multipart/form-data'):
#             if 'southwest' and 'northeast' and 'name' in request.form.keys():
#                 # results = model.detect_licenseplates(image)
#                 southwest = request.form.get('southwest')[7:-1].split(',')
#                 northeast = request.form.get('northeast')[7:-1].split(',')
#                 image_name = request.form.get('name')
#                 resp = {'1': [southwest, northeast]}
#                 print(southwest, northeast, image_name)
#                 gdal_convert(image_name, southwest, northeast)
#                 mask = veg_2(image_name)
#                 resp = geojson(image_name)
#                 # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
#                 # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
#                 return resp
#             else:
#                 resp.status_code = 400
#                 return resp
#         # else:
#         #     resp.status_code = 400
#         #     return resp
#         else:
#             resp.status_code = 400
#             return resp
#     except Exception as e:
#         logger.error(msg=str(e), status_code=500)
#         resp.status_code = 500
#         return resp




@app.route('/satellite_VEG',methods=['POST'])
def VEG():
    resp = Response(status=200, content_type='application/json')

    # try:
    # image = request.files['file']  # Single image path

    try:
        if (request.content_type != None):
            # if request.content_type.startswith('multipart/form-data'):
            if 'southwest' and 'northeast' and 'name' in request.form.keys():
                # results = model.detect_licenseplates(image)
                southwest = request.form.get('southwest')[7:-1].split(',')
                northeast = request.form.get('northeast')[7:-1].split(',')
                image_name = request.form.get('name')
                resp = {'1': [southwest, northeast]}
                print(southwest, northeast, image_name)
                gdal_convert(image_name, southwest, northeast)
                mask=predict_veg(image_name)
                resp = geojson(image_name)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                return resp
            else:
                resp.status_code = 400
                return resp
        # else:
        #     resp.status_code = 400
        #     return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        return resp


@app.route('/satellite_SOIL',methods=['POST'])
def Soil():
    resp = Response(status=200, content_type='application/json')

    # try:
    # image = request.files['file']  # Single image path
    try:
        if (request.content_type != None):
            # if request.content_type.startswith('multipart/form-data'):
            if 'southwest' and 'northeast' and 'name' in request.form.keys():
                # results = model.detect_licenseplates(image)
                southwest = request.form.get('southwest')[7:-1].split(',')
                northeast = request.form.get('northeast')[7:-1].split(',')
                image_name = request.form.get('name')
                resp = {'1': [southwest, northeast]}
                print(southwest, northeast, image_name)
                gdal_convert(image_name, southwest, northeast)
                mask=predict_soil(image_name)
                resp = geojson(image_name,mask)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                return resp
            else:
                resp.status_code = 400
                return resp
        # else:
        #     resp.status_code = 400
        #     return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        return resp


@app.route('/satellite_RD',methods=['POST'])
def roads():
    resp = Response(status=200, content_type='application/json')

    # try:
    # image = request.files['file']  # Single image path

    try:
        if (request.content_type != None):
            # if request.content_type.startswith('multipart/form-data'):
            if 'southwest' and 'northeast' and 'name' and 'bounds' in request.form.keys():
                # results = model.detect_licenseplates(image)
                southwest = request.form.get('southwest')[7:-1].split(',')
                northeast = request.form.get('northeast')[7:-1].split(',')
                bounds = eval(request.form.get('bounds'))
                sw_lat = bounds['_southWest']['lat']
                sw_long = bounds['_southWest']['lng']
                ne_lat = bounds['_northEast']['lat']
                ne_long = bounds['_northEast']['lng']
                southwest = [str(sw_lat), str(sw_long)]
                northeast = [str(ne_lat), str(ne_long)]
                print(bounds)
                image_name = request.form.get('name')
                # resp={'1':[southwest,northeast]}
                print(southwest, northeast, image_name)
                exce = gdal_convert(image_name, southwest, northeast)
                if exce is not None:
                    # raise FileNotFoundError
                    resp.status_code = 400
                    return resp
                mask = predict_RD(model1, image_name, graph1,(256,256))
                # resp = geojson(image_name, mask)
                resp = geojson(image_name)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                return resp
            else:
                resp.status_code = 400
                return resp
        # else:
        #     resp.status_code = 400
        #     return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        return resp


@app.route('/satellite_water',methods=['POST'])
def water():

    resp = Response(status=200, content_type='application/json')

    # try:
    # image = request.files['file']  # Single image path

    try:
        if (request.content_type != None):
            # if request.content_type.startswith('multipart/form-data'):
            if 'southwest' and 'northeast' and 'name' in request.form.keys():
                # results = model.detect_licenseplates(image)
                southwest = request.form.get('southwest')[7:-1].split(',')
                northeast = request.form.get('northeast')[7:-1].split(',')
                image_name = request.form.get('name')
                resp = {'1': [southwest, northeast]}
                print(southwest, northeast, image_name)
                gdal_convert(image_name, southwest, northeast)
                mask=predict_water(image_name)
                resp = geojson(image_name,mask)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                return resp
            else:
                resp.status_code = 400
                return resp
        # else:
        #     resp.status_code = 400
        #     return resp
        else:
            resp.status_code = 400
            return resp
    except Exception as e:
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=False)