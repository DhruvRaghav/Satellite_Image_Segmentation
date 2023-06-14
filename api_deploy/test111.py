import geoio
import cv2
import json
import os
# from PIL import Image

def geojson(path1,in_file):
    #print(path1)
    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpeg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #print(contours)
    polygon = []
    Features_p = []
    Features_l = []

    a=[]
    for cnt in contours[1]:
        new_filter_p=[]
        new_filter_l = []
        first=[]
        first_l=[]
        x2=0
        y2=0
        for j,i in enumerate(cnt):
            x1=int(i[0][0])
            y1=int(i[0][1])
            x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
            # a.append(i.tolist())
            if(len(new_filter_l)==0):
                # first.append(x1)
                first_l.append(x)
                first_l.append(y)
                # x2=x
                # y2=y
            new_filter_p.append([x1,y1])
            new_filter_l.append([x, y])
        new_filter_p.append(first)
        new_filter_l.append(first_l)

        #Features.append({"type": "features", "properties": {}, "geometry": new_filter})
        # Features.append({"type": "feature", "properties":{},"geometry":new_filter_p})
        #print(Features)
        Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "pixels": [new_filter_p]}})
        Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    #print(d)
    #print(p)
    c={"Locations":d,"Pixels":p}
    #print(c)
    #c={"PIXELS":d}
    #os.remove(os.path.join('/mnt/vol1/Deployment_projects/satellite_image_segmentation/uploads',in_file+'.TAB'))
    with open(path1+"/"+'122222'+'.geojson','w') as fp:
           json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    #return c
    # return {"Locations":d,"Pixels":p}
    return {"Locations":d}

geojson('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav (copy)/api_deploy/uploads2','6137_A1')

