import numpy as np
import cv2
import matplotlib.pyplot as plt

def predict_veg(path1,image_id):
        print(path1)
        image = cv2.imread(path1+ "/" + image_id + '.jpg')
        lower = np.array([30, 30, 20])
        upper = np.array([255, 255, 100])
        mask = cv2.inRange(image, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        thresh = cv2.erode(close, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)
        plt.imsave(path1+"/"+image_id+'_mask.png',thresh, cmap='gray', dpi=1)


def predict_veg_Tif_PL(path1,image_id):
        image = cv2.imread(path1+ "/" + image_id + '.jpeg')
        lower = np.array([30, 30, 20])
        upper = np.array([255, 255, 100])
        mask = cv2.inRange(image, lower, upper)
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        thresh = cv2.erode(close, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)
        plt.imsave(path1+"/"+image_id+'_mask.png',thresh, cmap='gray', dpi=1)




