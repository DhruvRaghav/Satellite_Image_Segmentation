import geoio
import pandas as pd
import os


'''*************************FOR ROADS ************************************************ '''
#data=pd.read_csv('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/Untitled Folder/RD_LATLON_WITH_GRID.csv')
#path='/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/satellite_road_images'



'''************************* FOR BUILDINGS ************************************************ '''
data=pd.read_csv('/home/ceinfo/Desktop/FP_Buildings.csv')
path='/home/ceinfo/Desktop/new_data_sample'



files = []
fileName=[]
exts = ['jpg', 'png', 'jpeg', 'JPG']
for parent, dirnames, filenames in os.walk(path):
    print('directory image path--',parent)
    for filename in filenames:
        #print(filename[:-4])
        #dirpath='/home/ceinfos/Documents/Textfiles(ENG)/newdata/'+filename[:-4]
        #print('directory image store path--',dirpath)
        #os.makedirs(dirpath)
        for ext in exts:
            if filename.endswith(ext):
                files.append(os.path.join(parent, filename))
                fileName.append(filename[:-4])
                break
print('Find {} images'.format(len(files)))
print(files)
# print(data[data['GridNo'] == 4428][:])
# filter = data[data['GridNo'] == 4428][:]
# ind=[i for i in range(0,len(filter))]
# filter.index=range(len(filter))
# print(type(filter))
# print(filter['CentroidX'][0])
# filter['CentroidX'][0]=12
# print(filter['CentroidX'][0])
new=pd.DataFrame(columns=['EDGE_ID','GridNo','Split_SequenceNum','CentroidX','CentroidY'])
for i in range(len(files)):
    filter=data[data['GridNo'] == int(fileName[i])][:]
    # new=filter.copy()
    print(fileName[i])
    filter.index = range(len(filter))
    # print(filter['CentroidX'])
    img = geoio.GeoImage(files[i])
    co_x=[]
    co_y=[]
    for j in range(len(filter)):
        x,y = img.proj_to_raster(filter['CentroidX'][j],filter['CentroidY'][j])
        co_x.append(x)
        co_y.append(y)
    filter['CentroidX']=co_x
    filter['CentroidY']=co_y
    # print(filter)
    new=pd.concat([new,filter])
# print(new.iloc[:,1:])

'''*************************FOR ROADS ************************************************ '''
#new.to_csv('/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy/preprocessing/data_csv/rd_test.csv',index=None)

'''*************************FOR BULDINGS ************************************************ '''
new.to_csv('/home/ceinfo/Desktop/new_data_sample/fp_test.csv',index=None)