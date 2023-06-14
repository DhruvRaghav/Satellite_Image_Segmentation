import cv2
import numpy as np
from numpy import asarray

# Load image, convert to grayscale, and find edges
# image = cv2.imread('image_thres1.jpg')
import os

'''images path'''
data_path = '/mnt/vol1/DhruvRaghav/dataset/building/all_image/'
'''mask path '''
data_path1 = '/mnt/vol1/DhruvRaghav/dataset/building/data_regioWise_mask/'


def func1():

    '''--------------------------------------------------------------------------'''

    path = os.getcwd()
    print(path)
    directory = "output_images"
    parent_dir = path
    path1 = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path1, exist_ok=True)
    except OSError as error:
        pass
    '''--------------------------------------------------------------------------'''

    for image_id in os.listdir(data_path1):
        print(image_id)
        # im = Image.open(os.path.join(data_path1, image_id))
        # im2 = Image.open(os.path.join(data_path, image_id))

        img = cv2.imread(os.path.join(data_path1, image_id))

        img2 = cv2.imread(os.path.join(data_path, image_id))


        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)[1]

        # Find contour and sort by contour area
        # cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        _,cnts, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


        # Find bounding box and extract ROI
        for c in cnts:
            x,y,w,h = cv2.boundingRect(c)
            ROI = img2[y:y+h, x:x+w]
            # break

            # cv2.imshow('ROI',ROI)
            # cv2.imwrite('ROI.png',ROI)
            # cv2.waitKey()
            average_color_row = np.average(ROI, axis=0)
            # average_color_row = np.(ROI, axis=0)

            average_color = np.average(average_color_row, axis=0)
            # print(average_color)    #
            # d_img = np.ones((312,312,3), dtype=np.uint8)
            # d_img[:,:] = average_color

            # cv2.imwrite('image.jpg', d_img)
            cv2.drawContours(img2,c, -1, (255,255,255), 2, cv2.QT_CHECKBOX)
            cv2.fillPoly(img2, pts=[c], color=average_color)
            # cv2.imwrite('image_thr.jpg', image2)
            # dst = cv2.addWeighted(image2, 0.7, asarray(d_img), 0.3, 0)
        cv2.imwrite("output_images/"+ image_id,img2)

if __name__ == '__main__':
    func1()