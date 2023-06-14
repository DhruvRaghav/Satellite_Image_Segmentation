
from skimage import io

import geoio
import cv2
#import json
import os
# from PIL import Image
import json
#alerts = {'upper':[1425],'lower':[576],'level':[2],'datetime':['2012-08-08 15:30']}

def geojson1(path1,in_file):
    #path='api_deploy'
    print("inside geojson now")
    print(path1)
    #geoimg = geoio.GeoImage(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/', in_file + '.tif'))
    #os.remove(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/', in_file + '.tif'))
    print(os.path.join(path1,(in_file+'_mask.jpg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    # img=cv2.imread('api_deploy/1111_mask.png')
    print(img)
    print("read the file")
    # os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'_mask.jpg'))
    # gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    # print(contours)
    polygon = []
    #print("polygon ",polygon)
    new_filter = []
    #print("new filter :", new_filter)
    for cnt in contours[1]:
        # endpoint = []
        # x1, y1 = geoimg.raster_to_proj(cnt[0][0][0], cnt[0][0][1])
        # x1,y1=pixel_lat_long(file=os.path.join(data_path,image_id),x=cnt[0][0][0],y=cnt[0][0][1])
        # if (x1 < 90.0 and x1 > 65.0 and y1 < 40.0 and y1 > 10.0):
        #     endpoint.append(x1)
        #     endpoint.append(y1)
        for j,i in enumerate(cnt):
            # if (i[0][0] == 0):
            #     i[0][0] = 213.0
            # elif (i[0][1] == 0):
            #     i[0][1] = 34.0
            x,y=i[0][0],i[0][1]
            #x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            new_filter.append([x,y])
            #print(type(new_filter))
            #print(new_filter)
            #if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
            #new_filter.append([x, y])

        if(len(new_filter)!=0):

            #print(new_filter)
            #if(len(new_filter)>10):
                new_filter=tuple(new_filter)

                i = ''.join(str(x) for x in new_filter)
                #print(type(i))
        #         #print((i))
        #         #print(type(new_filter1))
                p={"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "pixels": {"type": "MultiPolygon", "values": i}}]}
        # # new_filter=[]
    # d=tuple(polygon)
    # print(d)
    #print (d)
    # #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    #with open('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/122222'+'.geojson','w') as fp:
    #      json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line

    #'count__c': int(store['count'].iloc[i])
    # print(d)
    return p

def geojson2(path1,in_file):
    '''PIXELS TO BE REFLECTED ON POSTMAN IN A NEW FORMAT '''
    print("inside geojson now")
    print(in_file)
    in_file=in_file[0:-4]
    print(in_file)
    print(path1)
    image_id=in_file
    print(os.path.join(path1,(in_file+'_mask.png')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    #os.remove(path1 + "/" + image_id + '_mask.png')

    print("read the file")
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    print("1")
    ret,gray=cv2.threshold(gray,127,255,0)
    print("2")
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    print("3")
    for cnt in contours[1]:
        #print("4")
        new_filter = []
        Features=[]
        for j,i in enumerate(cnt):
            x=int(i[0][0])
            #print(x)
            y=int(i[0][1])
            #print(y)
            new_filter.append([x,y])
            #print(new_filter)
        print(new_filter)
        #Features.append({"type": "features","properties":{},"geometry":{"type":"polygon","coordinates":[new_filter]}})
        Features.append({"type": "feature", "properties": {}, "geometry": new_filter})
    p={"type": "FeatureCollection","Features":Features}
    #print(p)
    with open('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01/122222'+'.geojson','w')as fp:json.dump(p, fp)
    return {"Pixels":p}


def geojson3(in_file):
    #geoimg = geoio.GeoImage(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/', in_file + '.tif'))
    #os.remove(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/', in_file + '.tif'))
    img=cv2.imread(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01/', in_file + '_mask.png'))
    # os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'_mask.jpg'))
   # print(type(img))

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    polygon = []
    #print("polygon ",polygon)
    new_filter = []
    #print("new filter :", new_filter)
    for cnt in contours[1]:
        #print("hi")
        # endpoint = []
        # x1, y1 = geoimg.raster_to_proj(cnt[0][0][0], cnt[0][0][1])
        # x1,y1=pixel_lat_long(file=os.path.join(data_path,image_id),x=cnt[0][0][0],y=cnt[0][0][1])
        # if (x1 < 90.0 and x1 > 65.0 and y1 < 40.0 and y1 > 10.0):
        #     endpoint.append(x1)
        #     endpoint.append(y1)
        for j,i in enumerate(cnt):
            # if (i[0][0] == 0):
            #     i[0][0] = 213.0
            # elif (i[0][1] == 0):
            #     i[0][1] = 34.0
            x,y=i[0][0],i[0][1]
            #print(x)
            #x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            new_filter.append([x,y])
            #print(type(new_filter))
            #print(new_filter)
            #if(x<90.0 and x > 60.0 and y <40.0 and y>10.0):
            #new_filter.append([x, y])

        if(len(new_filter)!=0):

            #print(new_filter)
            #if(len(new_filter)>10):
                #new_filter1=tuple(new_filter)

                i = ''.join(str(x) for x in new_filter)
                #print(type(i))
                #print((i))
                #print(type(new_filter1))
                d={"type": "FeatureCollection","features": [{"type": "Feature", "properties": {}, "pixels": {"type": "MultiPolygon", "values": i}}]}
        # new_filter=[]
    # d=tuple(polygon)
    print(d)
    #print(i)
    #print (d)
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    with open('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01/122222'+'.geojson','w') as fp:
         json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line

    #'count__c': int(store['count'].iloc[i])
    return d



#print(path1)

def geojson4(path1,in_file):

    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    polygon = []
    Features_p = []
    # Features_l = []

    a=[]
    for cnt in contours[1]:
        new_filter_p=[]
        # new_filter_l = []
        first=[]
        first_p=[]
        x2=0
        y2=0
        for j,i in enumerate(cnt):
            x1=int(i[0][0])
            y1=int(i[0][1])
            # x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            # a.append(i.tolist())
            if(len(new_filter_p)==0):
                first_p.append(x1)
                first_p.append(y1)
                # x2=x
                # y2=y
            new_filter_p.append([x1,y1])
            # new_filter_l.append([x, y])
        # new_filter_p.append(first)
        new_filter_p.append(first_p)

        #Features.append({"type": "features", "properties": {}, "geometry": new_filter})
        # Features.append({"type": "feature", "properties":{},"geometry":new_filter_p})
        #print(Features)
        Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "pixels": [new_filter_p]}})
        # Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_p}
    #print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    #print(d)
    #print(p)
    c={"Pixels":p}
    #print(c)
    #c={"PIXELS":d}
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    with open(path1+"/"+'122222'+'.geojson','w') as fp:
           json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    #return c
    # return {"Locations":d,"Pixels":p}
    return {"Locations":p}


def geojson5(path1,in_file):

    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    # polygon = []
    Features_p = []
    # Features_l = []

    # a=[]
    for cnt in contours[1]:
        new_filter_p=[]
        # new_filter_l = []
        # first=[]
        first_p=[]
        x2=0
        y2=0
        for j,i in enumerate(cnt):
            x1=int(i[0][0])
            y1=int(i[0][1])
            # x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            # a.append(i.tolist())
            if(len(new_filter_p)==0):
                first_p.append(x1)
                first_p.append(y1)
                # x2=x
                # y2=y
            new_filter_p.append([x1,y1])
            # new_filter_l.append([x, y])
        # new_filter_p.append(first)
        new_filter_p.append(first_p)

        #Features.append({"type": "features", "properties": {}, "geometry": new_filter})
        # Features.append({"type": "feature", "properties":{},"geometry":new_filter_p})
        #print(Features)
        Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "pixels": [new_filter_p]}})
        # Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    # d = {"type": "FeatureCollection","features":Features_p}
    #print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    #print(d)
    #print(p)
    c={"Pixels":p}
    #print(c)
    #c={"PIXELS":d}
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    with open(path1+"/"+'122222'+'.geojson','w') as fp:
           json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    #return c
    # return {"Locations":d,"Pixels":p}
    return {"Locations":p}


if __name__ == '__main__':
    geojson4("/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01/",'Azamgarh_2')

# if __name__ == '__main__':
#     #geojson2("/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01",'Azamgarh_1.png')
#
#     geojson2(
#         "/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads01/",
#         'Azamgarh_2.jpg')
