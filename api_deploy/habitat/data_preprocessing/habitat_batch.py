import rioxarray
import json
# import cv2
import matplotlib as plt
import matplotlib.pyplot as plt
import os
import cv2
import numpy as np

from matplotlib import image as mpimg
def Geojson_to_mask():


    path = os.getcwd()
    directory = "uploads03"
    parent_dir = path
    path = os.path.join(parent_dir, directory)
    print("output path of mask : ",path)
    try:
        os.makedirs(path, exist_ok=True)
    except OSError as error:
        pass


    path1='/mnt/vol2/Dhruv_Raghav/habitation_2k22/test_train-habitat/'
    '''tiff image'''
    path2='/home/ceinfo/PycharmProjects/pythonProject/test_2022/uploads_tiff/'
    masks_path=path
    for file1 in os.listdir(path1):
        print("geojson file: ",file1)

        # load in the geojson file
        with open(os.path.join(path1,file1)) as igj:
            data = json.load(igj)
            print("data",data)
        # if GDAL 3+
        crs = data["crs"]["properties"]["name"]

        # crs = data["crs"]["properties"]["name"]

        # crs = "EPSG:4326" # if GDAL 2

        geoms = [feat["geometry"] for feat in data["features"]]
        print("geoms",geoms)

        # create empty mask raster based on the input raster
        print("image_path",path2+file1.split('_')[0]+"_data.tif")
        try:
            rds = rioxarray.open_rasterio(os.path.join(path2,file1.split('_')[0]+"_data.tif")).isel(band=0)
            rds.values[:] = 1
            rds.rio.write_nodata(0, inplace=True)
            clipped = rds.rio.clip(geoms, crs, drop=False)
            # print(clipped)

            clipped.rio.to_raster(os.path.join(masks_path, file1.split('_')[0] + "_mask.png"), dtype="uint8",
                                  interleave='Pixel')
            mask_path = os.path.join(masks_path, file1.split('_')[0] + "_mask.png")
            print("mask_path", mask_path)
            file1 = file1.split('_')[0] + "_mask.png"

            color_change(mask_path, path, file1)
            # print(clipped)

        except:
            pass
        # clip the raster to the mask

        # input_img = plt.imread('mask.tif')
        # plt.imshow('input_img')


def color_change(mask_path,path,file1):
    image = cv2.imread(mask_path)
    print("2")
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    print("3")

    image=np.array(gray)
    #plt.imshow(image)
    #plt.show()

    # image = cv2.flip(image, 1)
    # cv2.imshow("heyyy",image)
    # cv2.waitKey(0)
    # plt.imshow(image)
    # plt.show()

    th,thresh = cv2.threshold(image, 0.00001, 255, cv2.THRESH_BINARY)
    # plt.imshow(thresh)
    # plt.show()
    cv2.imwrite(path+"/"+file1,thresh)
if __name__ == '__main__':
    Geojson_to_mask()