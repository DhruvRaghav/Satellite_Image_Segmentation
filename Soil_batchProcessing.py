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
def predict_soil():
    #image = cv2.imread('/home/ceinfo/Desktop/1/'+image_id +'.jpg')

    data_path = '/home/ceinfo/Desktop/1/'
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

        lower = np.array([44, 6, 126])
        upper = np.array([252, 230, 240])

        mask = cv2.inRange(image, lower, upper)
        # plt.imshow(mask)
        # plt.show()

        thresh = cv2.erode(mask, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        #plt.imshow(thresh)
       # plt.show()
        plt.imsave("/home/ceinfo/Desktop/2/" + image_id[0:-4] + '.png',
                   thresh, cmap='gray', dpi=1)


if __name__ == '__main__':
    predict_soil()