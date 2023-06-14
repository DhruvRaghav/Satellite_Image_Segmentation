import geoio
import numpy as np
import cv2
import pandas as pd
from os import walk
import tifffile as tif
import json
import matplotlib.pyplot as plt
import os
data_path="/home/prateek/Downloads/tifff/"
# for data_path in file_path:
ids=[]
for (dirpath,dirnames,filenames) in walk(data_path):
    ids.extend(filenames)
    break
test_ids=[]
for i in ids:
    if 'tif' in i:
        test_ids.append(i)
counts=[]
print(test_ids)
# centroid
polygon=[]
new_filter=[]

for image_id in test_ids:
    # if(os.path.exists())
    # img=cv2.imread("/mnt/vol1/satellite_image/predicted_city_manipur/predicted_output_{s}/2019-07-27/".format(s=dir_names)+image_id[:-4]+'.Jpg')
    # if():
    #comment Predictions mask(binary images) Path
    # img=cv2.imread("/mnt/vol1/predicted_manipur_whole/2019-09-05/{}.jpg".format(image_id[:-4]))
    print(data_path+'2019-11-07/'+image_id[:-4]+'.tif')
    # print(data_path+'2019-11-07/'+'1.JPG')
    # img = cv2.imread(data_path+'2019-11-07/'+'1.JPG')
    # img=tif.imread(data_path+'/arcticdem_mosaic_1km_v3.0.tif')
    img=cv2.imread('/home/prateek/Downloads/Green_381.jpg')
    #     img = cv2.imread("/mnt/vol1/satellite_image/predicted_city_manipur/predicted_output_{s}/2019-07-27/".format(s=dir_names) + image_id[:-4] + '.jpg')
    # image_crop(img,os.path.join(data_path,image_id))
    # img=cv2.imread('/mnt/vol1/satellite_image/cropped_img/'+image_id[:-4]+'.jpg')
    # print(img)
    # print("/mnt/vol1/satellite_image/predicted_city_manipur/predicted_output_{s}/2019-07-27/".format(s=dir_names)+image_id[:-4]+'.Jpg')
    # print(img.shape)

    # gray_img=np.zeros((7500,7400,3))
    # gray_img[np.where(img>0)]=255.0

    # cv2.imwrite('my_tif.jpg',gray_img)
    # plt.imshow(gray_img)
    # plt.show()
    # print(img)
    # print(gray_img.min(),gray_img.max())
    # print(gray_img.shape)
    # img=img/abs(img.min())
    # print(img.min(), img.max())
    # geoimg = geoio.GeoImage("/mnt/vol1/satellite_image/city_image/{}/" .format(dir_names)+ image_id[:-4]+'.Jpg')
    # geoimg=geoio.GeoImage("/mnt/vol1/Manipur_geotiff_whole/{}".format(image_id))
    geoimg = geoio.GeoImage(data_path+image_id)
    # print(geoio.GeoImage(data_path+image_id))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    # gray2=gray.copy()
    # mask=np.zeros(gray.shape,np.uint8)
    contours,_=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        points=''
        endpoint = []
        x1, y1 = geoimg.raster_to_proj(cnt[0][0][0], cnt[0][0][1])
        # x1,y1=pixel_lat_long(file=os.path.join(data_path,image_id),x=cnt[0][0][0],y=cnt[0][0][1])
        # if (x1 < 90.0 and x1 > 65.0 and y1 < 40.0 and y1 > 10.0):
        endpoint.append(x1)
        endpoint.append(y1)
        for j,i in enumerate(cnt):
            if (i[0][0] == 0):
                i[0][0] = 213.0
            elif (i[0][1] == 0):
                i[0][1] = 34.0
            x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            # x,y=pixel_lat_long(file=os.path.join(data_path,image_id),x=i[0][0],y=i[0][1])
            # if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
                # points=points+str(x)+" "+str(y)+','
                # if (len(points) != 0):
            new_filter.append([x, y])

        if(len(endpoint)!=0 and len(new_filter)!=0):

            # print(new_filter)
            if(len(new_filter)>10):
                new_filter.append(endpoint)
                print(len(new_filter))
                polygon.append(new_filter)
        new_filter=[]
        # if(len(points)!=0):
        #     polygon.append('POLYGON (('+points[:len(points)-1]+'))')
    # print(x1, y1)
    # print(polygon,end='\n')
    if(len(polygon)!=0):
    # print(polygon)
        d = {"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "geometry": {"type": "MultiPolygon", "coordinates": polygon}}]}
    # d={'geom':polygon}
    # polygon = []
    #     if not (os.path.exists('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}'.format(dir_names))):
    #         os.makedirs('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}'.format(dir_names))
    #     with open('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}/{}.geojson'.format(dir_names,image_id[:-4]), 'w') as fp:
    # Geojson file output Path
    # with open('/mnt/vol1/geojson_line_manipur_state/{}.geojson'.format(image_id[:-4]),'w') as fp:
    #         json.dump(d, fp)
    with open(data_path+image_id[:-4]+'.geojson','w') as fp:
            json.dump(d, fp)
    polygon=[]
        # data=pd.DataFrame(d,columns=["geom"])
        # data.to_csv('/mnt/Ext1/PycharmProjects/Misc/LAT_LONG_greater_kailash/count_{}.csv'.format(image_id[:-4]))


