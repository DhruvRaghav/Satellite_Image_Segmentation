import geoio
import cv2
import json
import os
import datetime

def geojson(path1,in_file):
    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpeg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if (len(cnt > 2)):
            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                # a.append(i.tolist())
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d,"Pixels":p}
    with open(path1+"/"+'122222'+'.geojson','w') as fp:
           json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return c



def geojson2(path1,in_file):

    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Features_p = []
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            first_p=[]
            x2=0
            y2=0
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                if(len(new_filter_p)==0):
                     first_p.append(x1)
                     first_p.append(y1)
                new_filter_p.append([x1,y1])
            new_filter_p.append(first_p)


            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Pixels":p}
    with open(path1+"/"+'122222'+'.geojson','w') as fp:
           json.dump(c, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return {"Pixels":p}


def geojson3(path1,in_file):
    geoimg = geoio.GeoImage(os.path.join(path1+"/"+in_file+".tif"))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    print(d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}
    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return c



def geojson4(path1,in_file):
    geoimg = geoio.GeoImage(os.path.join(path1,(in_file+'.jpg')))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if(len(cnt>2)):

            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            # new_filter_p.append(first)
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)
            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})

    d = {"type": "FeatureCollection","features":Features_l}
    print('dict', d)
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}
    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    return c




def geojson5(path1,in_file):

    geoimg = geoio.GeoImage(os.path.join(path1+"/"+in_file+".tif"))
    img=cv2.imread(os.path.join(path1,(in_file+'_mask.png')))
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    ret,gray=cv2.threshold(gray,127,255,0)
    contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    Features_p = []
    Features_l = []
    for cnt in contours[1]:
        if(len(cnt>2)):
            new_filter_p=[]
            new_filter_l = []
            first_p=[]
            first_l=[]
            for j,i in enumerate(cnt):
                x1=int(i[0][0])
                y1=int(i[0][1])
                x,y=geoimg.raster_to_proj(i[0][0], i[0][1])
                if(len(new_filter_l)==0):
                    first_l.append(x)
                    first_l.append(y)
                    first_p.append(x1)
                    first_p.append(y1)

                new_filter_p.append([x1,y1])
                new_filter_l.append([x, y])
            new_filter_l.append(first_l)
            new_filter_p.append(first_p)

            Features_p.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_p]}})
            Features_l.append({"type": "Feature", "properties": {}, "geometry": {"type": "Polygon", "coordinates": [new_filter_l]}})
    d = {"type": "FeatureCollection","features":Features_l}
    p = {"type": "FeatureCollection", "features":Features_p}
    c={"Locations":d}

    with open(path1+"/"+in_file+'.geojson','w') as fp:
           json.dump(d, fp) # for the geojson saving uncomment #for fronend we need to comment this line
    print('geojson',datetime.datetime.now())
    return c

if __name__ == '__main__':
    geojson4("/home/ceinfo/Desktop/Images/","Azamgarh_1.jpg")