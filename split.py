import cv2
import numpy as np
import matplotlib.pyplot as plt
img=cv2.imread(r"/home/prateek/Downloads/satellite_change_detection/IMG_02/T43RGM_02102018.tif")
start=0
end=1000
for i in range(0,10):
    end=0
    for j in range(0,10):
        img1=img[start:start+1000,end:end+1000,:]
        # plt.imshow(img1)
        # plt.show()
        end=end+1000
        cv2.imwrite('split_images/'+str(i)+'_'+str(j)+'.jpg',img1)
    start = start + 1000
# plt.imshow(img1)
# plt.show()
