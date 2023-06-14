import cv2
import os
import math
root='/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/RD_Mask_2'
root1='/mnt/vol1/PycharmProjects/Satellite_Image_Segmentation/Images_With_Annotation_(copy)/'
for image in os.listdir(root):
    img=cv2.imread(os.path.join(root1,image))
    height,width,_=img.shape
    rows=math.floor(height/256)
    columns=math.floor(width/256)
    first=0
    last=256
    first1=0
    last1=256
    num=0
    for row in range(rows+1):
        if (row >= int(rows)):
            first = height - 256
            last = height
        for col in range(columns+1):
            if (col >= int(columns)):
                first1 = width - 256
                last1 = width
            cv2.imwrite('/mnt/vol1/Deployment_projects/satellite_image_segmentation/sat_img_crop/'+image[:-4]+'_'+str(num)+'.jpg',img[first:last,first1:last1])
            print(img[first:last,first1:last1].shape)
            num=num+1
            first1=first1+256
            last1=last1+256

        first=first+256
        last=last+256
        first1 = 0
        last1 = 256
    print(num)
    # num=num+1
    # cv2.imwrite('/mnt/vol1/Deployment_projects/satellite_image_segmentation/sat_img_crop/' + root + '_' + num,
    #             img[3705-512:3705, width-512:width])
    # print(img.shape)
    # print(image)