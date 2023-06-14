from datasets1 import SlippyMapTiles
import numpy as np
import cv2
s = SlippyMapTiles('/mnt/vol1/PycharmProjects/robosat-master/datasets/training/images','/mnt/vol1/PycharmProjects/robosat-master/datasets/training/labels')
for i in s:
    print(i[1].shape)
    mask = np.expand_dims(i[1], axis=-1)
    mask = mask / 255
    mask[mask < 0.5] = 0
    mask[mask >= 0.5] = 1
    mask = np.array(mask, dtype=np.uint8)
    # print(i[2])
    break
img3=cv2.imread('/mnt/vol1/Deployment_projects/satellite_image_segmentation/sat_mask_crop/4428_1.jpg')
img3=cv2.cvtColor(img3,cv2.COLOR_BGR2GRAY)
# import cv2
# import numpy as np
import matplotlib.pyplot as plt
# import os
# import glob
# # img = cv2.imread('/mnt/vol1/PycharmProjects/robosat-master/datasets/training/labels/18/63916/120377.png')
#
# # img[img == [108,136,249]]=255
# # img[img != [255,255,255]]=0
# plt.subplots(1,2)
fig=plt.figure(figsize=(2,2))
fig.add_subplot(1,1,1)
plt.imshow(i[0])
fig.add_subplot(1,2,2)
plt.imshow(i[1])
fig.add_subplot(2,1,1)
plt.imshow(img3)
plt.show()
# # print(np.max(img[:,:,2]))
# import glob
# #278728
# num=1
# for path, subdirs, files in os.walk('/mnt/vol1/PycharmProjects/robosat-master/datasets/training/images/18'):
#     for name in files:
#         num=num+1
#         # print(os.path.join(path, name))
#         # files.append(os.path.join(path, name))
# # print(len(files))
# print(num)
# print(len(os.listdir('/mnt/vol1/PycharmProjects/robosat-master/datasets/training/labels/18')))