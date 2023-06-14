import rioxarray
import json
import matplotlib as plt
import os
path1='/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/Green_layer'
path2='/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/tif'
masks_path='/mnt/vol1/Sakshi_2/Forest__Segmentation/mmi_data/test'
for file1 in os.listdir(path1):
    print(file1)
    # load in the geojson file
    with open(os.path.join(path1,file1)) as igj:
        data = json.load(igj)
    # if GDAL 3+
    crs = data["crs"]["properties"]["name"]
    # crs = "EPSG:4326" # if GDAL 2
    geoms = [feat["geometry"] for feat in data["features"]]

    # create empty mask raster based on the input raster
    rds = rioxarray.open_rasterio(os.path.join(path2,file1.split('_')[0]+"_data.tif")).isel(band=0)
    rds.values[:] = 1
    rds.rio.write_nodata(0, inplace=True)

    # clip the raster to the mask
    clipped = rds.rio.clip(geoms, crs, drop=False)
    clipped.rio.to_raster(os.path.join(masks_path,file1.split('_')[0]+"_mask.png"), dtype="uint8", interleave='Pixel')
    # input_img = plt.imread('mask.tif')
    # plt.imshow('input_img')