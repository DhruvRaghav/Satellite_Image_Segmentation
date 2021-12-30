# import matplotlib.pyplot as plt
# img = plt.imread("/home/ceinfos/Downloads/Untitled Folder/4428.jpg")
# fig, ax = plt.subplots()
# ax.imshow(img)
# fig, ax = plt.subplots()
# x = range(300)
# ax.imshow(img, extent=[0, 400, 0, 300])
# ax.plot(x, x, '--', color='firebrick')

import numpy as np
import cv2
# import skimage
import pandas as pd
import os
import math
# fig, (ax1, ax2) = plt.subplots(ncols=2, nrows=1, figsize=(10, 6))
# Create a black image

'''*************************FOR ROADS ************************************************ '''
data=pd.read_csv('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/rd_test.csv')
path='/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/satellite_road_images/'



files = []
fileName=[]
exts = ['jpg', 'png', 'jpeg', 'JPG']

for parent, dirnames, filenames in os.walk(path):
    print('directory image path--',parent)
    for filename in filenames:
        #print(filename[:-4])
        #dirpath='/home/ceinfos/Documents/Textfiles(ENG)/newdata/'+filename[:-4]
        #print('directory image store path--',dirpath)
        #os.makedirs(dirpath)
        for ext in exts:
            if filename.endswith(ext):
                files.append(os.path.join(parent, filename))
                fileName.append(filename[:-4])
                break
print('Find {} images'.format(len(files)))
print(files)
for i in range(len(fileName)):
    img_1 = np.array(cv2.imread(files[i]))
    img = np.zeros(img_1.shape, dtype=np.uint8)
    print(fileName[i])
    try:
        filter = data[data['GridNo'] == int(fileName[i])][:]
    except Exception as e:
        continue
    print(filter)
    filter.index = range(len(filter))
    pts=[]
    for j in range(0,len(filter)-1):
        edge_id=filter['EDGE_ID'][j]
        if(j==len(filter)):
            pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
            pts = np.array(pts)
            print(pts)
        if(edge_id==filter['EDGE_ID'][j+1]):
            pts.append([abs(math.ceil(filter['CentroidX'][j])),abs(math.ceil(filter['CentroidY'][j]))])
        else:
            pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
            pts = np.array(pts)
            print(pts)
            # pts = pts.reshape((-1,1,2))
            cv2.polylines(img, [pts], True, (255, 255, 255),thickness=10)
            pts = []
        # cv2.line(img,(math.ceil(filter['CentroidX'][j]),math.ceil(filter['CentroidY'][j])),(math.ceil(filter['CentroidX'][j+1]),math.ceil(filter['CentroidY'][j+1])),(255,255,255),20)
    save_img='/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/rd_masks/{}.jpg'.format(fileName[i])
    cv2.imwrite(save_img, img)
# img = np.zeros((512,512,3), np.uint8)
# img = np.zeros((3705, 4800, 3), dtype=np.uint8)
# Draw a diagonal blue line with thickness of 5 px
# cv2.line(img,(3088+2,3589+1),(2820+2,3384+1 ),(255,0,0),20)
# cv2.line(img,(3608,2333),(3612,2099 ),(255,0,0),20)
# ax1.imshow(img)
# skimage.io.imsave('/home/ceinfos/Downloads/Untitled Folder/road1.jpg',img)