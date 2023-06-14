from flask import Flask, request,Response
app = Flask(__name__)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import io
from skimage import io
from api_deploy.geotiff import gdal_convert
from api_deploy.pixel_to_lat_lon import *
from api_deploy.Soil import *
from api_deploy.Water_bodies import *
from api_deploy.geotiff import  *
from api_deploy.vegetation import *


if not (os.path.exists('Logs')):
    os.makedirs('Logs/',exist_ok=False)
log_filename = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
handler = TimedRotatingFileHandler('Logs/'+log_filename, when='MIDNIGHT', backupCount=7)

formatter = Formatter(fmt='%(asctime)s %(name)-12s %(levelname)-8s %(message)s', datefmt='%d-%m-%Y %I:%M:%S %p')

# logger = logging.getLogger('werkzeug')
logger = logging.getLogger('gunicorn.error')

handler.setLevel(logging.INFO)
handler.setFormatter(formatter)

logger.setLevel(logger.level)
logger.addHandler(handler)

logger.propagate = False


'''................... third function: takes jpg, bounds, geotag :2 --------------------------------------------------'''

def func3(image,bounds,key , scale, img_type):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''
    path = os.getcwd()
    scale=int(scale)
    '''Directory'''
    directory = "uploads03"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    '''image name without extension'''
    # in_file=image.filename[:-4]
    in_file=image.filename.split('.')[0]+str(datetime.datetime.now())
    in_file_ex = image.filename.split('.')[-1]
    in_file=in_file.replace('.','_').replace(' ','_')
    print("file",in_file)

    image_name = in_file


    '''to read image from postman in bgr fotmat'''
    # print("going to read image")
    image_name_bgr = io.imread(image)



    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)
    print(datetime.datetime.now())
    '''prediction : mask will be generated:'''
    # print("going to start prediction")
    if key =="VG":
        mask = predict_veg(path1,image_name)
        print(" prediction done: Vegetation masks created")
    elif key=="S":
        mask = predict_soil(path1,image_name)
    elif key=="W":
        if img_type=='google' and scale>0 and scale<=100:
            google_50_100(path1, image_name)
        elif img_type=='google' and scale>=200:
            google_200(path1, image_name)
        elif img_type=='bhuwan' and scale<=50:
            bhuwan_50(path1, image_name)
        elif img_type == 'bhuwan' and scale >= 100 and scale <=200 :
            bhuwan_100_200(path1, image_name)
        elif img_type=='bhuwan' and scale>=300:
            bhuwan_300(path1, image_name)

    sw_lat = bounds['_southWest']['lat']
    sw_long = bounds['_southWest']['lng']
    ne_lat = bounds['_northEast']['lat']
    ne_long = bounds['_northEast']['lng']
    southwest = [str(sw_lat), str(sw_long)]
    northeast = [str(ne_lat), str(ne_long)]
    exce = gdal_convert(path1,in_file, southwest, northeast)
    print('tiff',datetime.datetime.now())
    '''To create the goejson file use this function'''
    resp = geojson5(path1,in_file)
    # os.remove(path1 + "/" + in_file + '_mask.png')
    # os.remove(path1 + "/" + in_file + '.jpg')
    # os.remove(path1 + "/" + in_file + '.jpg')
    # os.remove(path1 + "/" + in_file + '.tif')
    return resp

'''----------------------------------------------------------------------------------------'''

'''.....................building footprints two function : -------func1 and func2----------'''

def func2(image,key , scale, img_type):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN JPG FORM  & GEOTAG : 0 '''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads02"
    '''Parent Directory path'''
    parent_dir = path
    ''' Path'''
    path1 = os.path.join(parent_dir, directory)

    '''Directory will be created at the current location of the project'''
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    '''image name without extension'''
    # in_file=image.filename[:-4]
    in_file=image.filename.split('.')[0]+str(datetime.datetime.now())
    #print(in_file)
    image_name = in_file
    '''to read image from postman in bgr fotmat'''
    print("going to read image")
    image_name_bgr = io.imread(image)
    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)

    '''prediction : mask will be generated:'''
    # print("going to start prediction")
    if key =="VG":
        mask = predict_veg(path1,image_name)
        print(" prediction done: Vegetation masks created")
    elif key=="S":
        mask = predict_soil(path1,image_name)
    elif key=="W":
        if img_type=='google' and scale>0 and scale<=100:
            google_50_100(path1, image_name)
        elif img_type=='google' and scale>=200:
            google_200(path1, image_name)
        elif img_type=='bhuwan' and scale<=50:
            bhuwan_50(path1, image_name)
        elif img_type == 'bhuwan' and scale > 50 and scale <=200 :
            bhuwan_100_200(path1, image_name)
        elif img_type=='bhuwan' and scale>=300:
            bhuwan_300(path1, image_name)

    '''To create the goejson file use this function'''
    resp = geojson2(path1,image_name)
    # print("geojson created at the location you mentioned")
    print(resp)
    return resp


'''-------------------------------------------------------------------------------------'''

def func1(image,key, scale, img_type):
    path = os.getcwd()
    print("The current working directory is %s" % path)

    print("creating a new directory now:")
    # Directory
    directory = "uploads01"

    # Parent Directory path
    parent_dir = path

    # Path
    path1 = os.path.join(parent_dir, directory)
    # print(path1)
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


    '''to make the jpg from tiff file'''
    print("going to start prediction")

    if key =="VG":
        mask = predict_veg_Tif_PL(path1,image_name)
        print(" prediction done: Vegetation masks created")
    elif key=="S":
        mask = predict_soil_Tif_PL(path1,image_name)
    elif key=="W":
        ''' different input for water to fetch different results scale wise'''
        if img_type=='google' and scale>=0 and scale<=100:
            google_50_100(path1, image_name)
        elif img_type=='google' and scale>=200:
            google_200(path1, image_name)
        elif img_type=='bhuwan' and scale<=50:
            bhuwan_50(path1, image_name)
        elif img_type == 'bhuwan' and scale > 50 and scale <=200 :
            bhuwan_100_200(path1, image_name)
        elif img_type=='bhuwan' and scale>=300:
            bhuwan_300(path1, image_name)

    '''for geogson to be in latitude longitude and pixels both values'''

    resp = geojson(path1,image_name)
    #print("geojson created at the location you mentioned")
    return resp





'''----------------------------------------------------------------------'''

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
                    get1=image.filename.split('.')[1]
                    geotag = request.form.get('geotag')
                    scale = request.form.get('scale')
                    img_type = request.form.get('img_type')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image, 'VG',scale,img_type)
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'VG',scale,img_type)
                        return resp


                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'VG', scale, img_type)
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






'''----------------------------------------------------------------------'''

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
                    get1=image.filename.split('.')[1]
                    geotag = request.form.get('geotag')
                    scale = request.form.get('scale')
                    img_type = request.form.get('img_type')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image, 'S',scale,img_type)
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'S',scale,img_type)
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'S', scale, img_type)
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



'''----------------------------------------------------------------------'''

@app.route('/satellite_WATER/',methods=['POST'])
def water():

        resp = Response(status=200, content_type='application/json')

        image = request.files['file']  # Single image path

        try:
            if (request.content_type != None):
                if request.content_type.startswith('multipart/form-data'):
                    if 'file' and 'geotag' and 'scale' and 'img_type' in request.form.keys():
                        get1 = image.filename
                        get1 = image.filename.split('.')[1]
                        geotag = request.form.get('geotag')
                        scale = request.form.get('scale')
                        img_type = request.form.get('img_type')
                        if (get1 == 'tif' and geotag == "1"):
                            print("it is a tiff image")
                            resp = func1(image, 'W', scale, img_type)
                            return resp

                        elif ( (get1=="jpg" or "png" or "jpeg") and geotag=="0"):
                            print("it is a jpg")
                            resp = func2(image, 'W', scale, img_type)
                            return resp
                        elif (geotag == "2" and ('bounds' in request.form.keys())):
                            print('func 3')
                            bounds = eval(request.form.get('bounds'))
                            resp = func3(image, bounds, 'W', scale, img_type)
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


'''----------------------------------------------------------------------'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7006, debug=False)