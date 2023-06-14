import cv2
import base64
import numpy as np
import os
from PIL import Image
#from os import walk
import cv2
from os import walk
import matplotlib.pyplot as plt
import os

'''images path'''
data_path = '/mnt/vol1/DhruvRaghav/dataset/building/all_image/'
'''mask path '''
data_path1 = '/mnt/vol1/DhruvRaghav/dataset/building/data_regioWise_mask/'
def func_1():
    path = os.getcwd()
    print(path)
    directory = "output_images"
    parent_dir = path
    path1 = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass

    for image_id in os.listdir(data_path1):
        print(image_id)
        # im = Image.open(os.path.join(data_path1, image_id))
        # im2 = Image.open(os.path.join(data_path, image_id))

        img = cv2.imread(os.path.join(data_path1, image_id))
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # blurred = cv2.GaussianBlur(gray,
        #                            (15, 15), 6)

        ret, thresh = cv2.threshold(gray,
                                    180, 255,
                                    cv2.THRESH_BINARY)


        image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        img2 = cv2.imread(os.path.join(data_path, image_id))

        for c in contours:
            # if the contour is not sufficiently large, ignore it
            # if  cv2.contourArea(c) < 2000:
            #     continue

            # get the min area rect
            # rect = cv2.minAreaRect(c)
            # box = cv2.boxPoints(rect)
            # convert all coordinates floating point values to int
            # box = np.int0(c)
            # draw a red 'nghien' rectangle
            # print(c)
            epsilon = 0.001 * cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.1, True)
            cv2.drawContours(img2, [approx], 0, (0, 0, 255), 1)
        cv2.imwrite("output_images/"+ image_id,img2)
            # cv2.imshow("contours", img2)


if __name__ == '__main__':
    func_1()
