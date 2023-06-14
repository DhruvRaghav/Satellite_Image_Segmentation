import csv
import os
import gdal
tab_list=[]

def extract_points():
    with open('/home/ceinfo/Desktop/habi/1234.TAB', newline='') as f:
        #game_reader = csv.DictReader(games)
        for f in f:
            tab_list.append((f))
        # print(tab_list)
        t=tab_list[7]
        # print("northwest",t)
        t=t.split(")")
        c=(t[0])
        # print("hello",c)
        northwest=c.split("(")
        northwest=northwest[1]
        print((northwest))
        t=northwest.split(",")
        print("northeast",t)

        p=tab_list[9]
        # print("southeast", t)
        p = p.split(")")
        c = (p[0])
        # print("hello", c)
        southeast = c.split("(")
        southeast = southeast[1]
        # print((northwest))
        p = southeast.split(",")
        print("southeast",p)
        return(p,t)

def gdal_convert1(in_file,southwest,northeast):

    try:
        in_files=os.path.join('/home/ceinfo/Desktop/rough',in_file+'.png')
        out_files=os.path.join('/home/ceinfo/Desktop/rough',in_file+'.tif')
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
        with open(os.path.join('/home/ceinfo/Desktop/rough/',in_file+'.TAB'),'w') as fp:
            fp.writelines(f)
    except Exception as e:
        return e
#


if __name__ == '__main__':
    p,t=extract_points()
    gdal_convert1("1234",p,t)