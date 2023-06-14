import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os
#def predict_soil(image_id):
image = cv2.imread('/mnt/vol1/Deployment_projects/satellite_image_segmentation/test_imgs/PROMIGAS_L36_C3.tif')
plt.imshow(image)
plt.show()
#os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
    # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # print(geoimg)

image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
lower = np.array([0, 0, 0])
upper = np.array([23, 114, 69])
mask = cv2.inRange(image, lower, upper)
plt.imshow(mask)
plt.show()

thresh = cv2.erode(mask, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
plt.imshow(thresh)
plt.show()
#plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask.jpg',
              # thresh, cmap='gray', dpi=1)