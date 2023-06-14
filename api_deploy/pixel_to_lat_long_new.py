from osgeo import gdal

# Open tif file
ds = gdal.Open('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads/5721_mask.tif')

# GDAL affine transform parameters, According to gdal documentation xoff/yoff are image left corner, a/e are pixel wight/height and b/d is rotation and is zero if image is north up.
xoff, a, b, yoff, d, e = ds.GetGeoTransform()
print(xoff,a, b, yoff, d, e)

def pixel2coord(x, y):
 """Returns global coordinates from pixel x, y coords"""
 xp = a * x + b * y + xoff
 yp = d * x + e * y + yoff
 return(xp, yp)

# get columns and rows of your image from gdalinfo
rows = 4800
colms = 3705

if __name__ == "__main__":
    x=1
 # for row in  range(0,rows):
 #  for col in  range(0,colms):
 #   # print(pixel2coord(col,row))