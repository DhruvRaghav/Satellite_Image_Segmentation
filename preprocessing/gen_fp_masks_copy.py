
import numpy as np
import cv2
# import skimage
import pandas as pd
import os
import math

data=pd.read_csv('/home/ceinfo/Desktop/test/fp_test.csv')
path='/home/ceinfo/Desktop/test/hi/'
files = []
fileName=[]
exts = ['jpg', 'png', 'jpeg', 'JPG']

for parent, dirnames, filenames in os.walk(path):
    print('directory image path--',parent)
    for filename in filenames:

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
        # if(j==len(filter)):
        #     pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
        #     pts = np.array(pts)
        # if(edge_id==filter['EDGE_ID'][j+1]):
        # pts.append([abs(math.ceil(filter['CentroidX'][j])),abs(math.ceil(filter['CentroidY'][j]))])
        # else:
        pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
        #     pts = np.array(pts)
    pts = np.array(pts)

    # print("hiiii",pts)
    img=cv2.fillConvexPoly(img,pts,(255, 255, 255))
    save_img='/home/ceinfo/Desktop/test/{}.jpg'.format(fileName[i])

    # save_img='/home/ceinfo/Desktop/test/'{}.jpg.format(fileName[i])
    cv2.imwrite(save_img, img)
