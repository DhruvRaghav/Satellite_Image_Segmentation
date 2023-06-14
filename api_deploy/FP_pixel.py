
import numpy as np
import argparse
import cv2
import matplotlib.pyplot as plt
import os
import base64
import json

def predict_fp_pixel(path1,image_id,bounds):


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
					with open(path1 + "/" + image_id + '.jpg', "rb") as r1:
						converted_string = base64.b64encode(r1.read())
					# converted_string.decode("utf-8")
					# print(converted_string)
					# print(converted_string.decode('utf-8'))

					with open('encode.bin', "wb") as file:
						file.write(converted_string)

					with open(path1 + "/" + image_id + '_mask.png', "rb") as r:
						converted_string_1 = base64.b64encode(r.read())
					# converted_string_1.decode("utf-8")
					# print(converted_string_1)
					# print(converted_string.decode('utf-8'))

					with open('encode_1.bin', "wb") as file:
						file.write(converted_string_1)

					c = {"1": converted_string, "2": converted_string_1}
					json_str = json.dumps(
						{'I M A G E': converted_string.decode('utf-8'), 'M A S K': converted_string_1.decode(('utf-8')),
						 "BOUNDS": bounds})

					return json_str


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

