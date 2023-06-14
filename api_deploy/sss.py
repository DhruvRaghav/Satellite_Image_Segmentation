import os
import gdal
in_file='1579513636756'
in_files = os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads', in_file + '.png')
out_files = os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads', in_file + '.tif')
T = gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
gdal.Translate(in_files, out_files, options=T)