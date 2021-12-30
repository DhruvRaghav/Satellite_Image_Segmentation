import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import os
from PIL import Image




import pandas as pd
# import geoio
# import math
# from imutils import perspective
# import imutils

def predict_veg(image,image_id,image_mask):
        # image = cv2.imread('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
        # os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
# image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# print(geoimg)
        img=cv2.imread(image)
        Image_pil=Image.open(image)
        # print(image)
        # print(img.shape)
        image = cv2.cvtColor(img, cv2.COLOR_RGB2XYZ)
        lower = np.array([30, 30, 35])
        upper = np.array([170,170, 150])
        mask = cv2.inRange(img,lower,upper)
        #plt.imshow(mask)
        # plt.show()


        thresh = cv2.erode(mask, None, iterations=3)
        thresh = cv2.dilate(thresh, None, iterations=3)
        #plt.imshow(thresh)
        #plt.show()

        # Image_pil=Image.eval(image)
        plt.imsave(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/split_predictions/" + str(image_mask),thresh, cmap='gray', dpi=1)
        Image_pil2=Image.open(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/split_predictions/" + str(image_mask))

        alphaBlended1 = Image.blend(Image_pil, Image_pil2, alpha=.4)
        alphaBlended1=alphaBlended1.save(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/split_predictions_overlay/" + str(image_mask))
        # alphaBlended2 = Image.blend(image5, image6, alpha=.4)

        # alpha = 0.6
        # new_mask = np.squeeze(thresh)
        # color_mask = np.dstack((new_mask, new_mask, new_mask))
        #
        # image = image - image * (color_mask * 0.3)
        # image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
        # print(image)


        # cv2.imwrite(r"C:\Users\Madhusudhan\Downloads\yolact-master\split_predictions_overlay/" + str(image_id) + '_mask.jpg',alphaBlended1)
        #
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
import os
img=cv2.imread(r'/home/prateek/Downloads/satellite_change_detection/IMG_02/T43RGM_02102018.tif')
# print(img)
data_path=r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/split_images"
file_names=os.listdir(data_path)
print(file_names)
files=[os.path.join(data_path,f) for f in file_names]
for i,image in enumerate(files):
        # print(image)
        predict_veg(image,i,os.path.basename(image))
print(files)
