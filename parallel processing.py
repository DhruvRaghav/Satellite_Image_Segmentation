import os
import multiprocessing as mp

processes = ('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_pixel/api_deploy/Api_deploy_pixel.py', '/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/API_Deploy_Pixel.py', '/home/ceinfo/PycharmProjects/database_mysql/1.py')

def run_python(process):
    os.system('python {}'.format(process))

pool = mp.Pool(processes=3)
pool.map(run_python, processes)