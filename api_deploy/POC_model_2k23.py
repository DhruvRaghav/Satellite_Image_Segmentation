import requests
from flask import Flask, request,Response
app = Flask(__name__)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import io
from skimage import io
from geotiff import gdal_convert
# from geotiff import gdal_convert_1
from pixel_to_lat_lon import *
from predict01 import *
from FP_pixel import *
# from datetime import datetime
from tensorflow import keras

import os, time, sys
from geotiff import *
''' convert extensions'''
'''for f in *.tif; do mv -- "$f" "${f%.tif}.tiff"; done'''


if not (os.path.exists('Logs')):
    os.makedirs('Logs/',exist_ok=False)
log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/'+log_filename, when='MIDNIGHT', backupCount=7)

formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

logger = logging.getLogger('gunicorn.error')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logger.level)
logger.addHandler(handler)

logger.propagate = False


try:
     model,graph=read_model()
     model1,graph1 = read_model_Rd()

except Exception as e:
     print(e)
     logger.error(msg="model is not loaded")


if tf.test.gpu_device_name():
    print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))
else:
   print("Please install GPU version of TF")

'''----------------------------------------------------------------------'''


def automatic_deletion():

    path = "/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/"
    now = time.time()
    # print(now)
    for f in os.listdir(path):
        # print(f)
        f = os.path.join(path, f)

        if os.stat(f).st_mtime < now - (1 * 60):
            if os.path.isfile(f):
                os.remove(os.path.join(path, f))

def func3(image,bounds,key, scale):
    path = os.getcwd()
    print(path)
    directory = "uploads03"
    parent_dir = path
    path1 = os.path.join(parent_dir, directory)

    '''----------------------------------------------------------------------------------------'''
    '''automatic deletes the output folder after a day'''
    automatic_deletion()

    '''----------------------------------------------------------------------------------------'''

    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    # in_file=image.filename[:-4]
    in_file=image.filename.split('.')[0]+str(datetime.datetime.now())
    in_file=in_file.replace('.','_').replace(' ','_')
    # print(in_file)

    image_name = in_file


    # print("going to read image")
    image_name_bgr = io.imread(image)


    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)
    # print(datetime.datetime.now())

    '''prediction : mask will be generated:'''
   # print("going to start prediction")
    values = {}

    if key=="FP" and scale <=100:

        '''old mask'''
        mask = predict01(path1,model, image_name, graph, (512, 512))
        print("prediction done : masks created")

        '''..............post processing on mask ......................'''
        '''Image path'''
        image_path =path1+"/"+in_file+'.jpg'
        # print("image path")

        '''mask path'''
        mask_path=  path1+"/"+in_file+'_mask.png'
        mask =  postprocessing(image_path, mask_path,path1,in_file,bounds)
       # print(datetime.datetime.now())


        # url = 'http://10.10.21.159:5002/satellite_FP_1/'

    elif key=="FP" and scale >100:
        mask = predict_fp_pixel(path1,image_name,bounds)
        # print("prediction done : masks created")
        #print(datetime.datetime.now())

    elif key=='RD':
        mask = predict_RD(path1,model1, image_name, graph1, (256, 256),bounds)
        # print(" prediction done: road masks created")


    static_file = request.files['file']

    filename = static_file.filename

    content_type = static_file.content_type


    mask_1 = json.loads(mask)
    # os.remove(path1+"/"+in_file+'_mask.png')
    # os.remove(path1+"/"+in_file+'jpg')


    url = 'http://10.10.21.159:7005/satellite_model/'
    files = [('file', (filename, static_file.read(), content_type)), ('mask', mask),('image',mask_1["I M A G E"])]
    #print("files", files)
    values["geotag"] = request.form['geotag']
    #print("geotag", values)
    values["scale"] = request.form['scale']
    values["img_type"] = request.form['img_type']
    values["mask"] = mask_1["M A S K"]

    values["image"]=mask_1["I M A G E"]
    values["d"]=mask


    #print("mask", values)
    #print(values)
    headers = {}
    r = requests.request("POST", url, files=files, data=values, headers=headers)
    if r.status_code == 200:

        return json.loads(r.text)
    else:
        return json.loads(
            '{"error": "Something went wrong while processing image", "status_code": 500}'), 500



'''----------------------------------------------------------------------'''
# path1
def func2(image,key,scale):

    path = os.getcwd()
    directory = "uploads01"
    parent_dir = path

    path1 = os.path.join(parent_dir, directory)

    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    # in_file=image.filename[:-4]
    in_file=image.filename.split('.')[0]+str(datetime.datetime.now())
    #print(in_file)

    image_name = in_file


    print("going to read image")
    image_name_bgr = io.imread(image)



    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)

    if key == "FP" and scale <= 100:
        mask = predict01(path1, model, image_name, graph, (512, 512))
        print("prediction done : masks created")
        print(datetime.datetime.now())

    elif key == "FP" and scale > 100:
        mask = predict_fp_pixel(path1, image_name)
        print("prediction done : masks created")
        print(datetime.datetime.now())

    elif key=='RD':
        mask = predict_RD(path1,model1, image_name, graph1, (256, 256))
        print(" prediction done: road masks created")

    resp = geojson2(path1,image_name)
    # print("geojson created at the location you mentioned")
    # print(resp)
    return resp


'''----------------------------------------------------------------------'''

def func1(image,key,scale):
    path = os.getcwd()
    print("The current working directory is %s" % path)

    print("creating a new directory now:")
    directory = "uploads2"

    parent_dir = path

    path1 = os.path.join(parent_dir, directory)
    try:

        os.makedirs(path1, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    in_file = image.filename[:-4]
    print(in_file)
    print(type(image))
    # in_files = os.path.join(path,in_file + '.jpg')
    image_name = in_file+str(datetime.datetime.now())
    image.save(path1 + "/" + in_file + ".jpeg")



    if key == "FP" and scale <= 100:
        mask = predict_FP_Tif_PL(path1, model, in_file, graph, (512, 512))
        print("prediction done : masks created")
        print(datetime.datetime.now())

    elif key == "FP" and scale > 100:
        mask = predict_fp_pixel_tif(path1, in_file)
        print("prediction done : masks created")
        print(datetime.datetime.now())

    if key=="RD":
        mask = predict_RD_Tif_PL(path1,model1, in_file, graph1, (256, 256))
        print("mask created at the mentioned location")

    resp = geojson(path1,in_file)
    return resp





'''----------------------------------------------------------------------'''

@app.route('/satellite_FP/',methods=['POST'])  # Single Api
def FP():
    print ("Welcome to satellite image segmentation")
    resp=Response(status=200,content_type='application/json')
    image = request.files['file']  # Single image path
    #print(image)
    geotag = request.form.get('geotag')
    scale = int(request.form.get('scale'))
    # print('start',datetime.datetime.now())
    # print("geotag :",geotag,"\nscale :",scale)


    try:
        print("hello")
        if(request.content_type!=None):
             if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' and 'scale' in request.form.keys():

                    get1=image.filename.split('.')[1]
                    # print("file name : ", get1)


                    geotag=request.form.get('geotag')
                    if ( get1== 'tif' and geotag=="1"):
                        # print("it is a tiff image")
                        resp=func1(image,'FP', scale)
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        resp = func2(image, 'FP', scale)
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        # print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        # print(bounds)

                        resp = func3(image, bounds, 'FP', scale)
                        return resp
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
        print(e)

        return resp



'''----------------------------------------------------------------------'''
@app.route('/satellite_RD/',methods=['POST'])
def roads():
    print("welcome to satellite image segmentation")
    resp = Response(status=200, content_type='application/json')

    image = request.files['file']  # Single image path

    try:
        if (request.content_type != None):
            if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1 = image.filename
                    get1=image.filename.split('.')[1]
                    geotag = request.form.get('geotag')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image,'RD', 0)
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'RD', 0)
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'RD', 0)
                        return resp
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
        logger.error(msg=str(e), status_code=500)
        resp.status_code = 500
        print(e)
        return resp



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7007, debug=False)




'------------------------------------------------------------'

'''TO kill the process running on different ports'''
'------------------------------------------------------------'

"sudo kill -9 $(sudo lsof -t -i:portnumber)"

'------------------------------------------------------------'