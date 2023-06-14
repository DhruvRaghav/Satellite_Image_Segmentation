import cv2
from skimage import draw

# read the image
import numpy as np
import skimage

image = cv2.imread('/home/ceinfo/Desktop/uploads03/filename2022-07-01_14:46:36_966454_mask.png')

# B, G, R channel splitting
blue, green, red = cv2.split(image)

# detect contours using blue channel and without thresholding
_,contours1, hierarchy1 = cv2.findContours(image=blue, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# draw contours on the original image
image_contour_blue = image.copy()
cv2.drawContours(image=image_contour_blue, contours=contours1, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
# see the results
cv2.imshow('Contour detection using blue channels only', image_contour_blue)
cv2.waitKey(0)
cv2.imwrite('/home/ceinfo/Desktop/hello/blue_channel.jpg', image_contour_blue)
cv2.destroyAllWindows()

# detect contours using green channel and without thresholding
_, contours2, _= cv2.findContours(image=green,mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# contours2, hierarchy2 = cv2.findContours(image=green, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
# draw contours on the original image
image_contour_green = image.copy()
cv2.drawContours(image=image_contour_green, contours=contours2, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
# see the results
cv2.imshow('Contour detection using green channels only', image_contour_green)
cv2.waitKey(0)
cv2.imwrite('/home/ceinfo/Desktop/hello/green_channel.jpg', image_contour_green)
cv2.destroyAllWindows()

# detect contours using red channel and without thresholding
_, contours3, _= cv2.findContours(image=red,mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)

# contours3, hierarchy3 = cv2.findContours(image=red, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
# draw contours on the original image
image_contour_red = image.copy()
cv2.drawContours(image=image_contour_red, contours=contours3, contourIdx=-1, color=(0, 255, 0), thickness=0, lineType=cv2.LINE_AA)
# see the results
cv2.imshow('Contour detection using red channels only', image_contour_red)
cv2.waitKey(0)
cv2.imwrite('/home/ceinfo/Desktop/hello/red_channel.jpg', image_contour_red)
cv2.destroyAllWindows()

# Load the original image
image = cv2.imread("/home/ceinfo/Desktop/hello/red_channel.jpg")

# Create the basic mask
mask = np.ones(shape=image.shape[0:2], dtype="bool")

# Draw a filled rectangle on the mask image
rr, cc = skimage.draw.rectangle(start=(357, 44), end=(740, 720))
c=mask[rr, cc] = False
cv2.imwrite('/home/ceinfo/Desktop/hello/red_channel.jpg', rr)
cv2.imwrite('/home/ceinfo/Desktop/hello/red_channel.jpg', cc)
# cv2.imwrite('/home/ceinfo/Desktop/hello/red_channel.jpg', c)



