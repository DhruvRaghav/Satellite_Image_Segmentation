import shapefile, csv
import csv
import re
import urllib
import json
from pyproj import transform,Proj
import requests
# create a point shapefile
def getWKT_PRJ (epsg_code):
    # wkt=requests.get("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    # wkt = urllib.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    # wkt=wkt.json()
    wkt=urllib.request.urlopen("http://spatialreference.org/ref/epsg/{0}/prettywkt/".format(epsg_code))
    # print(wkt.read().decode())
    wkt =wkt.read().decode()
    print(wkt)
    # wkt=json.dumps(wkt)
    # wkt= [x.decode('utf8').strip() for x in wkt.readlines()]
    # remove_spaces = wkt.replace(" ","")
    # output = remove_spaces.replace("\n", "")
    return wkt

output_shp = shapefile.Writer(shapefile.POLYGON)
# for every record there must be a corresponding geometry.
output_shp.autoBalance = 1
# create the field names and data type for each.
# you can insert or omit lat-long here
# output_shp('Date','D')
# output_shp('Target','C',50)
# output_shp('ID','N')
# count the features
counter = 1
# access the CSV file
output_shp.field('label')
with open('/home/ceinfo/Downloads/polygon_WKT.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    # skip the header
    next(reader, None)
    # input_projection = Proj(init="epsg:3857")
    # output_projection = Proj(init="epsg:4326")
    #loop through each of the rows and assign the attributes to variables
    # print(len(reader))
    for h,row in enumerate(reader):
        id= row[0]
        # target= row[1]
        # date = row[2]
        # create the point geometry
        # output_shp.polygon(float(longitude),float(latitude))
        # add attribute data
        # output_shp.record(id, target, date)
        line=[]
        # print(len(row[1]))
        row=row[1][10:len(row[1])-2]
        # row=row.split(' |,')
        row=re.split(' |, |,',row)

        # row=row.split(',')
        # row.remove(',')
        # line=[[float(row[s]),float(row[s+1])] for s in range(0,len(row),2)]
        for i in range(0,len(row),2):
            # new_x, new_y = transform(input_projection, output_projection, float(row[i]), float(row[i+1]))
            line.append([float(row[i]),float(row[i+1])])
            # line.append(new_x,new_y)
        # print(line)


        # output_shp.line(parts=([ float(row[1][8:len(row[1])-2])    ) ) )
        output_shp.line(parts=([line]))
        output_shp.record(h)
        # output_shp.save('line')
        # print(row)
        print("Feature " + str(counter) + " added to Shapefile.")
        counter = counter + 1
# save the Shapefile
# output_shp.save("output.shp")
output_shp.save('line1')
prj = open("line1.prj", "w")
epsg = getWKT_PRJ("4326")
print(epsg)
prj.write(epsg)
prj.close()

# import shapefile as shp
# import csv
#
# out_file = 'GPS_Pts.shp'
#
# #Set up blank lists for data
# x,y,id_no,date,target=[],[],[],[],[]
#
# #read data from csv file and store in lists
# with open('/home/ceinfo/Downloads/count_vgg.csv', 'rb') as csvfile:
#     r = csv.reader(csvfile, delimiter=';')
#     # for i,row in enumerate(r):
#     #     if i > 0: #skip header
#     #         x.append(float(row[3]))
#             # y.append(float(row[4]))
#             # id_no.append(row[0])
#             # date.append(''.join(row[1].split('-')))#formats the date correctly
#             # target.append(row[2])
#
# #Set up shapefile writer and create empty fields
# w = shp.shp.Writer(shp.POINT)
# w.autoBalance = 1 #ensures gemoetry and attributes match
# w.field('X','F',10,8)
# w.field('Y','F',10,8)
# w.field('Date','D')
# w.field('Target','C',50)
# w.field('ID','N')
#
# #loop through the data and write the shapefile
# # for j,k in enumerate(x):
# #     w.point(k,y[j]) #write the geometry
# #     w.record(k,y[j],date[j], target[j], id_no[j]) #write the attributes
#
# #Save shapefile
# w.save(out_file)


# convert well known text to geometry, and compile shapes into a single feature class...
# 11/15/2012
# import arcpy
#
# File = "C:\Users\Team\Documents\Theo Laptop Folder\Tasks\Quick tasks\WKTtest\WKT_to_QGISmakealayerCSV2.csv"
#
# # dimension the WKT string field and poly ID field...
# # the field holding the WKT string...
# field1 = "WKT"
# # the field holding the unique ID...
# field2 = "Our_ref"
#
# # set up the empty list...
# featureList = []
#
# # set the spatial reference to a known EPSG code...
# sr = arcpy.SpatialReference(27700)
# # iterate on table row...
# cursor = arcpy.SearchCursor(File)
# row = cursor.next()
#
# while row:
#     print(row.getValue(field2))
#     WKT = row.getValue(field1)
#     # this is the part that converts the WKT string to geometry using the defined spatial reference...
#     temp = arcpy.FromWKT(WKT, sr)
#     # append the current geometry to the list...
#     featureList.append(temp)
#     row = cursor.next()
#
# # copy all geometries in the list to a feature class...
# arcpy.CopyFeatures_management(featureList,"C:\Users\Team\Documents\Theo Laptop Folder\Tasks\Quick tasks\WKTtest\WKTShapes.shp")
#
# # clean up...
# del row, temp, WKT, File, field1, featureList, cursor