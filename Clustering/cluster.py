import matplotlib.pyplot as plt
import cv2
import numpy as np

image = cv2.imread("/home/ceinfo/Downloads/habitat_Test/2021-12-30/5722.png")
paper = image.copy()
real = cv2.imread("/home/ceinfo/Downloads/habitat_Test/images/5722.jpg")
abc = real.copy()
ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)
contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for c in contours:
    area = cv2.contourArea(c)

    if area < 1000:
        cv2.fillPoly(thresh_gray, pts=[c], color=1)
        continue

    rect = cv2.minAreaRect(c)

thresh_gray = cv2.morphologyEx(thresh_gray, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (91, 91)))
# plt.imshow(thresh_gray)
# plt.show()

contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

for c in contours:
    area = cv2.contourArea(c)

    if area < 2000:
        cv2.fillPoly(thresh_gray, pts=[c], color=0)
        continue

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)

    box = np.int0(box)
    cv2.drawContours(paper, [box], 0, (255, 255, 255), -1)

_, thresh_gay = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)
plt.imshow(thresh_gay)
plt.show()

contours, hier = cv2.findContours(thresh_gay, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
# print(contours)
for c in contours:
    # print(c)
    area = cv2.contourArea(c)

    # if area < 2000:
    #     cv2.fillPoly(thresh_gray, pts=[c], color=0)
    #     continue

    rect = cv2.minAreaRect(c)
    box = cv2.boxPoints(rect)

    box = np.int0(box)
    cv2.drawContours(abc, [box], 0, (0, 255, 0), 7)

# cv2.imshow('output', abc)
cv2.imwrite('output.jpg', abc)
cv2.waitKey(0)
cv2.destroyAllWindows()
