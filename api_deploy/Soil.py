import cv2
import numpy as np
import matplotlib.pyplot as plt

def predict_soil(path1,image_id):
    #image = cv2.imread('/home/ceinfo/Desktop/1/'+image_id +'.jpg')

    data_path = path1+"/"
    #data_path = '/home/ceinfo/Desktop/1/'
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1


    image = cv2.imread(path1 + "/" + image_id+".jpg")
    #os.remove(path1 + "/" + image_id+".jpg")
    # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # print(geoimg)

    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    print("")

    lower = np.array([44, 6, 126])
    upper = np.array([252, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    # plt.imshow(mask)
    # plt.show()

    thresh = cv2.erode(mask, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    # plt.imshow(thresh)
    # plt.show()
    plt.imsave(data_path + image_id + '_mask.png',
               thresh, cmap='gray', dpi=1)



def predict_soil_Tif_PL(path1,image_id):
    #image = cv2.imread('/home/ceinfo/Desktop/1/'+image_id +'.jpg')

    data_path = path1+"/"
    #data_path = '/home/ceinfo/Desktop/1/'
    # print(data_path)
    # num_channels = 3
    # num_mask_channels = 1
    # threshold = 0.1


    image = cv2.imread(path1 + "/" + image_id+".jpeg")
    #os.remove(path1 + "/" + image_id+".jpeg")
    # image = cv2.imread('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # geoimg = geoio.GeoImage('/home/ceinfos/Documents/Divya Programs/output_shadow/archive(8)/1579769437695.png')
    # print(geoimg)

    image = cv2.cvtColor(image, cv2.COLOR_HSV2RGB)
    print("")

    lower = np.array([44, 6, 126])
    upper = np.array([252, 255, 255])
    mask = cv2.inRange(image, lower, upper)
    # plt.imshow(mask)
    # plt.show()

    thresh = cv2.erode(mask, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    # plt.imshow(thresh)
    # plt.show()
    plt.imsave(data_path + image_id + '_mask.png',
               thresh, cmap='gray', dpi=1)



if __name__ == '__main__':
    predict_soil("/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01")