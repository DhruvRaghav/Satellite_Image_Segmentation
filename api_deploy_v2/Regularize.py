import cv2
import os
import numpy as np
from datetime import datetime
# image = cv2.imread('')
th=2

def removeOverlapping(image_name):
    print(image_name)
    m_img = cv2.imread(image_name+'_mask.png')
    img = cv2.imread(os.path.join(image_name + '.jpg'))
    img_1 = cv2.imread(os.path.join(image_name + '.jpg'))

    f_mask = np.zeros(img.shape, dtype=np.uint8)
    f_mask.fill(0)
    # img = cv2.imread(image)
    # new_mask = np.zeros(m_img.shape, dtype=np.uint8)
    # new_mask.fill(0)
    gray = cv2.cvtColor(m_img, cv2.COLOR_BGR2GRAY)
    # gray=cv2.cvtColor(img,cv2.COLOR_RGB2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    contours = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # gray1 = cv2.cvtColor(m_img, cv2.COLOR_BGR2GRAY)
    # ret, gray1 = cv2.threshold(gray1, 127, 255, 0)
    # # contours=cv2.findContours(gray,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    #
    # contour_list = cv2.findContours(gray1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contour_list, key=cv2.contourArea, reverse=True)
    # cnt_all=len(contours)
    # print(cnt_all)
    i = 0
    for cnt in contours[1]:
        if(len(cnt)>2):
            # print(cnt)
            area = cv2.contourArea(cnt)
            if(area<250 and area>50):
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                im = cv2.drawContours(img, [box], 0, (0, 255, 0), thickness=th)
                im_f = cv2.drawContours(f_mask, [box], 0, (0, 0, 0), thickness=2)
                cv2.fillPoly(f_mask, pts=[box], color=(255, 255, 255))
                i=i+1
            # imm = cv2.drawContours(new_mask, [cnt], 0, (255, 255, 255))
            imm2 = cv2.drawContours(img_1, [cnt], 0, (0, 255, 0),thickness=th)
            # cv2.fillPoly(new_mask, pts=[cnt], color=(255, 255, 255))
    # cv2.imwrite(img_name + '_new_mask.png', imm)
    # print('small contours',i)
    cv2.imwrite(image_name + 'original.jpg', imm2)
    if(i>0):
        cv2.imwrite(image_name + '_res.jpg', im)
        cv2.imwrite(image_name + '_final_res.png', im_f)
    else:
        cv2.imwrite(image_name + '_res.jpg', img)
        cv2.imwrite(image_name + '_final_res.png', f_mask)



def generate_step0_results(image_name):
    th = 2
    mask_image = cv2.imread(os.path.join(image_name + '_mask.png'))
    img = cv2.imread(os.path.join(image_name + '.jpg'))
    th, msk = cv2.threshold(mask_image, 45, 255, cv2.THRESH_BINARY)  # threshold range
    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(255)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imwrite(image_name + '_new_mask.png', opening)
    # cv2.imwrite(image_name + '_res.jpg', im)


def generate_step1_results(image_name):
    th=2
    mask_image = cv2.imread(os.path.join(image_name + '_new_mask.png'))
    img = cv2.imread(os.path.join(image_name + '_res.jpg'))
    f_mask = cv2.imread(os.path.join(image_name + '_final_res.png'))


    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(0)
    gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    contours = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # rest=len(contours)
    # print('rest',rest)
    i=0
    for cnt in contours[1]:
        if (len(cnt) > 2):
            area = cv2.contourArea(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            c_hull = cv2.convexHull(cnt)
            area_hull = cv2.contourArea(c_hull)
            solidity = area / area_hull
            # print(solidity)

            if (solidity > 0.85 or area<250):
                box = np.int0(box)
                im = cv2.drawContours(img, [box], 0, (0, 255, 0),thickness=th)
                im_f = cv2.drawContours(f_mask, [box], 0, (0, 0, 0), thickness=2)
                cv2.fillPoly(f_mask, pts=[box], color=(255, 255, 255))
                i=i+1
            else:
                imm = cv2.drawContours(img_1, [c_hull], 0, (0, 0, 0),thickness=1)
                cv2.fillPoly(img_1, pts=[cnt], color=(255, 255, 255))
    cv2.imwrite(image_name + '_temp1.png', img_1)
    mask_image = cv2.imread(os.path.join(image_name + '_temp1.png'))
    th, msk = cv2.threshold(mask_image, 45, 255, cv2.THRESH_BINARY)  # threshold range
    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(255)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel, iterations=2)
    cv2.imwrite(image_name + '_temp2.png', opening)
    if(i>0):
        cv2.imwrite(image_name + '_res.jpg', im)
        cv2.imwrite(image_name + '_final_res.png', im_f)




def generate_step2_results(image_name):
    th=3
    mask_image = cv2.imread(os.path.join(image_name + '_temp2.png'))
    img = cv2.imread(os.path.join(image_name + '_res.jpg'))
    f_mask = cv2.imread(os.path.join(image_name + '_final_res.png'))

    f=0
    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(0)
    gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    contours = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours[1]:
        if (len(cnt) > 2):
            area = cv2.contourArea(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            c_hull = cv2.convexHull(cnt)
            area_hull = cv2.contourArea(c_hull)
            solidity = area / area_hull
            # print(solidity)
            if (solidity > 0.8 or area<500):
                box = np.int0(box)
                im = cv2.drawContours(img, [box], 0, (0, 255, 0),thickness=th)
                im_f = cv2.drawContours(f_mask, [box], 0, (0, 0, 0), thickness=2)
                cv2.fillPoly(f_mask, pts=[box], color=(255, 255, 255))
                f=1
            else:
                imm = cv2.drawContours(img_1, [c_hull], 0, (0, 0, 0),thickness=1)
                cv2.fillPoly(img_1, pts=[cnt], color=(255, 255, 255))
    cv2.imwrite(image_name + '_temp3.png', img_1)
    if(f>0):
        cv2.imwrite(image_name + '_res.jpg', im)
        cv2.imwrite(image_name + '_final_res.png', im_f)


    mask_image = cv2.imread(os.path.join(image_name + '_temp3.png'))
    th, msk = cv2.threshold(mask_image, 45, 255, cv2.THRESH_BINARY)  # threshold range
    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(255)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    opening = cv2.morphologyEx(msk, cv2.MORPH_OPEN, kernel, iterations=4)
    cv2.imwrite(image_name + '_temp4.png', opening)
    # cv2.imwrite(img_name + '_final_res.png', im_f)



def generate_step3_results(image_name):
    mask_image = cv2.imread(os.path.join(image_name + '_temp4.png'))
    img = cv2.imread(os.path.join(image_name + '_res.jpg'))
    f_mask = cv2.imread(os.path.join(image_name + '_final_res.png'))

    f=0
    img_1 = np.zeros(mask_image.shape, dtype=np.uint8)
    img_1.fill(0)
    gray = cv2.cvtColor(mask_image, cv2.COLOR_BGR2GRAY)
    ret, gray = cv2.threshold(gray, 127, 255, 0)
    contours = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours[1]:
        if (len(cnt) > 2):
            area = cv2.contourArea(cnt)
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            # c_hull = cv2.convexHull(cnt)
            area_hull = cv2.contourArea(c_hull)
            solidity = area / area_hull
            # print(solidity)
            if (solidity > 0.8 or area<250):
                f=1
                box = np.int0(box)
                im = cv2.drawContours(img, [box], 0, (0, 255, 0),thickness=th)
                im_f = cv2.drawContours(f_mask, [box], 0, (0, 0, 0), thickness=2)
                cv2.fillPoly(f_mask, pts=[box], color=(255, 255, 255))

            else:
                f=1
                im = cv2.drawContours(img, [box], 0, (0, 255, 0),thickness=th)
                im_f = cv2.drawContours(f_mask, [box], 0, (0, 0, 0), thickness=2)
                cv2.fillPoly(f_mask, pts=[box], color=(255, 255, 255))
                # print(c_hull)
            # cv2.fillPoly(img, pts=[cnt], color=(255, 255, 255))
    if(f==1):
        cv2.imwrite(image_name + '_res.jpg', im)
        cv2.imwrite(image_name + '_final_res.png', im_f)


def print_output(image_name):
    m_img = cv2.imread(image_name + '_final_res.png')
    img = cv2.imread(os.path.join(image_name + '.jpg'))
    # img_1 = cv2.imread(os.path.join(image_name + '.jpg'))
    gray1 = cv2.cvtColor(m_img, cv2.COLOR_BGR2GRAY)
    ret, gray1 = cv2.threshold(gray1, 127, 255, 0)
    contours = cv2.findContours(gray1, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # contours = sorted(contour_list, key=cv2.contourArea, reverse=True)
    cnt_all = len(contours)
    # print(cnt_all)
    i = 0
    for cnt in contours[1]:

        im = cv2.drawContours(img, [cnt], 0, (0, 255, 0), thickness=th)

    cv2.imwrite(image_name + '_result.jpg', im)
    os.remove(image_name + '_res.jpg')
    os.remove(image_name + '_temp1.png')
    os.remove(image_name + '_temp2.png')
    os.remove(image_name + '_temp3.png')
    os.remove(image_name + '_temp4.png')
    os.remove(image_name + '_new_mask.png')




def regularize_1(img_folder,image_name):

    th=2
    # img_folder='/mnt/vol2/step_2'

    img_name = img_folder+'/'+image_name
    # print(img_name)
    removeOverlapping(img_name)
    generate_step0_results(img_name)

    generate_step1_results(img_name)
    generate_step2_results(img_name)
    generate_step3_results(img_name)
    print_output(img_name)


def regularize(img_folder):
    th = 2
    # img_folder='/mnt/vol2/step_2'

    img_list = os.listdir(img_folder)

    for img in img_list:
        try:
            if (img.split('.')[-1] == 'jpg'):
                print(img)
                img_name = img_folder + '/' + img.split('.')[0]
                # print(img_name)
                removeOverlapping(img_name)
                generate_step0_results(img_name)

                generate_step1_results(img_name)
                generate_step2_results(img_name)
                generate_step3_results(img_name)
                print_output(img_name)
        except Exception as e:
            print(e)



# regularize_1('/mnt/vol2/Satellite_Results','1_data')



