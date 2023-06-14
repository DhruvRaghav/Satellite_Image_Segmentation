import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

for root, dirs, files in os.walk("/home/ceinfo/Desktop/transfer_9_images/",
                                 topdown=False):
    for name in files:
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".jpg":
            x = name[0:-4]
            print("/home/ceinfo/Desktop/transfer_9/" + x + "_mask.png")
            image = cv2.imread("/home/ceinfo/Desktop/transfer_9/" + x + "_mask.png")
            # Read masks

            new = cv2.imread(root + name)  # Read the image
            paper = image.copy()
            # plt.imshow(paper)
            # plt.show()
            ret, thresh_gray = cv2.threshold(cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY), 200, 255, cv2.THRESH_BINARY)

            # contours, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            _, contours, _ = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in contours:
                area = cv2.contourArea(c)

                if area < 300:
                    cv2.fillPoly(thresh_gray, pts=[c], color=0)
                    continue

                rect = cv2.minAreaRect(c)
                (x, y), (w, h), angle = rect
                aspect_ratio = max(w, h) / min(w, h)

            thresh_gray = cv2.morphologyEx(thresh_gray, cv2.MORPH_CLOSE,
                                           cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (150, 150)))

            # cont, hier = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            _, cont, _ = cv2.findContours(thresh_gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

            for c in cont:
                area = cv2.contourArea(c)

                if area < 2000:
                    cv2.drawContours(paper, [c], 0, (0, 0, 0), -1)
                    continue
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)

                box = np.int0(box)
                cv2.drawContours(paper, [box], 0, (255, 255, 255), -1)

            gray = cv2.cvtColor(paper, cv2.COLOR_BGR2GRAY)
            dst = cv2.fastNlMeansDenoising(gray, None, 50, 7, 21)

            # plt.imshow(dst)
            # plt.show()

            # cont, hier = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            _, cont, _ = cv2.findContours(dst, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for c in cont:
                area = cv2.contourArea(c)
                # print(area)
                if area < 2000:
                    # cv2.drawContours(paper, [c], 0, (0, 0, 0), -1)
                    continue
                rect = cv2.minAreaRect(c)
                box = cv2.boxPoints(rect)
                print(area)
                box = np.int0(box)
                cv2.drawContours(new, [box], 0, (0, 255, 0), 7)
                print(name)

            # cv2.imshow('output', new)
            cv2.imwrite("/home/ceinfo/Desktop/transfer_9_result/" + name, new)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()