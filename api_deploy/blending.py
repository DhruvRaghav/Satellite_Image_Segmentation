from PIL import Image
#from os import walk
import cv2
from os import walk
import matplotlib.pyplot as plt
import os
import numpy as np
from datetime import date
# Function to change the image size
def changeImageSize(maxWidth,maxHeight,im):
    print(im.size)
    widthRatio = maxWidth / im.size[0]
    heightRatio = maxHeight / im.size[1]

    newWidth = int(widthRatio * im.size[0])
    newHeight = int(heightRatio * im.size[1])

    newImage = im.resize((newWidth, newHeight))
    return newImage





'''images path'''
data_path = '/home/ceinfo/Desktop/50_new/FP_ASUTOSH/images/'
'''mask path '''
data_path1 = '/home/ceinfo/Desktop/50_new/FP_ASUTOSH/mask/'
#print(data_path)
#num_channels = 3
#num_mask_channels = 1
#threshold = 0.1

# ids = []
# test_ids = []
# for (dirpath, dirnames, filenames) in walk(data_path):
#         ids.extend(filenames)
#         print(ids)
#         print("###########")
#         break
#
# for i in ids:
#         if 'jpg' or 'png' in i:
#                 test_ids.append(i)
#
#
# test_ids1 = []
# for (dirpath, dirnames, filenames) in walk(data_path1):
#         ids.extend(filenames)
#         #print(ids)
#         print("###########")
#         break
#
# for i in ids:
#         if 'jpg' or 'png' in i:
#                 test_ids1.append(i)
# # print(test_ids1)
# # print(len(test_ids1))
#
#
#


# for image_id in test_ids and test_ids1:
for image_id in os.listdir(data_path):
    print(image_id)
    im = Image.open(os.path.join(data_path1,image_id))
    im2 = Image.open(os.path.join(data_path,image_id))
    #print(im)
    #print(im2)
#
    # #/home/ceinfo/Desktop/1
    # Take two images for blending them together
    # image1 = Image.open("/home/ceinfo/Desktop/4428.jpg")
    # image2 = Image.open("/home/ceinfo/Desktop/1.jpg")

    # Make the images of uniform size
    print("1")
    image3 = changeImageSize(800, 500, im)
    print("2")
    image4 = changeImageSize(800, 500, im2)

    # Make sure images got an alpha channel
    print("3")
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")

    # Display the images
    #image5.show()
    #image6.show()

    # alpha-blend the images with varying values of alpha
    #alphaBlended1 = Image.blend(image5, image6, alpha=.2)
    alphaBlended2 = Image.blend(image5, image6, alpha=.4)
    print("4")

    # Display the alpha-blended images
    #alphaBlended1.show()
    #alphaBlended2.show()


    os.makedirs("/home/ceinfo/Desktop/50_new/FP_ASUTOSH/overlay/" + "(overlays)", exist_ok=True)
    print("5")
    #plt.imsave("/mnt/vol1/DhruvRaghav/2021(improved models)/pythonProject/images/MGIS VISION/building_model/bhuvan/banglore/(overlays)" + image_id, np.squeeze(alphaBlended2) * 255, cmap='gray', dpi=1)
    print("6")

    # alpha = 0.6
    # new_mask = np.squeeze(new_mask, -1)
    # color_mask = np.dstack((new_mask, new_mask, new_mask))
    #
    # image = image - image * (color_mask * 0.3)
    # image[:, :, 0] += ((color_mask * 255) * 0.3)[:, :, 0]
    # print(image)

    plt.imsave("/home/ceinfo/Desktop/50_new/FP_ASUTOSH/overlay/(overlays)/"  +  image_id[:-4] + ".png",alphaBlended2 , dpi=1)




