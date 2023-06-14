import gdal
import os
import io
import cv2
from PIL import Image,ImageFilter

def gdal_convert(path1,in_file,southwest,northeast):

    try:
        print(path1,in_file,southwest,northeast)
        in_files=os.path.join((path1+"/"+in_file+".jpg"))
        print(type(in_files))
        out_files=os.path.join('uploads03',in_file+".tif")
        print("1")

        # T=gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
        # print('T',T)
        #gdal.Translate(out_files,in_files,options=T)
        gdal.TranslateOptions(out_files,in_files,outputSRS='EPSG:3857',outputBounds =[southwest[1],southwest[0],northeast[1],northeast[0]])

        f = ['!table\n', '!version 300\n', '!charset WindowsLatin1\n', '\n', 'Definition Table\n', '  File "{a}"\n'.format(a=in_file),
             '  Type "RASTER"\n', '  (77.029501,28.738489) (0,0) Label "Pt 1",\n',
             '  (77.042887,28.738489) (1232,0) Label "Pt 2",\n', '  (77.042887,28.728832) (1232,650) Label "Pt 3",\n',
             '  (77.029501,28.728832) (0,650) Label "Pt 4"\n', '  CoordSys Earth Projection 1, 104\n', '  Units "degree"\n']
        pt1 = f[7].split(' ')
        pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # pt1[3]=str((0,0))
        f[7] = ' '.join(pt1)
        pt2 = f[8].split(' ')
        pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        f[8] = ' '.join(pt2)
        pt2 = f[9].split(' ')
        pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        f[9] = ' '.join(pt2)
        pt2 = f[10].split(' ')
        pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        f[10] = ' '.join(pt2)
        with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
            fp.writelines(f)

    except Exception as e:
        return e

    #import geoio
    #ds = geoio.GeoImage(os.path.join(path1+"/"+in_file+".tif"))


    #ds = gdal.open(path1 + "/" + in_file + '.tif')
    #print("hello")

    #print("1",type(ds))
    #ds.SetProjection("EPSG:4326-WGS84")
    #cv2.imsave(path1 + "/" + "hello" + ".tif", ds)


'''****************************************************************************************************'''

def gdal_completetiff():

    print("in")
    from osgeo import gdal
    from osgeo import osr
    import numpy as np
    import h5py
    import os

    os.environ['GDAL_DATA'] = "/Users/andyprata/Library/Enthought/Canopy_64bit/User/share/gdal"

    # read in data
    input_path = '/Users/andyprata/Desktop/modisRGB/'
    with h5py.File(input_path + 'red.h5', "r") as f:
        red = f['red'].value
        lon = f['lons'].value
        lat = f['lats'].value

    with h5py.File(input_path + 'green.h5', "r") as f:
        green = f['green'].value

    with h5py.File(input_path + 'blue.h5', "r") as f:
        blue = f['blue'].value

    # convert rgbs to uint8
    r = red.astype('uint8')
    g = green.astype('uint8')
    b = blue.astype('uint8')

    # set geotransform
    nx = red.shape[0]
    ny = red.shape[1]
    xmin, ymin, xmax, ymax = [lon.min(), lat.min(), lon.max(), lat.max()]
    xres = (xmax - xmin) / float(nx)
    yres = (ymax - ymin) / float(ny)
    geotransform = (xmin, xres, 0, ymax, 0, -yres)

    # create the 3-band raster file
    dst_ds = gdal.GetDriverByName('GTiff').Create('myGeoTIFF.tif', ny, nx, 3, gdal.GDT_Float32)
    dst_ds.SetGeoTransform(geotransform)  # specify coords
    srs = osr.SpatialReference()  # establish encoding
    srs.ImportFromEPSG(3857)  # WGS84 lat/long
    dst_ds.SetProjection(srs.ExportToWkt())  # export coords to file
    dst_ds.GetRasterBand(1).WriteArray(r)  # write r-band to the raster
    dst_ds.GetRasterBand(2).WriteArray(g)  # write g-band to the raster
    dst_ds.GetRasterBand(3).WriteArray(b)  # write b-band to the raster
    dst_ds.FlushCache()  # write to disk
    dst_ds = None




if __name__ == '__main__':

    gdal_convert("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/",'filename',['28.62956387304972', '77.21055150032045'],['28.63669236364457', '77.22771763801576'])



#