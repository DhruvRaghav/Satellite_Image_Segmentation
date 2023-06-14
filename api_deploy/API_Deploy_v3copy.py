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





def func2(image):
    path = os.getcwd()
    #print("The current working directory is %s" % path)

    #print("creating a new directory now:")
    # Directory
    directory = "uploads01"

    # Parent Directory path
    parent_dir = path

    # Path
    path1 = os.path.join(parent_dir, directory)

    # Create the directory
    # 'GeeksForGeeks' in
    # '/home / User / Documents'
    #os.mkdir(path1)
    #print(path1)
    try:
        os.makedirs(path1, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    in_file=image.filename[:-4]
    #print(in_file)

    image_name = in_file
    print("going to read image")
    image_name_bgr = io.imread(image)
    image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    status = cv2.imwrite(path1+"/"+in_file+".jpg",image_name_rgb)
    print("Image written to file-system : ", status)
    print("going to start prediction")
    mask = predict01(path1,model, image_name, graph, (512, 512))
    print("prediction done")
    resp = geojson2(path1,image_name)
    #print("geojson created at the location you mentioned")
    print(resp)
    return resp

def func1(image):
    #exce = gdal_convert(image_name, southwest, northeast)
    #print("tiff and tab file created ")
    #print(exce)
    # if exce is not None:
    #     # raise FileNotFoundError
    #     resp.status_code = 400
    #     return resp
    path = os.getcwd()
    print("The current working directory is %s" % path)

    print("creating a new directory now:")
    # Directory
    directory = "uploads2"

    # Parent Directory path
    parent_dir = path

    # Path
    path1 = os.path.join(parent_dir, directory)

    # Create the directory
    # 'GeeksForGeeks' in
    # '/home / User / Documents'
    # os.mkdir(path1)
    print(path1)
    try:
        os.makedirs(path1, exist_ok=True)
        print("Directory '%s' created successfully" % directory)
    except OSError as error:
        print("Directory '%s' can not be created" % directory)

    in_file = image.filename[:-4]
    print(in_file)
    print(type(image))
    # in_files = os.path.join(path,in_file + '.jpg')
    image_name = in_file

    import dgsamples

    # Instantiate an image object
    #img = geoio.GeoImage(image)  # a TIF file

    # Print useful information about the object
    #img.files
    #img.meta

    # Get numpy array
    #data = img.get_data()

    # Process data and write to new image
    #newdata = data * 2
    #img.write_img_like_this(path1,"/",(directory+".jpg"), newdata)
    #geoimg = geoio.GeoImage('/home/ceinfo/Desktop/image_10/a.jpg')
    #print(geoimg)
    image.save(path1+"/"+in_file+".tif")
    image.save(path1 + "/" + in_file + ".jpg")

    image.save("/home/ceinfo/Desktop/testing/1111/tiff")

    print("image saved")






    #images = np.array(Image.open(path1,"/",(directory+".jpg")))
   # print("hurray")

    #gray = cv2.cvtColor(images, cv2.COLOR_BGR2GRAY)

    #image_name_bgr = Image.open(image)
    #image_name_bgr = io.imread(image)
   # print("1")

    #image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    #status = cv2.imwrite(path1 + "/" + in_file + ".tif", gray)
    #print("Image written to file-system : ", status)

    # '''gdal convertion'''
    # import rasterio
    #
    # dataset = rasterio.open(path1 + "/" + in_file + ".tif")
    # print(dataset.bounds)
    # for i in range(0, len(dataset.bounds)):
    #     a = dataset.bounds[i]
    #     print(a)

    #southwest=
    #northeast=
    #gdal_convert(image_name, southwest, northeast)
   # print("hello")
    #image_name_bgr = io.imread(image)
    #print(image_name_bgr)
    # print("^^^^^^^^^^^^^^^^^^")
    #image_name_rgb = cv2.cvtColor(image_name_bgr, cv2.COLOR_BGR2RGB)
    #status = cv2.imwrite(
     #   "/home/ceinfo/Desktop/image_10/1111.jpg",
     #   image_name_rgb)
    #print("Image written to file-system : ", status)




    print("3333333333333333333333333333333333333333333333333333333333333333")




    img = geoio.GeoImage("/home/ceinfo/Desktop/testing/test_image.tif")  # a TIF file

    # Print useful information about the object
    img.files
    img.meta

    # Get numpy array
    data = img.get_data()

    '''to make the jpg from tiff file'''
    # Process data and write to new image
    newdata = data * 2
    img.write_img_like_this('/home/ceinfo/Desktop/image_10/test.jpg', newdata)
    geoimg = geoio.GeoImage('/home/ceinfo/Desktop/image_10/test.jpg')
    # print(geoimg)
    '''extracting out the coordinated'''

    import rasterio
    dataset = rasterio.open('/home/ceinfo/Desktop/image_10/test.jpg')
    # print (dataset.bounds)
    c = []
    d = []
    for i in range(0, len(dataset.bounds)):
        if i <= 1:
            a = dataset.bounds[i]
            c.append(float(a))
        if i > 1 and i <= 3:
            a = dataset.bounds[i]
            d.append(float(a))

    # print(a)
    # print((type(a)))
    print(c)
    print(d)
    # a=[]
    # for i in range(0,len(dataset.bounds)):
    #  a=a.append(i)
    # print(a)
    # BoundingBox(left=71.84509, bottom=22.106, right=78.61267, top=25.37381)

    #
    #
    ''' to make tab file '''
    sw_lat = c[0]
    print(sw_lat)
    print("1")
    sw_long = c[1]
    print(sw_long)
    ne_lat = d[0]
    print(ne_lat)
    ne_long = d[1]
    print(ne_long)
    southwest = [str(sw_lat), str(sw_long)]
    print(southwest)
    northeast = [str(ne_lat), str(ne_long)]
    print(northeast)
    gdal_convert("1585922787072", southwest, northeast)




    print("444444444444444444444444444444444444444444444444444444444444444444444444444")




    print("going to start prediction")
    mask = predict01(path1, model, image_name, graph, (512, 512))
    print("mask created at the mentioned location")
    '''for geogson to be in latitudelongitude and pixels both values'''
    resp = geojson(path1,image_name)
    #print("geojson created at the location you mentioned")
    return resp





@app.route('/satellite_FP/',methods=['POST'])  # Single Api
def FP():
    print ("Welcome to satellite image segmentation")
    resp=Response(status=200,content_type='application/json')
   # print("1")
    # try:
    image = request.files['file']  # Single image path
    #image = request.files.get('file', '')
    #image.save('/home/ceinfo/Desktop/testing/test_image1.jpg')

    #print(image)
    #print(type(image))
    #print("2")

    try:
        if(request.content_type!=None):
             #print("3")
             if request.content_type.startswith('multipart/form-data'):
                if 'file' and 'geotag' in request.form.keys():

                    # import os

                    # detect the current working directory and print it
                    #path = os.getcwd()
                    #print("The current working directory is %s" % path)
                    #get=eval(request.form.get('file'))
                    #image = request.files['file']
                    get1=image.filename

                    #print(get1)
                    #print((1))
                    #print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                    get1=get1[-3:]
                    #get2=get2[-4:]
                    #print(get1)
                    #print(type(get1))
                    #rint("$")
                    #print(get2)
                    #print(type(get2))
                    geotag=request.form.get('geotag')
                    #print(geotag)
                    #print(type(geotag))
                    #bounds = (request.form.get('bounds'))


                    if ( get1== 'tif' and geotag=="0"):
                        print("it is a tiff image")
                        resp=func1(image)
                        return resp

                    elif( get1=="jpg" and geotag=="1"):
                        print("it is a jpg")
                        resp=func2(image)
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
    resp = Response(status=200, content_type='application/json')

    # try:
    image = request.files['file']  # Single image path
    print("*************")
    try:
        if (request.content_type != None):
           print("1")
           if request.content_type.startswith('multipart/form-data'):
             print("2")
             if 'southwest'and 'northeast'and 'file' and 'bounds' in request.form.keys():
                print("3")
                # results = model.detect_licenseplates(image)
                #southwest = request.form.get('southwest')[7:-1].split(',')
                #northeast = request.form.get('northeast')[7:-1].split(',')
                bounds = eval(request.form.get('bounds'))
                sw_lat = bounds['_southWest']['lat']
                sw_long = bounds['_southWest']['lng']
                ne_lat = bounds['_northEast']['lat']
                ne_long = bounds['_northEast']['lng']
                southwest = [str(sw_lat), str(sw_long)]
                northeast = [str(ne_lat), str(ne_long)]

                #image_name = request.form.get('name')
                #resp = {'1': [southwest, northeast]}
                image_name_BGR = io.imread(image)
                image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                status = cv2.imwrite('/home/ceinfo/Desktop/image_10/1111.jpg',image_name_RGB)
                print("Image written to file-system : ", status)
                image_name=image.filename
                print(image_name)
                image_name=image_name[:-4]
                print(image_name)
                print(southwest, northeast, image_name)
                gdal_convert(image_name, southwest, northeast)
                mask=predict_veg(image_name)
                resp = geojson1(image_name)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
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
        return resp


@app.route('/satellite_SOIL/',methods=['POST'])
def Soil():
    resp = Response(status=200, content_type='application/json')

    # try:
    image = request.files['file']  # Single image path
    print(image)

    try:
      if (request.content_type != None):
         print("1")
         if request.content_type.startswith('multipart/form-data'):
            print("2")
            if 'southwest' and 'northeast' and 'file' and "bounds" in request.form.keys():
                print("3")
                #results = model.detect_licenseplates(image)
                #southwest = request.form.get('southwest')[7:-1].split(',')
                #northeast = request.form.get('northeast')[7:-1].split(',')
                bounds = eval(request.form.get('bounds'))

                sw_lat = bounds['_southWest']['lat']
                sw_long = bounds['_southWest']['lng']
                ne_lat = bounds['_northEast']['lat']
                ne_long = bounds['_northEast']['lng']
                southwest = [str(sw_lat), str(sw_long)]
                northeast = [str(ne_lat), str(ne_long)]

                #image_name = request.form.get('name')
                image_name=image.filename

                image_name=image_name[:-4]
                resp = {'1': [southwest, northeast]}
                print(southwest, northeast, image_name)
                image_BGR=io.imread(image)
                image_RGB = cv2.cvtColor(image_BGR, cv2.COLOR_BGR2RGB)
                status=cv2.imwrite("/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/1111.jpg",image_RGB)
                print(status)
                gdal_convert(image_name, southwest, northeast)
                mask=predict_soil(image_name)
                resp = geojson1(image_name)
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
    image = request.files['file']  # Single image path

    try:
      if (request.content_type != None):
         if request.content_type.startswith('multipart/form-data'):
            if 'southwest' and 'northeast' and 'file' and 'bounds' in request.form.keys():
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
                image_name=image.filename
                print(image_name)
                image_name=image_name[:-4]
                print(image_name)
                image_name_BGR = io.imread(image)
                image_name_RGB= cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                status = cv2.imwrite('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/1111.jpg',image_name_RGB)
                print("Image written to file-system : ", status)
                print(bounds)
                #image_name = request.form.get('name')
                #resp={'1':[southwest,northeast]}
                #print(southwest, northeast, image_name)
                exce = gdal_convert(image_name, southwest, northeast)
                if exce is not None:
                    # raise FileNotFoundError
                    resp.status_code = 400
                    return resp
                mask = predict_RD(model1, image_name, graph1,(256,256))
                #resp = geojson(image_name, mask)
                resp = geojson1(image_name)
                # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
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
        return resp


@app.route('/satellite_water/',methods=['POST'])
def water():

        resp = Response(status=200, content_type='application/json')

        #try:
        image = request.files['file']  # Single image path

        try:
            if (request.content_type != None):
                  if request.content_type.startswith('multipart/form-data'):
                        if 'southwest' and 'northeast' and 'file' and 'bounds' in request.form.keys():
                            # results = model.detect_licenseplates(image)
                            #southwest = request.form.get('southwest')[7:-1].split(',')
                            #northeast = request.form.get('northeast')[7:-1].split(',')
                            #image_name = request.form.get('name')
                            bounds = eval(request.form.get('bounds'))
                            sw_lat = bounds['_southWest']['lat']
                            sw_long = bounds['_southWest']['lng']
                            ne_lat = bounds['_northEast']['lat']
                            ne_long = bounds['_northEast']['lng']
                            southwest = [str(sw_lat), str(sw_long)]
                            northeast = [str(ne_lat), str(ne_long)]
                            image_name = image.filename
                            print(image_name)
                            image_name = image_name[:-4]
                            print(image_name)
                            image_name_BGR = io.imread(image)
                            image_name_RGB = cv2.cvtColor(image_name_BGR, cv2.COLOR_BGR2RGB)
                            status = cv2.imwrite('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/1111.jpg',image_name_RGB)
                            print("Image written to file-system : ", status)
                            print(bounds)
                            resp = {'1': [southwest, northeast]}
                            print(southwest, northeast, image_name)
                            gdal_convert(image_name, southwest, northeast)
                            mask=predict_water(image_name)
                            resp = geojson1(image_name)
                            # resp = json.dumps({'Predictions': [{'x1': i[0], 'y1': i[1], 'x2': i[2], 'y2': i[3] } for i in results]})
                            # resp = json.dumps({'Predictions': [{'x1': i[0][0], 'y1': i[0][1], 'w': i[2][0] - i[0][0], 'h': i[2][1] - i[0][1]} for i in results]})
                            return resp
                        else:
                            resp.status_code = 400
                            print("enter the correct parameters in the code")
                            return resp
                  else:
                     resp.status_code = 400
                     print("select the file option  rather than the text version in pycharm , error:")
                     return resp
            else:
                 print("enter the correct parameters  in the postman body")
                 resp.status_code = 400
                 return resp
        except Exception as e:
                logger.error(msg=str(e), status_code=500)
                resp.status_code = 500
                return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7005, debug=False)