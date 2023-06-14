import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage import io


# image = cv2.imread("/home/ceinfo/Desktop/test_png/screenshot-map.png", 1)
# # Loading the image
#
# bigger = cv2.resize(image, (1000, 500))
#
# cv2.imwrite('test.png',bigger)

img=io.imread("/home/ceinfo/Desktop/test_png/screenshot-map.png")
# img2=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
image_name_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
image_name_rgb = cv2.resize(image_name_rgb, (1915, 935))

cv2.imwrite("/home/ceinfo/Desktop/test_png/screenshot-map_new.png",image_name_rgb)