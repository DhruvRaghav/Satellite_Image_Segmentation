import cv2
import numpy as np

#load the satellite image
img = cv2.imread("/home/ceinfo/Pictures/SAT_IMAGES/1234.png")

#convert to grayscale
gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#apply canny edge detection
edges = cv2.Canny(gray_img,50,200)

#find contours
_,cnts, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#iterate to find the contours with large area
building_contours = []
for c in cnts:
    area = cv2.contourArea(c)
    if area > 400:
        building_contours.append(c)

#draw the contours on the image
cv2.drawContours(img, building_contours, -1, (0,255,0), 3)

#save the image
cv2.imwrite("building_footprints_detected.jpg", img)