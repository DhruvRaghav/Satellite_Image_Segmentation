# # write a python script to convert mask in an image  into regularized mask
# import matplotlib as plt
# import cv2
# import numpy as np
#
# #read the image
# img = cv2.imread('/mnt/vol2/Dhruv_Raghav/Satellite_image_segmentation_everything/satellite_image_segmentation/sample_Results/test/V4_backup/filename2022-07-12_09:52:46_840291_mask.png', 0)
#
# #convert the image into binary
# ret, thresh = cv2.threshold(img,127,255,cv2.THRESH_BINARY)
#
# #find contours in the image
# contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
#
# #draw all contours in the image
# cv2.drawContours(img, contours, -1, (0,255,0), 3)
#
# #display the image
# # cv2.imshow('image',img)
# #
# # #press any key to close the window
# # cv2.waitKey(0)
# #
# # #destroy all windows
# # cv2.destroyAllWindows()
# cv2.imwrite("/home/ceinfo/Desktop/result/1.jpg",img)


'''----'''

import os
from multiprocessing import Pool
from timeit import default_timer as timer

input_dir = '/home/ceinfo/Desktop/images_copy/'
output_dir="/home/ceinfo/Desktop/images/"

# command = 'gdal_translate -of GTiff -co COMPRESS=JPEG {input} {output}'
# out_files = path1 + "/" + in_file + ".tif"
southwest=[77.144258,28.612838]
northeast=[77.174728,28.625383]
# print("outfiles", out_files)
ulx = southwest[1]
uly = northeast[0]
lrx = northeast[1]
print("lrx", lrx)
lry = southwest[0]
print("lry", lry)
command1 = 'gdal_translate -of Gtiff -co compress=JPEG  -a_ullr '   + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + input_dir+"1.png" +" "+ output_dir+"1.tif"


def process(file):
    input = os.path.join(input_dir, file)
    filename = os.path.splitext(os.path.basename(file))[0]
    output = os.path.join(output_dir, filename + '.tif')
    # os.system(command1.format(input=input, output=output))
    print(command1)
    os.system(command1.format(input=input, output=output))


files = [file for file in os.listdir(input_dir) if file.endswith('.png')]

if __name__ == '__main__':
    start = timer()
    p = Pool(4)
    p.map(process, files)
    end = timer()
    print(end - start)

    start = timer()
    for file in files:
        process(file)
    end = timer()
    print(end - start)