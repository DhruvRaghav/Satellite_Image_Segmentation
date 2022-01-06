import cv2
import numpy as np
import matplotlib.pyplot as plt

image = cv2.imread("/home/ceinfo/Downloads/tests/final_masks(Deeplab)/B7377.png")
new = cv2.imread("/home/ceinfo/Downloads/tests/images2/B7377.jpg")
paper = image.copy()
black = np.zeros(paper.shape, dtype=np.uint8)
# img = np.zeros((512,512,3), np.uint8)
ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)

thresh_gray = cv2.morphologyEx(thresh_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (71, 71)))
plt.imshow(thresh_gray)
plt.show()
cont, hier = cv2.findContours(thresh_gray, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

for c in cont:
    area = cv2.contourArea(c)
    # print(area)
    if area < 2000:
        # cv2.drawContours(paper, [c], 0, (0, 0, 0), -1)
        continue
    # print(area)
    epsilon = 0.0001 * cv2.arcLength(c, True)
    approx = cv2.approxPolyDP(c, epsilon, True)
    cv2.drawContours(new, [approx], 0, (0, 255, 0), 7)
    cv2.drawContours(black, [approx], 0, (255, 255, 255), 5)

# cv2.imshow('output', new)
cv2.imwrite('output.jpg', new)
cv2.imwrite('black.jpg', black)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# def getXYtoLatLng(x,y,img_pixel_width,img_pixel_height,zoom,center_lat,center_lng):


# convert pixel
