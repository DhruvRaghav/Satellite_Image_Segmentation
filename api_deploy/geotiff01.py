import gdal
import os

def gdal_convert1(in_file,southwest,northeast):

    try:
        in_files=os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/',in_file+'.jpg')
        out_files=os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/',in_file+'.tif')
        T=gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
        gdal.Translate(out_files,in_files,options=T)
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
        with open(os.path.join('/mnt/vol1/DhruvRaghav/PROJECTS/satellite_image_segmentation_deploy_DhruvRaghav/uploads/',in_file+'.TAB'),'w') as fp:
            fp.writelines(f)
    except Exception as e:
        return e
#