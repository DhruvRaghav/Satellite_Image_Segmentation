import geoio
import cv2
import json
import os
# from PIL import Image



def geojson(in_file):
    geoimg = geoio.GeoImage(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads_1',in_file+'.tif'))
    # os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.tif'))
    img=cv2.imread(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'_mask.jpg'))
    # os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'_mask.jpg'))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    polygon = []
    new_filter = []
    for cnt in contours[1]:
        # endpoint = []
        # x1, y1 = geoimg.raster_to_proj(cnt[0][0][0], cnt[0][0][1])
        # x1,y1=pixel_lat_long(file=os.path.join(data_path,image_id),x=cnt[0][0][0],y=cnt[0][0][1])
        # if (x1 < 90.0 and x1 > 65.0 and y1 < 40.0 and y1 > 10.0):
        #     endpoint.append(x1)
        #     endpoint.append(y1)
        for j,i in enumerate(cnt):
            # print(j,i)
            # if (i[0][0] == 0):
            #     i[0][0] = 213.0
            # elif (i[0][1] == 0):
            #     i[0][1] = 34.0
            x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
                new_filter.append([x, y])

        if(len(new_filter)!=0):

            # print(new_filter)
            if(len(new_filter)>10):
                polygon.append([new_filter])
        new_filter=[]
    print(polygon)
    d = {"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "geometry": {"type": "MultiPolygon", "coordinates": polygon}}]}
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    with open('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads_1/122222'+'.geojson','w') as fp:
            json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return d

# geojson('4428')