import os
import subprocess
# from api_deploy.habitat.conversion_tiff_image import *

# from api_deploy.geotiff import gdal_convert
def gpu_parallel_exec(script1, script2):
# assuming both the scripts are in the same directory
    p1 = subprocess.Popen(['python', script1], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(['python', script2], stdout=subprocess.PIPE)
    print(p1.communicate()[0])
    print(p2.communicate()[0])

if __name__ == '__main__':
     gpu_parallel_exec('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/API_Deploy.py', '/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/API_Deploy.py')