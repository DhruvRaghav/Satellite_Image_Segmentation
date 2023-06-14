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

def predict_veg(image,image_id):
        # image = cv2.imread('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
        # os.remove('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/' + image_id + '.png')
# image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
# print(geoimg)
        img=cv2.imread(image)
        # img=image
        Image_pil=Image.open(image)
        # print(image)
        # print(img.shape)
        # image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lower = np.array([10, 5, 15])
        upper = np.array([170, 170, 150])
        mask = cv2.inRange(img,lower,upper)
        #plt.imshow(mask)
        # plt.show()
        res = cv2.bitwise_or(img, upper, mask=mask)
        # plt.imshow(res)
        # plt.show()

        thresh = cv2.erode(res, None, iterations=1)
        thresh = cv2.dilate(thresh, None, iterations=1)



        # thresh = cv2.erode(mask, None, iterations=3)
        # thresh = cv2.dilate(thresh, None, iterations=3)
        #plt.imshow(thresh)
        #plt.show()

        # Image_pil=Image.eval(image)
        plt.imsave(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/veg_overlay_code/Veg_Mask/" + str(image_id) + '_mask.jpg',thresh, cmap='gray', dpi=1)
        Image_pil2=Image.open(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/veg_overlay_code/Veg_Mask/" + str(image_id) + '_mask.jpg')

        alphaBlended1 = Image.blend(Image_pil,Image_pil2, alpha=.5)
        alphaBlended1=alphaBlended1.save(r"/mnt/vol1/Deployment_projects/satellite_image_segmentation/veg_overlay_code/Veg_overlay/" + str(image_id) + '_mask.jpg')
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
img_name='/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/4428.jpg'
# img=cv2.imread('uploads/4428.jpg')
# print(img)
# data_path="split_image"
# files=os.listdir(data_path)
# print(files)
# files=[os.path.join(data_path,f) for f in files]
# for i,image in enumerate(files):
        # print(image)
predict_veg(img_name,1)
# print(files)
