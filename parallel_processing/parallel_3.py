# write a python script to generate georeferenced image using jpg image and its lat longs

#!/usr/bin/env python

import sys
import os
import argparse

from PIL import Image

from pyproj import Proj, transform

def main():
    parser = argparse.ArgumentParser(description="This script generates a georeferenced image using a JPG image and its latitude and longitude coordinates")
    parser.add_argument("--image", help="The path to the JPG image", required=True, default="/home/ceinfo/Desktop/images_copy/1.jpg")
    parser.add_argument("--latitude", help="The latitude of the image", required=True)
    parser.add_argument("--longitude", help="The longitude of the image", required=True)
    parser.add_argument("--output", help="The path to the output image", required=True)
    args = parser.parse_args()

    #generate output image
    img = Image.open(args.image)
    width, height = img.size

    #set up the source projection
    sourceProj = Proj(init='epsg:4326')

    #set up the destination projection
    destProj = Proj(init='epsg:3857')

    #convert the latitude and longitude to x and y coordinates
    x1,y1 = transform(sourceProj, destProj, args.longitude, args.latitude)

    #calculate the x and y coordinates for the bottom right corner of the image
    x2,y2 = transform(sourceProj, destProj, args.longitude + (1.0/3600.0), args.latitude + (1.0/3600.0))

    #calculate the width and height of the image in the destination projection
    width2 = x2 - x1
    height2 = y1 - y2

    #open the output image
    out = Image.new('RGBA', (width, height))

    #paste the input image into the output image
    out.paste(img, (0,0))

    #save the output image
    out.save(args.output)

if __name__ == "__main__":
    main()