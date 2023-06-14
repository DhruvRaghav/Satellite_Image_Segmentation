# Write a python script to generate masks from geojson and image

# import json
# import sys
# import os
# import numpy as np
# from PIL import Image
# import matplotlib.pyplot as plt
# import cv2
#
# #Loading the image
# img = cv2.imread('/mnt/vol2/Dhruv_Raghav/habitation_2k22/Habit_IMG_Grid/1_data.png')
# #Loading the geojson
# with open('/mnt/vol2/Dhruv_Raghav/habitation_2k22/Habit_IMG_Grid/1_data.geojson') as f:
#   data = json.load(f)
#   print(data)
#
# #converting the geojson to list
# geo_list = data['Locations']['features']
# print(geo_list)
#
# #extracting coordinates from the geojson
# coords = geo_list[0]['geometry']['coordinates'][0]
#
# #Converting the list of coordinates to numpy array
# array = np.array(coords)
#
# #getting the shape of the image
# height, width, _ = img.shape
#
# #Converting the numpy array to list
# points = array.tolist()
#
# #Converting the list of points to integer
# points_int = [[int(i[0]*width),int(i[1]*height)]for i in points]
#
# #finding the min-x, min-y, max-x and max-y
# xs, ys = zip(*points_int)
# min_x, min_y = min(xs), min(ys)
# max_x, max_y = max(xs), max(ys)
#
# #Creating a mask
# mask = np.zeros(img.shape)
#
# #filling the polygon
# cv2.fillPoly(mask, [np.array(points_int)], (255, 255, 255))
#
# #applying the mask to the image
# result = cv2.bitwise_and(img, mask)
# # cvtColor(mask, canny, CV_RGB2GRAY);
#
# #displaying the image
# plt.imshow(result)
# plt.show()

'''==='''
import json
import numpy as np
from PIL import Image

with open('/mnt/vol2/Dhruv_Raghav/habitation_2k22/Habit_IMG_Grid/1_data.geojson') as f:
    data = json.load(f)

im = Image.open('/mnt/vol2/Dhruv_Raghav/habitation_2k22/Habit_IMG_Grid/1_data.png')

for feature in data['Locations']['features']:
    coords = feature['geometry']['coordinates']
    imarray = np.asarray(im)
    mask = np.zeros(imarray.shape)
    for coord in coords:
        x, y = coord
        mask[x, y] = 1
    mask = Image.fromarray(mask)
    mask.save('mask_{}.png'.format(feature['id']))