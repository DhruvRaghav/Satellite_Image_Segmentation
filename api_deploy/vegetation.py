import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os
import pandas as pd
import geoio
# import math
# from imutils import perspective
# import imutils

from PIL import Image,ImageFilter

def predict_veg(path1,image_id):
        print("inside predict")
        print(image_id)
        #im = Image.open(path1 + "/" + image_id + '.jpg')
        print(path1)
        image = cv2.imread(path1+ "/" + image_id + '.jpg')
        # os.remove(path1 + "/" + image_id + '.jpg')

# geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# print(geoimg)

        #image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower = np.array([30, 30, 20])
        upper = np.array([255, 255, 100])
        mask = cv2.inRange(image, lower, upper)
        # plt.imshow(mask)
        # plt.show()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        thresh = cv2.erode(close, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)
        #plt.imshow(thresh)
        #plt.show()
        plt.imsave(path1+"/"+image_id+'_mask.png',thresh, cmap='gray', dpi=1)


def predict_veg_Tif_PL(path1,image_id):
        print("inside predict")
        print(image_id)
        #im = Image.open(path1 + "/" + image_id + '.jpg')
        print(path1)
        image = cv2.imread(path1+ "/" + image_id + '.jpeg')
        #os.remove(path1 + "/" + image_id + '.jpeg')

# geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# print(geoimg)

        #image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        lower = np.array([30, 30, 20])
        upper = np.array([255, 255, 100])
        mask = cv2.inRange(image, lower, upper)
        # plt.imshow(mask)
        # plt.show()
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        thresh = cv2.erode(close, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)
        #plt.imshow(thresh)
        #plt.show()
        plt.imsave(path1+"/"+image_id+'_mask.png',thresh, cmap='gray', dpi=1)


if __name__ == '__main__':
        predict_veg("/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01","Azamgarh_1")


