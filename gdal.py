import os
# from gdal import *
import pandas as pd
import ast
def gdal():


        # df = pd.read_csv('Users.csv')

        f=open("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/text_file/parameters.txt","r")
        # import pandas as pd
        southwest=f.readline()
        print(type(southwest))

        southwest=ast.literal_eval(southwest)
        print(type(southwest))

        northeast=f.readline()
        northeast = ast.literal_eval(northeast)
        print(northeast)
        path1=f.readline()
        print("with space",path1)
        path1=path1[0:-1]
        print(path1)
        inn_files=f.readline()
        in_files=path1+"/"+inn_files+".jpg"
        print(in_files)

        out_files=path1+"/"+inn_files+".tif"
        # read CSV file
        # df = pd.read_csv('datafile.csv')

        # read the value in the cell at row 2 and column 1
        # value = df.iloc[1, 0]
        # value = df.iloc[1, 1]
        # value = df.iloc[1, 1]
        # value = df.iloc[1, 1]


        # print(value)

        # print("infile",in_file)
        # print("hi", path1,in_file,southwest,northeast)
        # in_files=os.path.join((path1+"/"+in_file+".jpg"))
        # #out_files=os.path.join((path1+"/"+in_file+".tif"))
        #
        # out_files= path1+"/"+in_file+".tif"
        # print("outfiles",out_files)
        # ulx=southwest[1]
        # uly=northeast[0]
        # lrx=northeast[1]
        # print("lrx",lrx)
        # lry=southwest[0]
        # print("lry",lry)
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)


        # command1='gdal_translate -of Gtiff -co compress=JPEG -A_ullr '+str(southwest[1]) +' '+ str(southwest[0]) +' '+ str(northeast[1]) +' '+ str(northeast[0]) +' -a_srs EPSG:4326 '+in_files+' '+out_files
        command1=f"gdal_translate -of Gtiff -co compress=JPEG -A_ullr {str(southwest[1])} {str(southwest[0])}  {str(northeast[1])}  {str(northeast[0])} -a_srs EPSG:4326 {in_files} {out_files} "
        # geotif
        #command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files
        #
        print(command1)
        os.system(command1)
        #command1 = 'gdal_translate -of Gtiff -co compress=JPEG -A_ullr ' + str(ulx) + ' ' + str(uly) + ' ' + str(lrx) + ' ' + str(lry) + ' -a_srs EPSG:4326 ' + in_files + ' ' + out_files

        # # hello()
        # print(command1)
        # c="'"+command1+"'"
        # hello()
        # print("c",c)

        # os.system(c)
        #
        # gdaloutput = out_files
        # gdalinput = in_files
        # translate_options = gdal.TranslateOptions(format='GTiff',
        #                                           creationOptions=['TFW=YES', 'COMPRESS=LZW']
        #                                           )
        # gdal.Translate(gdaloutput, gdalinput, options=translate_options)

        # T=gdal.TranslateOptions(gdal.ParseCommandLine("-of Gtiff -co compress=JPEG"))
        # print('T',T)
        # gdal.Translate(out_files,in_files,options=T)
        # f = ['!table\n', '!version 300\n', '!charset WindowsLatin1\n', '\n', 'Definition Table\n', '  File "{a}"\n'.format(a=in_file),
        #      '  Type "RASTER"\n', '  (77.029501,28.738489) (0,0) Label "Pt 1",\n',
        #      '  (77.042887,28.738489) (1232,0) Label "Pt 2",\n', '  (77.042887,28.728832) (1232,650) Label "Pt 3",\n',
        #      '  (77.029501,28.728832) (0,650) Label "Pt 4"\n', '  CoordSys Earth Projection 1, 104\n', '  Units "degree"\n']
        # pt1 = f[7].split(' ')
        # pt1[2] = '(' + southwest[1] + ',' + northeast[0] + ')'
        # # pt1[3]=str((0,0))
        # f[7] = ' '.join(pt1)
        # pt2 = f[8].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + northeast[0] + ')'
        # f[8] = ' '.join(pt2)
        # pt2 = f[9].split(' ')
        # pt2[2] = '(' + northeast[1] + ',' + southwest[0] + ')'
        # f[9] = ' '.join(pt2)
        # pt2 = f[10].split(' ')
        # pt2[2] = '(' + southwest[1] + ',' + southwest[0] + ')'
        # f[10] = ' '.join(pt2)
        # with open(os.path.join('uploads03',in_file+'.TAB'),'w') as fp:
        #     fp.writelines(f)
        # # subprocess.call('gdalwarp -t_srs EPSG:4326  /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/
        # api_deploy/uploads03/filename.tif /mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads03/filename_reproject.tif')


if __name__ == '__main__':


    gdal()