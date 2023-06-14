
from PIL import Image
#from os import walk
import cv2
from os import walk
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import date
import gdal

destinationFile = 'qwert.jpg'
inpuDataset = gdal.Open('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/uploads/1585831523973.tif')
format = 'JPEG'

driver = gdal.GetDriverByName(format)

outputDataset = driver.CreateCopy(destinationFile, inpuDataset, 0)


inpuDataset = None
outputDataset = None

#nycImage = cv2.imread(destinationFile, cv2.IMREAD_LOAD_GDAL & cv2.IMREAD_GRAYSCALE)

nycImage = cv2.imread(destinationFile, cv2.IMREAD_LOAD_GDAL & cv2.IMREAD_GRAYSCALE)

th, processedPic = cv2.threshold(nycImage, 110, 255, cv2.THRESH_BINARY)

cv2.imwrite(destinationFile, processedPic)
cv2.imshow('thresholded_NDVI', processedPic)

cv2.waitKey(0)
cv2.destroyAllWindows()