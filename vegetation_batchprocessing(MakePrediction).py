import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os

#from __future__ import division
import cv2
import numpy as np
from os import walk
import os
#import extra_functions
import numpy as np
# from keras.models import model_from_json
from keras.models import load_model
import matplotlib.pyplot as plt
from datetime import date
from keras import backend as K
from keras.backend import binary_crossentropy
import tensorflow as tf
from os import walk
import os
import pandas as pd
import geoio
# import math
# from imutils import perspective
# import imutils

def predict_veg():
        '''path of the images whose overlays you want to create '''
        data_path = '/home/ceinfo/Desktop/veg_testing/'
        print(data_path)
        #num_channels = 3
        #num_mask_channels = 1
        #threshold = 0.1

        ids = []
        test_ids = []
        for (dirpath, dirnames, filenames) in walk(data_path):
                ids.extend(filenames)
                print(ids)
                print("###########")
                break

        for i in ids:
                if 'jpg' or 'png' in i:
                        test_ids.append(i)
        print(test_ids)
        print(len(test_ids))


        for image_id in test_ids:
                                im = cv2.imread(data_path+image_id)




                                #os.remove('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/' + image_id + '.jpg')
                                #print("jpg removed")
                                # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
                                # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
                                # print(geoimg)

                                #image = cv2.cvtColor(im, cv2.COLOR_RGB2HSV)
                                lower = np.array([30, 30, 20])
                                upper = np.array([255, 255, 100])
                                mask = cv2.inRange(im,lower,upper)
                                # plt.imshow(mask)
                                # plt.show()
                                kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(3,3))
                                opening = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel,iterations=2)
                                close = cv2.morphologyEx(opening,cv2.MORPH_CLOSE,kernel,iterations=2)

                                thresh = cv2.erode(close, None, iterations=1)
                                thresh = cv2.dilate(thresh, None, iterations=1)
                                # plt.imshow(thresh)
                                # plt.show()
                                image_id1=image_id[:-4]
                                length = len(test_ids)
                                #print(length)

                                plt.imsave("/home/ceinfo/Desktop/changed_testing_result/" + image_id1 + '.jpg',
                                            thresh, cmap='gray', dpi=1)
                                print("masks created for image {} : {}".format(test_ids.index(image_id)+1, image_id1))
        #print(length)

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
if __name__ == '__main__':
   predict_veg()