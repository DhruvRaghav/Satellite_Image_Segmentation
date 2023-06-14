# write a python script to generate georeferenced image using jpg image and its lat longs

import sys
import os
import numpy as np
from PIL import Image

# read in image and lat/long data
im = Image.open("/home/ceinfo/Desktop/images_copy/1.png")

lat=[1.0,77.144258,28.612838]
print(lat[0])
long=[10.0,77.174728,28.625383]
# lat = np.loadtxt(sys.argv[2])
# long = np.loadtxt(sys.argv[3])

# get image dimensions
nx,ny = im.size
print(nx,ny)

# create a new geotif file
cmd = 'gdal_translate -of GTiff -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" '
cmd += '-a_srs EPSG:4326 -gcp 0 0 %f %f -gcp %d %d %f %f -gcp %d %d %f %f ' % (long[0],lat[0],nx,0,long[1],lat[1],0,ny,long[2],lat[2])
cmd += "/home/ceinfo/Desktop/images_copy/1.png" + ' temp.tif'
os.system(cmd)

# reproject to UTM
cmd = 'gdalwarp -co "TILED=YES" -co "BLOCKXSIZE=512" -co "BLOCKYSIZE=512" -r bilinear '
cmd += '-t_srs EPSG:32630 temp.tif ' + "/home/ceinfo/Desktop/images_copy/1" + '.tif'
os.system(cmd)

# clean up
os.remove('temp.tif')