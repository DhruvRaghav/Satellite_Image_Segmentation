# Write a python script to generate a tiff image using the image and mask of the image

#!/usr/bin/env python

import numpy as np
from PIL import Image

# read in image and mask
image = Image.open('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename2022-07-12_09:51:04_4510112022-10-31_14:34:53_763225.jpg')
mask = Image.open('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename2022-07-12_09:51:04_4510112022-10-31_14:34:53_763225_mask.png')

# create a new image the same size as the original
new_image = Image.new('RGB', image.size)

# get image width and height in pixels
width, height = image.size

# loop over all pixels in the image
for x in range(width):
    for y in range(height):
        # get the color of the current pixel
        color = image.getpixel((x, y))

        # check if the mask pixel is black
        if mask.getpixel((x, y)) == 0:
            # if so, set the new image pixel to black
            new_image.putpixel((x, y), (0, 0, 0))

        # otherwise, set the new image pixel to the original color
        else:
            new_image.putpixel((x, y), color)

# save the new image
new_image.save('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/1.tiff')




"""---------------------------------"""
# Write a python script to generate a  geojson using the tiff image from PIL import Image

import numpy, sys
from numpy.random import rand
import json

# Open the image and convert it to an ndarray
im = Image.open('image.tiff')
arr = numpy.array(im)

# Get the dimensions of the array
rows, cols = arr.shape

# Generate a random array of coordinates
coords = numpy.array([[rand()*cols, rand()*rows] for i in range(1000)])

# Generate a GeoJSON file
geojson = {'type': 'FeatureCollection', 'features': []}
for coord in coords:
    geojson['features'].append({ 'type': 'Feature',
                                 'geometry': {'type': 'Point',
                                              'coordinates': coord.tolist()},
                                 'properties': {'value': arr[coord[1], coord[0]]}
                               })

# Write the GeoJSON file
with open('output.geojson', 'w') as outfile:
    json.dump(geojson, outfile)


