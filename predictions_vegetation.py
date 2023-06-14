import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os
from datetime import date

import pandas as pd
import geoio
# import math
# from imutils import perspective
# import imutils

#def predict_veg(image_id):
image = cv2.imread('/home/ceinfo/Desktop/Images/Azamgarh_1.jpg')
#os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
# image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# print(geoimg)

#image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
lower = np.array([30, 30, 20])
upper = np.array([255,255, 100])
mask = cv2.inRange(image,lower,upper)
#plt.imshow(mask)
#plt.show()


thresh = cv2.erode(mask, None, iterations=1)
thresh = cv2.dilate(thresh, None, iterations=1)
#plt.imshow(thresh)
#plt.show()

alpha = 0.6
new_mask = np.squeeze(thresh, -1)*255
color_mask = np.dstack((new_mask, new_mask, new_mask))

image = image - image * (color_mask * 0.3)
image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
# print(image)

plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/outputs/" + str(
    date.today()) + "/overlays/overlay_veg_" + image, image, dpi=1)

#plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask.jpg',
                  # thresh, cmap='gray', dpi=1)
        # return thresh
        # cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# cnts = cnts[0] if len(cnts) == 2 else cnts[1]
# bounding = []
# bounding1 =[]
# Moment = []
# centroid1 = []
#
# for i in cnts:
#         print("i:",i)
#
#         x1, y1 = geoimg.raster_to_proj(i[0][0][0] ,i[0][0][1])
#
#         draw = cv2.drawContours(image, [i], -1, (0, 0, 255), 3)
#
#         c = max(cnts, key=cv2.contourArea)
#
#         cv2.drawContours(image, [c], -1, (0, 255, 255), 3)
#
#
# plt.imshow(image)
# plt.show()
