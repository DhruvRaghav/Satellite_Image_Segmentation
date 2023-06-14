import os

def hello():
    c='gdal_translate -of Gtiff -co compress=JPEG -A_ullr 77.53618 20.52536 77.58905 20.55248 -a_srs EPSG:4326 /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/22022-11-18_16:54:10_385800.jpg /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/22022-11-18_16:54:10_385800.tif'
    p='gdal_translate -of JPEG  -A_ullr 77.53618 20.52536 77.58905 20.55248 -a_srs EPSG:4326 /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/22022-11-18_16:54:10_385800.jpg /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/22022-11-18_16:54:10_385800.tif'
    os.system(p)

if __name__ == '__main__':
    hello()