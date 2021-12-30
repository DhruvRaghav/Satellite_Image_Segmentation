import os

def gdal_convert(path1,in_file,southwest,northeast):

    try:
        in_files=os.path.join((path1+"/"+in_file+".jpg"))
        out_files=os.path.join(("uploads03/"+in_file+".tif"))
        ulx=southwest[1]
        uly=northeast[0]
        lrx=northeast[1]
        lry=southwest[0]
        command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files

        os.system(command1)
    except Exception as e:
        return e

'''****************************************************************************************************'''

def gdal_completetiff():

    from osgeo import gdal
    from osgeo import osr
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

    gdal_convert("/home/ceinfo/Desktop/Images/",'Raebareilly_183',['20.55248', '77.53618'],['20.52536', '77.58905'])

