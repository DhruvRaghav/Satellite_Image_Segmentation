from flask import Flask, request,Response
app = Flask(__name__)
import logging
from logging.handlers import TimedRotatingFileHandler
from logging import Formatter
import io
from skimage import io
from api_deploy.geotiff import gdal_convert
from api_deploy.pixel_to_lat_lon import *
from api_deploy.predict01 import *
from api_deploy.Soil import *
from api_deploy.Ocean import *
from api_deploy.vegetation import *


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



'''---------------------------------------------------------------------------------------'''

''' ................MODEL LOADING........................'''
try:
     model,graph=read_model()
     model1,graph1 = read_model_Rd()

except Exception as e:
     print(e)
     logger.error(msg="model is not loaded")





'''----------------------------------------------------------------------------------------'''

'''...................to check the name of the GPU........................................'''
if tf.test.gpu_device_name():
    print('Default GPU Device:{}'.format(tf.test.gpu_device_name()))
else:
   print("Please install GPU version of TF")



'''----------------------------------------------------------------------------------------'''

'''................... third function: takes jpg, bounds, geotag :2 --------------------------------------------------'''

def func3(image,bounds,key):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN jpg FORM  & GEOTAG : 2 '''
    path = os.getcwd()
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
    in_file=image.filename.split('.')[0]
    image_name = in_file


    '''to read image from postman in bgr fotmat'''
    image_name_bgr = io.imread(image)



    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)
    print(datetime.datetime.now())
    '''prediction : mask will be generated:'''
    if key=="FP":
        mask = predict01(path1,model, image_name, graph, (512, 512))
        print("prediction done : masks created")
        print(datetime.datetime.now())
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

    sw_lat = bounds['_southWest']['lat']
    sw_long = bounds['_southWest']['lng']
    ne_lat = bounds['_northEast']['lat']
    ne_long = bounds['_northEast']['lng']
    southwest = [str(sw_lat), str(sw_long)]
    northeast = [str(ne_lat), str(ne_long)]
    image_name = image.filename
    image_name = image_name.split('.')[0]
    exce = gdal_convert(path1,image_name, southwest, northeast)
    print('tiff',datetime.datetime.now())


    '''To create the goejson file use this function'''
    resp = geojson5(path1,image_name)
    return resp

'''----------------------------------------------------------------------------------------'''

'''.....................building footprints two function : -------func1 and func2----------'''

def func2(image,key):

    '''  TO RETURN PIXELS  IT REQUIRES : IMAGE IN JPG FORM  & GEOTAG : 0 '''
    path = os.getcwd()
    '''Directory'''
    directory = "uploads01"
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
    in_file=image.filename.split('.')[0]

    image_name = in_file


    '''to read image from postman in bgr fotmat'''
    print("going to read image")
    image_name_bgr = io.imread(image)



    '''converting bgr to rgb  , so that it can be saved/write in the directory'''
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)

    '''prediction : mask will be generated:'''
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
    return resp


'''----------------------------------------------------------------------'''

def func1(image,key):
    path = os.getcwd()
    # Directory
    directory = "uploads2"

    # Parent Directory path
    parent_dir = path

    # Path
    path1 = os.path.join(parent_dir, directory)
    try:

        os.makedirs(path1, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    in_file = image.filename[:-4]
    print(in_file)
    print(type(image))
    image_name = in_file
    image.save(path1 + "/" + in_file + ".jpeg")


    '''to make the jpg from tiff file'''
    '''extracting out the coordinated'''

    '''----------------------------------------------------------------------------'''
    if key=="FP":
        mask = predict_FP_Tif_PL(path1, model, image_name, graph, (512, 512))
        print("mask created at the mentioned location")
    '''----------------------------------------------------------------------------'''
    if  key=="S":
        mask = predict_soil_Tif_PL(path1, image_name)

    '''----------------------------------------------------------------------------'''

    if key=="RD":
        mask = predict_RD_Tif_PL(path1,model1, image_name, graph1, (256, 256))
        print("mask created at the mentioned location")

    '''----------------------------------------------------------------------------'''
    if key == "VG":
        mask = predict_veg_Tif_PL(path1, image_name)
        print(" prediction done: Vegetation masks created")


    if key=="W":
        mask = predict_water_Tiff_PL(path1)

    '''for geogson to be in latitudelongitude and pixels both values'''

    resp = geojson(path1,image_name)
    return resp




'''----------------------------------------------------------------------'''

@app.route('/satellite_FP/',methods=['POST'])  # Single Api
def FP():
    print ("Welcome to satellite image segmentation")
    resp=Response(status=200,content_type='application/json')
    image = request.files['file']  # Single image path
    print(image)
    geotag = request.form.get('geotag')
    print('start',datetime.datetime.now())
    print(geotag)

    try:
        if(request.content_type!=None):
             if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():
                    get1=image.filename.split('.')[1]

                    geotag=request.form.get('geotag')
                    if ( get1== 'tif' and geotag=="1"):
                        resp=func1(image,'FP')
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        resp = func2(image, 'FP')
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'FP')
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

@app.route('/satellite_VEG/',methods=['POST'])
def VEG():
    print("Welcome to satellite image segmentation-VEGETATION:")
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
                        resp = func1(image, 'VG')
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'VG')
                        return resp


                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'VG')
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
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image, 'S')
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'S')
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'S')
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
                    get1=image.filename.split('.')[1]
                    geotag = request.form.get('geotag')
                    if (get1 == 'tif' and geotag == "1"):
                        print("it is a tiff image")
                        resp = func1(image,'RD')
                        return resp


                    elif ((get1 == "jpg" or "png" or "jpeg") and geotag == "0"):
                        print("it is a jpg")
                        resp = func2(image, 'RD')
                        return resp

                    elif (geotag == "2" and ('bounds' in request.form.keys())):
                        print('func 3')
                        bounds = eval(request.form.get('bounds'))
                        resp = func3(image, bounds, 'RD')
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

        #try:
        image = request.files['file']  # Single image path

        try:
            if (request.content_type != None):
                if request.content_type.startswith('multipart/form-data'):
                    if 'file' and 'geotag' in request.form.keys():
                        get1 = image.filename
                        get1 = image.filename.split('.')[1]
                        geotag = request.form.get('geotag')
                        if (get1 == 'tif' and geotag == "1"):
                            print("it is a tiff image")
                            resp = func1(image, 'W')
                            return resp

                        elif ( (get1=="jpg" or "png" or "jpeg") and geotag=="0"):
                            print("it is a jpg")
                            resp = func2(image, 'W')
                            return resp
                        elif (geotag == "2" and ('bounds' in request.form.keys())):
                            print('func 3')
                            bounds = eval(request.form.get('bounds'))
                            resp = func3(image, bounds, 'W')
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
    app.run(host='0.0.0.0', port=7007, debug=False)