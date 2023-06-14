import cv2
import numpy as np
import os

def google_50_100(path1, image_name):

    input_path = os.path.join(path1, image_name+".jpg")
    img = cv2.imread(input_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    mask = cv2.inRange(img, (0, 0, 0), (25, 25, 100))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

    close = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=2)

    count = cv2.countNonZero(close)
    total = img.shape[0] * img.shape[1]

    per = (count / total) * 100
    # print('Percentage of pixels :', per)

    if per <= 1.9:
        mask = cv2.inRange(img, (35, 79, 65), (49, 100, 87))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)
        count = cv2.countNonZero(close)
        total = img.shape[0] * img.shape[1]

        per = (count / total) * 100

    if per <= 1.9:
        mask = cv2.inRange(img, (0, 0, 0), (49, 100, 100))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    xmask = np.ones(img.shape[:2], dtype="uint8") * 255
    for i in cnts:
        # print('area ', end=" ")
        area = cv2.contourArea(i)
        # print(area)
        if area > 8000:
            cv2.drawContours(xmask, [i], -1, 0, -1)
    xmask = cv2.bitwise_not(xmask)

    out_file = image_name.split(".")[0]
    cv2.imwrite(os.path.join(path1, out_file) + "_mask.png", xmask)


def google_200(path1, image_name):

    input_path = os.path.join(path1, image_name+".jpg")
    img = cv2.imread(input_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    mask = cv2.inRange(img, (0, 0, 0), (30, 80, 250))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    count = cv2.countNonZero(close)
    # print(count)
    total = img.shape[0] * img.shape[1]
    # print(total)

    per = (count / total) * 100
    # print('Percentage of pixels :', per)

    if per <= 0.9:
        mask = cv2.inRange(img, (0, 0, 0), (80, 120, 200))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    xmask = np.ones(img.shape[:2], dtype="uint8") * 255
    for i in cnts:
        # print('area ', end=" ")
        area = cv2.contourArea(i)
        # print(area)
        if area > 4000:
            cv2.drawContours(xmask, [i], -1, 0, -1)
    xmask = cv2.bitwise_not(xmask)
    out_file=image_name.split(".")[0]
    cv2.imwrite(os.path.join(path1,out_file)+"_mask.png", xmask)


def bhuwan_50(path1, image_name):
    input_path = os.path.join(path1, image_name+".jpg")
    img = cv2.imread(input_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    mask = cv2.inRange(img, (0, 0, 0), (50, 60, 255))
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    xmask = np.ones(img.shape[:2], dtype="uint8") * 255
    for i in cnts:
        # print('area ', end=" ")
        area = cv2.contourArea(i)
        # print(area)
        if area > 8000:
            cv2.drawContours(xmask, [i], -1, 0, -1)
    xmask = cv2.bitwise_not(xmask)

    f1=image_name.split(".")[0]
    cv2.imwrite(os.path.join(path1,f1)+"_mask.png", xmask)


def noise(msk, x):
    cnts = cv2.findContours(msk, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    xmask = np.ones(x.shape[:2], dtype="uint8") * 255
    for i in cnts:
        # print('area ', end=" ")
        area = cv2.contourArea(i)
        # print(area)
        if area > 2000:
            cv2.drawContours(xmask, [i], -1, 0, -1)
    return cv2.bitwise_not(xmask)


def bhuwan_100_200(path1, image_name):

    input_path = os.path.join(path1, image_name+".jpg")
    img = cv2.imread(input_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()
    mask = cv2.inRange(img, (0, 20, 50), (77, 70, 255))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    count = cv2.countNonZero(close)
    total = img.shape[0] * img.shape[1]
    per = (count / total) * 100

    if per <= 9:
        mask = cv2.inRange(img, (0, 0, 1), (20, 35, 255))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    xmask = noise(close, img)

    count = cv2.countNonZero(xmask)
    total = img.shape[0] * img.shape[1]
    per = (count / total) * 100
    # print('Percentage of pixels :', per)
    if per < 1:
        mask = cv2.inRange(img, (0, 0, 0), (60, 60, 255))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

        xmask = noise(close, img)

    f1=image_name.split(".")[0]
    cv2.imwrite(os.path.join(path1,f1)+"_mask.png", xmask)

def bhuwan_300(path1, image_name):

    input_path = os.path.join(path1, image_name+".jpg")
    print(input_path)
    img = cv2.imread(input_path)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_copy = img.copy()

    mask = cv2.inRange(img, (0, 0, 30), (75, 65, 255))

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=0)
    close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    count = cv2.countNonZero(close)
    total = img.shape[0] * img.shape[1]
    per = (count / total) * 100
    # print('Percentage of pixels :', per)

    if per >= 36:
        mask = cv2.inRange(img, (0, 0, 1), (20, 35, 255))

        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

        opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel2, iterations=2)
        close = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel, iterations=2)

    cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    xmask = np.ones(img.shape[:2], dtype="uint8") * 255
    for i in cnts:
        # print('area ', end=" ")
        area = cv2.contourArea(i)
        # print(area)
        if area > 900:
            cv2.drawContours(xmask, [i], -1, 0, -1)

    xmask = cv2.bitwise_not(xmask)
    f1 = image_name.split(".")[0]
    cv2.imwrite(os.path.join(path1, f1) + "_mask.png", xmask)


if __name__ == '__main__':
    bhuwan_300('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_pixel/api_deploy/uploads03','filename.jpg')