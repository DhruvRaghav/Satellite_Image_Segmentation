import numpy as np
import cv2
from os import walk
import pandas as pd
import matplotlib.pyplot as plt
# img = cv2.imread('/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/predicted_images_link_jacard_int_azam_submit/2019-07-11/5756.jpg')
# # img = cv2.resize(img, (400, 500))
# data_path="/mnt/vol1/Datasets/Satellite_Images/SampleSatelliteImages/Delhi NCR Part-4035_04Dec2016"
# ids=[]
# for (dirpath, dirnames, filenames) in walk(data_path):
#     ids.extend(filenames)
#     break
# test_ids=[]
# for i in ids:
#     if 'jpg' in i:
#         test_ids.append(i)
# counts=[]
# print(test_ids)
# for image_id in test_ids:
#     img = cv2.imread("/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/predicted_images_link_jacard_int_Delhi_NEW_vggmodel/2019-07-11/"+image_id)
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     ret, gray = cv2.threshold(gray, 127, 255, 0)
#     gray2 = gray.copy()
#     mask = np.zeros(gray.shape, np.uint8)
#     _,contours, hier = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     counts.append(len(contours))
#     print(len(contours))
# d={'ImageId':test_ids,'Count':counts}
# data = pd.DataFrame(d,columns=['ImageId', 'Count'])
# data.to_csv('count_vgg.csv')
    # for cnt in contours:
    #     # if 200 < cv2.contourArea(cnt) < 5000:
    #     if cv2.contourArea(cnt)<100:
    #         (x, y, w, h) = cv2.boundingRect(cnt)
    #         cv2.rectangle(mask, (x, y), (x + w, y + h),(255,255,255),cv2.FILLED)
    #         # print(cnt)
    #         # new=[]
    #         # new.append([x,y])
    #         # new.append([x,y+h])
    #         # new.append([x+w,y])
    #         # new.append([x+w,y+h])
    #         # new=np.asarray(new)
    #     else:
    #         # cv2.fillPoly(img, pts=[new], color=(255, 255, 255))
    #         cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)
    #         cv2.drawContours(mask, [cnt], 0, 255, -1)
    # print(cnt)
    # # new_mask = np.squeeze(mask, -1)
    # new_mask=mask/255
    # color_mask = np.dstack((new_mask, new_mask, new_mask))
    #
    # image = image - image * (color_mask * 0.3)
    # image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
    # cv2.imwrite("infi.jpg",mask)
    # cv2.imwrite("infi_ori.jpg",image)
import cv2
import numpy as np

img = cv2.imread('/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/predicted_images_link_jacard_int_azam_submit/2019-07-11/5756.jpg')
# img = cv2.resize(img,(4,500))
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,gray = cv2.threshold(gray,127,255,0)
gray2 = gray.copy()
mask = np.zeros(gray.shape, np.uint8)

_,contours, hier = cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
print(contours[0][0],hier)
cv2.line(mask,tuple(contours[0][0][0]),tuple(contours[0][1][0]),color=(255))
# cv2.line(mask,tuple(contours[0][2][0]),tuple(contours[0][3][0]),color=(255))
# cv2.line(mask,tuple(contours[0][4][0]),tuple(contours[0][5][0]),color=(255))
# cv2.line(mask,tuple(contours[0][6][0]),tuple(contours[0][7][0]),color=(255))
# cv2.line(mask,tuple(contours[0][8][0]),tuple(contours[0][9][0]),color=(255))
# cv2.line(mask,tuple(contours[0][10][0]),tuple(contours[0][0][0]),color=(255))
# for cnt in contours:
    # if 1000<cv2.contourArea(cnt)<5000:
        # (x,y,w,h) = cv2.boundingRect(cnt)
        # cv2.rectangle(gray2,(x,y),(x+w,y+h),0,-1)
        # s=cv2.fillConvexPoly(mask,cnt,color=(255))
plt.imshow(gray2)
cv2.imwrite("infi.jpg",mask)
cv2.imwrite("infi_gray.jpg",gray)
# cv2.waitKey(0)
# cv2.destroyAllWindows()