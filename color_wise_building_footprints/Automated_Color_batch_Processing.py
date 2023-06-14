import numpy as np
import cv2
import pandas as pd
import os
import math

def Automated_Color_batch_Processing(csv_path, image_path):
        data = pd.read_csv(csv_path)
        df = pd.DataFrame(columns=['EdgeID', 'color','hex'])

        files = []
        fileName = []
        exts = ['jpg', 'png', 'jpeg', 'JPG']

        for parent, dirnames, filenames in os.walk(image_path):
            print('directory image path--', parent)
            for filename in filenames:

                for ext in exts:
                    if filename.endswith(ext):
                        files.append(os.path.join(parent, filename))
                        fileName.append(filename[:-4])
                        break
        print('Find {} images'.format(len(files)))
        for i in range(len(fileName)):
            img_1 = np.array(cv2.imread(files[i]))
            print("file name ",fileName[i])


            try:
                filter = data[data['GridNo'] == int(fileName[i])][:]
            except Exception as e:
                continue
            filter.index = range(len(filter))
            pts = []
            for j in range(0, len(filter) - 1):
                edge_id = filter['EDGE_ID'][j]
                if (j == len(filter)):
                    pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
                    pts = np.array(pts)
                if (edge_id == filter['EDGE_ID'][j + 1]):
                    pts.append([abs(math.ceil(filter['CentroidX'][j])), abs(math.ceil(filter['CentroidY'][j]))])
                else:
                    pts.append([math.ceil(filter['CentroidX'][j]), math.ceil(filter['CentroidY'][j])])
                    pts = np.array(pts)
                    x, y, w, h = cv2.boundingRect(pts)

                    ROI = img_1[y:y + h, x:x + w]

                    average_color_row = np.average(ROI, axis=0)
                    average_color = np.average(average_color_row, axis=0)

                    cv2.fillConvexPoly(img_1, pts, average_color)
                    pts = []

                    try:
                        average_color=[int(average_color[2]), int(average_color[1]),int(average_color[0])]
                        hex_c = ('{:X}{:X}{:X}').format(average_color[0], average_color[1], average_color[2])
                    except:
                        print('false')

                    df.loc[len(df.index)] = [edge_id, average_color, hex_c]


            print("i am filename ",fileName[i])
            save_img = '/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/color_wise_building_footprints/output_images/{}.jpg'.format(fileName[i])
            print(save_img)
            cv2.imwrite(save_img, img_1)
        df.to_csv("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/color_wise_building_footprints/color_csv/result.csv", index=None)