import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
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
def predict_building():
    #image = cv2.imread('/home/ceinfo/Desktop/1/'+image_id +'.jpg')

    data_path = '/home/ceinfo/Desktop/HELLO/images/'
    #print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        #print(ids)
        #print("###########")
        break

    for i in ids:
        if 'jpg' or 'png' in i:
            test_ids.append(i)
    #print(test_ids)
    #print(len(test_ids))

    for image_id in test_ids:
        im = cv2.imread(data_path + image_id)

        #os.remove('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/'+ image_id +'.jpg')
        # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # print(geoimg)

        image = cv2.cvtColor(im, cv2.COLOR_HSV2RGB)

        ''' 50'''
        '''1st try'''
        # (133, 137, 144)
        # (212, 221, 216)
        '''2nd try '''
        # lower = np.array([1, 1, 1])
        # upper = np.array([132, 121, 119])
        '''3nd try '''
        # lower = np.array([50, 50, 1])
        # upper = np.array([244, 221, 212])


        lower = np.array([50, 50, 1])
        upper = np.array([244, 221, 212])

        mask = cv2.inRange(image, lower, upper)

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=3)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=3)

        thresh = cv2.erode(close, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)
        # plt.imshow(thresh)
        # plt.show()

        #plt.imshow(thresh)
       # plt.show()
        plt.imsave("/home/ceinfo/Desktop/HELLO/" + image_id[0:-4] + '.png',
                   thresh, cmap='gray', dpi=1)


if __name__ == '__main__':
    predict_building()