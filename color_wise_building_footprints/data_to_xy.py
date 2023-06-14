import geoio
from Automated_Color_batch_Processing import *

def latlon_to_pixel_conversion():

    data=pd.read_csv('/home/ceinfo/Desktop/For_Dhruv/FP_AOI.csv')

    path='/home/ceinfo/Desktop/For_Dhruv/Image/'

    path1 = os.getcwd()
    print("path of ddirectory ---------",path1)

    directory = "pixel_csv"

    parent_dir = path1
    path2 = os.path.join(parent_dir, directory)
    try:
        os.makedirs(path2, exist_ok=True)
    except OSError as error:
        pass

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


    new.to_csv(path2+"/fp_test.csv",index=None)

    return(path2+"/fp_test.csv",path)

if __name__ == '__main__':
    csv_path,path=latlon_to_pixel_conversion()

    Automated_Color_batch_Processing(csv_path, path)
