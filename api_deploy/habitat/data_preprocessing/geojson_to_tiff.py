import os
import json


def tif_maker(path, data=None):
    in_file = path.split('.')[0]
    print(0)
    # check json file
    assert os.path.exists(in_file + ".geojson")
    print(in_file + ".geojson")
    f = open(in_file + ".geojson")
    data = json.load(f)
    print('data', data)
    print(data['features'][0]['properties']['top'])
    # print(data['Locations']['features'][0]['geometry']['coordinates'][0])
    # northeast, southwest= data['Locations']['features'][0]['geometry']['coordinates'][0][0], data['Locations']['features'][0]['geometry']['coordinates'][0][1]
    northeast, southwest = (data['features'][0]['properties']['top'], data['features'][0]['properties']['left']), (
        data['features'][0]['properties']['bottom'], data['features'][0]['properties']['right'])
    print('northeast, southwest',northeast, southwest)

    files = path
    out_files = in_file + ".tif"
    ulx = southwest[1]
    uly = northeast[0]
    lrx = northeast[1]
    lry = southwest[0]
    command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(
        lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + files + ' ' + out_files

    print("hello", command1)
    os.system(command1)

def tif_maker_1(path):


    in_file=path.split('.')[0]
    print(0)
    #check json file
    assert os.path.exists(in_file + ".geojson")
    print(in_file + ".geojson")
    f=open(in_file + ".geojson")
    data = json.load(f)
    print(data)
    print(data['Locations']['features'][0]['geometry']['coordinates'][0])
    northeast, southwest= data['Locations']['features'][0]['geometry']['coordinates'][0][0], data['Locations']['features'][0]['geometry']['coordinates'][0][1]
    print(northeast, southwest)

    files = path
    out_files = in_file + ".tif"
    ulx = southwest[1]
    uly = northeast[0]
    lrx = northeast[1]
    lry = southwest[0]
    command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(
        lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + files + ' ' + out_files

    print("hello", command1)
    os.system(command1)


def geojson_to_tif_(path):
    path_ = os.getcwd()
    # print("path of geojson and png",path_)
    directory = "uploads_tiff"
    parent_dir = path_
    path_ = os.path.join(parent_dir, directory)
    print("output path of tiff : ", path_)
    try:
        os.makedirs(path_, exist_ok=True)
    except OSError as error:
        pass
    print("path of geojson and png",path)
    for file1 in os.listdir(path):
        print("files ",file1)


        get1 = file1.split('.')[1]
        print("extension of geojson file",get1)
        filename=file1.split('.')[0]
        print("filename",filename)

        if (get1 == 'geojson'):

            in_file = path
            print("path of jeojson",in_file)



            # check json file
            assert os.path.exists(in_file + filename +".geojson")
            print("1 ",in_file + filename +".geojson")
            f = open(in_file + filename +".geojson")
            data = json.load(f)
            print(data)
            print(data['Locations']['features'][0]['geometry']['coordinates'][0])
            northeast, southwest = data['Locations']['features'][0]['geometry']['coordinates'][0][0], \
                                   data['Locations']['features'][0]['geometry']['coordinates'][0][1]
            print(northeast, southwest)

            files = path+"/"+ filename+".png"
            print("tiff file path ",files)


            out_files = path_+"/"+filename+ ".tif"
            print("output path of tiff",out_files)
            ulx = southwest[1]
            uly = northeast[0]
            lrx = northeast[1]
            lry = southwest[0]
            command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(
                lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + files + ' ' + out_files

            print("hello", command1)
            os.system(command1)


# tif_maker_1("/home/ceinfo/Downloads/test11/3_data.png")

if __name__ == '__main__':

    # tif_maker_1("/home/ceinfo/Desktop/geojson/3_data.png")
    geojson_to_tif_("/home/ceinfo/Desktop/rough/")