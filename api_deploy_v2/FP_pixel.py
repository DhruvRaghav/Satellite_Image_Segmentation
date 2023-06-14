
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
import os


def predict_fp_pixel(path1,image_id):


	image = cv2.imread(os.path.join(path1,image_id+'.jpg'))


	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	boundaries = [([124,140,70], [170,250,250])]




	for (lower, upper) in boundaries:
					lower = np.array(lower, dtype="uint8")
					upper = np.array(upper, dtype="uint8")

					mask = cv2.inRange(image, lower, upper)
					kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
					mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=0)
					thresh = cv2.erode(mask, None, iterations=0)
					thresh = cv2.dilate(thresh, None, iterations=0)

					plt.imsave(os.path.join(path1,image_id+'_mask.png'), thresh, cmap='gray', dpi=1)

def predict_fp_pixel_tif(path1,image_id):


	image = cv2.imread(os.path.join(path1,image_id+'.jpeg'))


	image=cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
	boundaries = [([124,140,70], [170,250,250])]




	for (lower, upper) in boundaries:
					lower = np.array(lower, dtype="uint8")
					upper = np.array(upper, dtype="uint8")

					mask = cv2.inRange(image, lower, upper)
					kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
					mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=0)
					thresh = cv2.erode(mask, None, iterations=0)
					thresh = cv2.dilate(thresh, None, iterations=0)

					plt.imsave(os.path.join(path1,image_id+'_mask.png'), thresh, cmap='gray', dpi=1)

