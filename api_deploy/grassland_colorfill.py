import numpy as np
import cv2
from scipy.spatial.distance import euclidean
import matplotlib.pyplot as plt
import pandas as pd
import geoio
import math
from imutils import perspective
import imutils


image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1.PNG')
geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1580117884006.png')
print(geoimg)
#
image = cv2.cvtColor(image, cv2.COLOR_BGR2HLS)
plt.imshow(image)
plt.show()

lower = np.array([0, 0, 0])
upper = np.array([23,114,69])
mask = cv2.inRange(image,lower,upper)
plt.imshow(mask)
plt.show()
res = cv2.bitwise_and(image,upper, mask= mask)
plt.imshow(res)
plt.show()

thresh = cv2.erode(res, None, iterations=2)
thresh = cv2.dilate(thresh, None, iterations=2)
plt.imshow(thresh)
plt.show()


cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

cnts = cnts[0] if len(cnts) == 2 else cnts[1]
bounding = []
bounding1 =[]
Moment = []
centroid1 = []

for i in cnts:
        print("i:",i)

        x1, y1 = geoimg.raster_to_proj(i[0][0][0] ,i[0][0][1])

        draw = cv2.drawContours(image, [i], -1, (0, 0, 255), 3)

        c = max(cnts, key=cv2.contourArea)

        #cv2.drawContours(image, [c], -1, (0, 255, 255), 3)


plt.imshow(image)
plt.show()
