import cv2
import numpy as np
import matplotlib.pyplot as plt

def predict_soil(path1,image_id):
    data_path = path1+"/"
    image = cv2.imread(path1 + "/" + image_id+".jpg")
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)

    lower = np.array([44, 6, 126])
    upper = np.array([252, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    thresh = cv2.erode(mask, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    plt.imsave(data_path + image_id + '_mask.png',
               thresh, cmap='gray', dpi=1)



def predict_soil_Tif_PL(path1,image_id):
    data_path = path1+"/"

    image = cv2.imread(path1 + "/" + image_id+".jpeg")
    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    lower = np.array([44, 6, 126])
    upper = np.array([252, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    thresh = cv2.erode(mask, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    plt.imsave(data_path + image_id + '_mask.png',
               thresh, cmap='gray', dpi=1)

