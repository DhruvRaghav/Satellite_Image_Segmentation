import geoio
import numpy as np
import cv2
from os import walk
import pandas as pd
# import matplotlib.pyplot as plt
# img = cv2.imread('/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/predicted_images_link_jacard_int_azam_submit/2019-07-11/5756.jpg')
# img = cv2.resize(img, (400, 500))
data_path="/home/ceinfos/Downloads/Satellite_images_data/test"
ids=[]
for (dirpath, dirnames, filenames) in walk(data_path):
    ids.extend(filenames)
    break
test_ids=[]
for i in ids:
    if 'jpg' in i:
        test_ids.append(i)
counts=[]
centroid_x=()
centroid_y=()
region_id=()
polygon=[]
print(test_ids)
for image_id in test_ids:
    img = cv2.imread("/home/ceinfos/Downloads/Satellite_images_data/test/"+image_id)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    gray2 = gray.copy()
    mask = np.zeros(gray.shape, np.uint8)
    contours,hier = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # counts.append(len(contours))
    for cnt in contours:
        geoimg=geoio.GeoImage("/home/ceinfos/Downloads/Satellite_images_data/SatelliteAnnotations/Images_With_Annotation (copy)/"+image_id)
        points=''
        for j,i in enumerate(cnt):
            # print(i)
            x, y = geoimg.raster_to_proj(i[0][0],i[0][1])
            # centroid_x.append(x)
            # centroid_y.append(y)
            # region_id.append(j)
            points=points+str(x)+" "+str(y)+','
        polygon.append('POLYGON (('+points[:len(points)-1]+'))')

    # print(len(contours))
# d={'regionId':region_id,'centroid_x':centroid_x,'centroid_y':centroid_y}
d={'geom':polygon}
# data = pd.DataFrame(d,columns=['regionId','centroid_x', 'centroid_y'])
data = pd.DataFrame(d,columns=['geom'])
data.to_csv('count_vgg.csv')