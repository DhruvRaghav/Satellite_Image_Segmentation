import numpy as np
import cv2
import geoio
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os
from PIL import Image

geoimg = geoio.GeoImage('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/5721.jpg')
print(geoimg)
# geoimgimg=cv2.imread('/home/prateek/Downloads/satellite_change_detection/3_Bands_Data/IMG_03_17102019/T43RGM_17102019.tif')
# #Image_pil=Image.open(image)
# print(img)
# print(img.shape)
# #image = cv2.cvtColor(img, cv2.COLOR_RGB2XYZ)
# lower = np.array([10, 5, 15])
# upper = np.array([170, 170, 150])
# mask = cv2.inRange(img,lower,upper)
# plt.imshow(mask,cmap='gray')
# plt.imshow(mask)
# plt.show()