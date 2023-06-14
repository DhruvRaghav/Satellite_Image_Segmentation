import geotiff


# geotiff.gdal_convert("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/",'sat_image_12022-09-13_19:40:10_046028',['20.55248', '77.53618'],['20.52536', '77.58905'])




def create_tiff(path1,in_file,southwest,northeast):
    geotiff.gdal_convert(path1,in_file,southwest,northeast)