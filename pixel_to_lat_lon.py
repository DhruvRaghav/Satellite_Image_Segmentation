import geoio
import numpy as np
import cv2
import pandas as pd
from os import walk
import json
import os
#from GEo_tiff import pixel_lat_long


#input folder with TAB file
data_path="/mnt/vol1/Deployment_projects/satellite_image_segmentation/test_imgs/"
#folder with mask images
data_path2="/mnt/vol1/Deployment_projects/satellite_image_segmentation/outputs/2020-09-24/"
# for data_path in file_path:
ids=[]
for (dirpath,dirnames,filenames) in walk(data_path):
    ids.extend(filenames)
    break
test_ids=[]
for i in ids:
    if 'jpg' in i:
        test_ids.append(i)
counts=[]
print(test_ids)
# centroid
polygon=[]
new_filter=[]

for image_id in test_ids:
    #comment Predictions mask(binary images) Path
    img=cv2.imread(os.path.join(data_path2,"{}.png".format(image_id[:-4])))
    #     img = cv2.imread("/mnt/vol1/satellite_image/predicted_city_manipur/predicted_output_{s}/2019-07-27/".format(s=dir_names) + image_id[:-4] + '.jpg')
    # img=cv2.imread('/mnt/vol1/satellite_image/cropped_img/'+image_id[:-4]+'.jpg')
    # print(img.shape)
    geoimg = geoio.GeoImage(data_path+image_id)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours[1]:
        points=''
        endpoint = []
        x1, y1 = geoimg.raster_to_proj(cnt[0][0][0], cnt[0][0][1])
        # x1,y1=pixel_lat_long(file=os.path.join(data_path,image_id),x=cnt[0][0][0],y=cnt[0][0][1])
        if (x1 < 90.0 and x1 > 65.0 and y1 < 40.0 and y1 > 10.0):
            endpoint.append(x1)
            endpoint.append(y1)
        for j,i in enumerate(cnt):
            # if (i[0][0] == 0):
            #     i[0][0] = 213.0
            # elif (i[0][1] == 0):
            #     i[0][1] = 34.0
            x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
                new_filter.append([x, y])

        if(len(endpoint)!=0 and len(new_filter)!=0):

            # print(new_filter)
            if(len(new_filter)>10):
                new_filter.append(endpoint)
                # print(len(new_filter))
                polygon.append(new_filter)
        new_filter=[]
        # if(len(points)!=0):
        #     polygon.append('POLYGON (('+points[:len(points)-1]+'))')
    if(len(polygon)!=0):
        d = {"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "geometry": {"type": "MultiLineString", "coordinates": polygon}}]}
    else:
        d={"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "geometry": {"type": "MultiLineString", "coordinates": polygon}}]}
        print("No polygons detected")
    #     if not (os.path.exists('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}'.format(dir_names))):
    #         os.makedirs('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}'.format(dir_names))
    #     with open('/mnt/vol1/satellite_image/geotiff_manipur_city/predicted_output_{}/{}.geojson'.format(dir_names,image_id[:-4]), 'w') as fp:
    # Geojson file output Path
    # with open('/mnt/vol1/geojson_line_manipur_state/{}.geojson'.format(image_id[:-4]),'w') as fp:
    #         json.dump(d, fp)
    with open(data_path+image_id[:-4]+'.geojson','w') as fp:
            json.dump(d, fp)
    polygon=[]

