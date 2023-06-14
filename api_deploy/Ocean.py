import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os

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
def predict_water(path1):
    data_path = path1+"/"
    print(data_path)
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        # print(ids)
        # print("###########")
        break

    for i in ids:
        if 'jpg'  in i:
            test_ids.append(i)
    # print(test_ids)
    # print(len(test_ids))

    for image_id in test_ids:
        image = cv2.imread(path1 + "/" + image_id, cv2.IMREAD_GRAYSCALE)
        # os.remove(path1 + "/" + image_id)
        # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # print(geoimg)
        # image1=image


        # image = cv2.cvtColor(image,cv2.COLOR_BGR2HLS)
        # lower = np.array([75, 35, 15])
        # upper = np.array([255,255,255])
        # mask = cv2.inRange(image, lower, upper)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        # # plt.imshow(mask)
        # # plt.show()
        # thresh = cv2.dilate(mask, None, iterations=1)
        # #thresh = cv2.erode(thresh, None, iterations=2)

        th, msk = cv2.threshold(image, 45, 255, cv2.THRESH_BINARY)  # threshold range

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.bitwise_not(msk)


        # tmp_thresh=thresh
        # tmp_thresh[tmp_thresh > 1] = 1
        # tmp_thresh[tmp_thresh < 1] = 0
        # cnts, _ = cv2.findContours(tmp_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in cnts:
        #     cv2.drawContours(image,[cnt],-1,(255,0,255),5)
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(np.max(tmp_thresh))
        # tmp_thresh=np.squeeze(tmp_thresh,-1)
        # tmp_thresh=np.squeeze
        # tmp_thresh=np.dstack((tmp_thresh,tmp_thresh,tmp_thresh))
        # tmp_thresh=tmp_thresh[np.where(tmp_thresh>)==1]

        # tmp_thresh=np.resize(tmp_thresh,(650,1232,3))
        # plt.imshow(thresh)
        # plt.show()
        # overlay=(image+tmp_thresh)*0.6
        # overlay = image1 - image1 * (tmp_thresh * 0.3)
        # overlay[:, :, 0] += ((tmp_thresh * 255) * 0.3)[:, :, 0]
        # overlay=cv2.addWeighted(image,0.6,tmp_thresh,0.4,0)
        # overlay=np.array(overlay,dtype=np.uint8)
        # plt.imshow(overlay)
        # plt.show()
        #image_id=image_id[:-4]
        image_id=image_id[:-4]
        # plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask_ov.jpg',
        #            overlay, dpi=1)
        plt.imsave(path1 + "/" + image_id + '_mask.png', np.squeeze(mask) * 255, cmap='gray', dpi=1)



def predict_water_old(path1):
    data_path = path1+"/"
    print(data_path)
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        # print(ids)
        # print("###########")
        break

    for i in ids:
        if 'jpg'  in i:
            test_ids.append(i)
    # print(test_ids)
    # print(len(test_ids))

    for image_id in test_ids:
        image = cv2.imread(path1 + "/" + image_id)
        # os.remove(path1 + "/" + image_id)
        # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # print(geoimg)
        # image1=image
        image = cv2.cvtColor(image,cv2.COLOR_BGR2HLS)
        lower = np.array([75, 35, 15])
        upper = np.array([255,255,255])
        mask = cv2.inRange(image, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        # plt.imshow(mask)
        # plt.show()
        thresh = cv2.dilate(mask, None, iterations=1)
        #thresh = cv2.erode(thresh, None, iterations=2)

        # tmp_thresh=thresh
        # tmp_thresh[tmp_thresh > 1] = 1
        # tmp_thresh[tmp_thresh < 1] = 0
        # cnts, _ = cv2.findContours(tmp_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in cnts:
        #     cv2.drawContours(image,[cnt],-1,(255,0,255),5)
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(np.max(tmp_thresh))
        # tmp_thresh=np.squeeze(tmp_thresh,-1)
        # tmp_thresh=np.squeeze
        # tmp_thresh=np.dstack((tmp_thresh,tmp_thresh,tmp_thresh))
        # tmp_thresh=tmp_thresh[np.where(tmp_thresh>)==1]

        # tmp_thresh=np.resize(tmp_thresh,(650,1232,3))
        # plt.imshow(thresh)
        # plt.show()
        # overlay=(image+tmp_thresh)*0.6
        # overlay = image1 - image1 * (tmp_thresh * 0.3)
        # overlay[:, :, 0] += ((tmp_thresh * 255) * 0.3)[:, :, 0]
        # overlay=cv2.addWeighted(image,0.6,tmp_thresh,0.4,0)
        # overlay=np.array(overlay,dtype=np.uint8)
        # plt.imshow(overlay)
        # plt.show()
        #image_id=image_id[:-4]
        image_id=image_id[:-4]
        # plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask_ov.jpg',
        #            overlay, dpi=1)
        plt.imsave(path1 + "/" + image_id + '_mask.png', np.squeeze(thresh) * 255, cmap='gray', dpi=1)














def predict_water_Tiff_PL(path1):
    data_path = path1+"/"
    print(data_path)
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        # print(ids)
        # print("###########")
        break

    for i in ids:
        if 'jpeg' in i:
            test_ids.append(i)
    # print(test_ids)
    # print(len(test_ids))

    for image_id in test_ids:
        image = cv2.imread(path1 + "/" + image_id)
        #os.remove(path1 + "/" + image_id)
        # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # print(geoimg)
        # image1=image


        # image = cv2.cvtColor(image,cv2.COLOR_BGR2HLS)
        # lower = np.array([75, 35, 15])
        # upper = np.array([255,255,255])
        # mask = cv2.inRange(image, lower, upper)
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        # #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        # mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        # # plt.imshow(mask)
        # # plt.show()
        # thresh = cv2.dilate(mask, None, iterations=1)
        # #thresh = cv2.erode(thresh, None, iterations=2)

        th, msk = cv2.threshold(image, 45, 255, cv2.THRESH_BINARY)  # threshold range

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
        mask = cv2.bitwise_not(msk)



        # tmp_thresh=thresh
        # tmp_thresh[tmp_thresh > 1] = 1
        # tmp_thresh[tmp_thresh < 1] = 0
        # cnts, _ = cv2.findContours(tmp_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in cnts:
        #     cv2.drawContours(image,[cnt],-1,(255,0,255),5)
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(np.max(tmp_thresh))
        # tmp_thresh=np.squeeze(tmp_thresh,-1)
        # tmp_thresh=np.squeeze
        # tmp_thresh=np.dstack((tmp_thresh,tmp_thresh,tmp_thresh))
        # tmp_thresh=tmp_thresh[np.where(tmp_thresh>)==1]

        # tmp_thresh=np.resize(tmp_thresh,(650,1232,3))
        # plt.imshow(thresh)
        # plt.show()
        # overlay=(image+tmp_thresh)*0.6
        # overlay = image1 - image1 * (tmp_thresh * 0.3)
        # overlay[:, :, 0] += ((tmp_thresh * 255) * 0.3)[:, :, 0]
        # overlay=cv2.addWeighted(image,0.6,tmp_thresh,0.4,0)
        # overlay=np.array(overlay,dtype=np.uint8)
        # plt.imshow(overlay)
        # plt.show()
        #image_id=image_id[:-4]
        image_id=image_id[:-5]
        # plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask_ov.jpg',
        #            overlay, dpi=1)
        # plt.imsave(path1 + "/" + image_id + '_mask.png', np.squeeze(thresh) * 255, cmap='gray', dpi=1)
        plt.imsave(path1 + "/" + image_id + '_mask.png', np.squeeze(mask) * 255, cmap='gray', dpi=1)





def predict_water1(path1):
    data_path = path1+"/"
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        # print(ids)
        # print("###########")
        break

    for i in ids:
        if 'jpg' or 'png' in i:
            test_ids.append(i)
    # print(test_ids)
    # print(len(test_ids))

    for image_id in test_ids:
        im = cv2.imread(data_path + image_id)
        #image = cv2.imread('/home/ceinfo/Desktop/1/' + image_id + '.jpg')
        # os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
        image = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
        l_b = np.array([90, 74, 0])
        u_b = np.array([144, 255, 95])
        mask = cv2.inRange(image, l_b, u_b)
        mask2 = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.array((3, 3)), iterations=7)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.array((3, 3)), iterations=4)
        frame2 = cv2.bitwise_and(mask, mask2, mask=mask2)
        frame2 = cv2.morphologyEx(frame2, cv2.MORPH_CLOSE, np.array((3, 3)), iterations=7)
        frame2 = cv2.erode(frame2, (3, 3), iterations=3)
        cnts, _ = cv2.findContours(frame2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cnts = cv2.findContours(frame2, cv2.RETR_TREE)
        #cntss= cv2.findContours( cv2.CHAIN_APPROX_SIMPLE)
        print(cnts)
        dup = np.zeros(image.shape)
        for i in cnts:
            if cv2.contourArea(i) > 3800:
                cv2.drawContours(dup, [i], -1, (255, 255, 255), thickness=-1)
        # dup.dtype=np.unit8
        dup=np.array(dup,dtype=np.uint8)
        plt.imsave(path1 + "/" + image_id + '_mask.png', dup, cmap='gray', dpi=1)


def predict_water_Tiff_PL_old(path1):
    data_path = path1+"/"
    print(data_path)
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1

    ids = []
    test_ids = []
    for (dirpath, dirnames, filenames) in walk(data_path):
        ids.extend(filenames)
        # print(ids)
        # print("###########")
        break

    for i in ids:
        if 'jpeg' in i:
            test_ids.append(i)
    # print(test_ids)
    # print(len(test_ids))

    for image_id in test_ids:
        image = cv2.imread(path1 + "/" + image_id)
        #os.remove(path1 + "/" + image_id)
        # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
        # print(geoimg)
        # image1=image
        image = cv2.cvtColor(image,cv2.COLOR_BGR2HLS)
        lower = np.array([75, 35, 15])
        upper = np.array([255,255,255])
        mask = cv2.inRange(image, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        #mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        # plt.imshow(mask)
        # plt.show()
        thresh = cv2.dilate(mask, None, iterations=1)
        #thresh = cv2.erode(thresh, None, iterations=2)

        # tmp_thresh=thresh
        # tmp_thresh[tmp_thresh > 1] = 1
        # tmp_thresh[tmp_thresh < 1] = 0
        # cnts, _ = cv2.findContours(tmp_thresh,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        # for cnt in cnts:
        #     cv2.drawContours(image,[cnt],-1,(255,0,255),5)
        # image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(np.max(tmp_thresh))
        # tmp_thresh=np.squeeze(tmp_thresh,-1)
        # tmp_thresh=np.squeeze
        # tmp_thresh=np.dstack((tmp_thresh,tmp_thresh,tmp_thresh))
        # tmp_thresh=tmp_thresh[np.where(tmp_thresh>)==1]

        # tmp_thresh=np.resize(tmp_thresh,(650,1232,3))
        # plt.imshow(thresh)
        # plt.show()
        # overlay=(image+tmp_thresh)*0.6
        # overlay = image1 - image1 * (tmp_thresh * 0.3)
        # overlay[:, :, 0] += ((tmp_thresh * 255) * 0.3)[:, :, 0]
        # overlay=cv2.addWeighted(image,0.6,tmp_thresh,0.4,0)
        # overlay=np.array(overlay,dtype=np.uint8)
        # plt.imshow(overlay)
        # plt.show()
        #image_id=image_id[:-4]
        image_id=image_id[:-5]
        # plt.imsave("/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/" + image_id + '_mask_ov.jpg',
        #            overlay, dpi=1)
        plt.imsave(path1 + "/" + image_id + '_mask.png', np.squeeze(thresh) * 255, cmap='gray', dpi=1)





if __name__ == '__main__':
    predict_water()