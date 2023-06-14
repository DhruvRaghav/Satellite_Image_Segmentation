# import the necessary packages
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())


# load the image
#image = cv2.imread('C:/Users/dhruv/Desktop/images/MGIS VISION/bhuvan/300.jpg')
image = cv2.imread('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_pixel/api_deploy/uploads03/12021-07-13_17:31:54_421831.jpg')


# define the list of boundaries
''' building'''
image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
boundaries = [([124,140,70], [170,250,250])]




for (lower, upper) in boundaries:
				# create NumPy arrays from the boundaries
				lower = np.array(lower, dtype="uint8")
				upper = np.array(upper, dtype="uint8")
				# find the colors within the specified boundaries and apply
				# the mask
				mask = cv2.inRange(image, lower, upper)
				kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
				mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=0)
				thresh = cv2.erode(mask, None, iterations=0)
				thresh = cv2.dilate(thresh, None, iterations=0)
				# plt.imshow(thresh)
				# plt.show()
				#plt.imsave("C:/Users/dhruv/Desktop/images/MGIS VISION/bhuvan/"+ '300.png',thresh, cmap='gray', dpi=1)
				plt.imsave('500.png', thresh, cmap='gray', dpi=1)

				# 		   thresh, cmap='gray', dpi=1)

				#cv2.imshow("mask", thresh)
				#cv2.waitKey(0)
				#output = cv2.bitwise_and(image, image, mask = thresh)
				# show the images
				#cv2.imshow("images", np.hstack([image, output]))
				#cv2.waitKey(0)

