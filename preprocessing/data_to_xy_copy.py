import geoio
import pandas as pd
import os




data=pd.read_csv('/home/ceinfo/Desktop/FP_Buildings.csv')
path='/home/ceinfo/Desktop/new_data_sample'



files = []
fileName=[]
exts = ['jpg', 'png', 'jpeg', 'JPG']
for parent, dirnames, filenames in os.walk(path):
    print('directory image path--',parent)
    for filename in filenames:

        for ext in exts:
            if filename.endswith(ext):
                files.append(os.path.join(parent, filename))
                fileName.append(filename[:-4])
                break
print('Find {} images'.format(len(files)))
print(files)

new=pd.DataFrame(columns=['EDGE_ID','GridNo','Split_SequenceNum','CentroidX','CentroidY'])
for i in range(len(files)):
    filter=data[data['GridNo'] == int(fileName[i])][:]
    print(fileName[i])
    filter.index = range(len(filter))
    img = geoio.GeoImage(files[i])
    co_x=[]
    co_y=[]
    for j in range(len(filter)):
        x,y = img.proj_to_raster(filter['CentroidX'][j],filter['CentroidY'][j])
        co_x.append(x)
        co_y.append(y)
    filter['CentroidX']=co_x
    filter['CentroidY']=co_y
    new=pd.concat([new,filter])


new.to_csv('/home/ceinfo/Desktop/new_data_sample/fp_test.csv',index=None)