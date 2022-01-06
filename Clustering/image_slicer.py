import cv2
import os
from PIL import Image


path = "/home/ceinfo/Downloads/sampletif/"

for root, dirs, files in os.walk(path, topdown=False):          # slice
    for name in files:
        if os.path.splitext(os.path.join(root, name))[1].lower() == ".tif":
            img = cv2.imread(os.path.join(root, name))
            img1 = name[0:-4]
            print(img1)
            for r in range(0, img.shape[0], 512):
                for c in range(0, img.shape[1], 512):
                    cv2.imwrite(f"/home/ceinfo/Downloads/sampletif/cropped tif/{img1}_{r}_{c}.tif", img[r:r + 512, c:c + 512, :])

# yourpath = "/media/ce00107619/a4f1adca-486c-4569-93b0-952e59adf44e/mnt/BFP-mask-rcnn-master/data/val/new/"
# # outfile = "/home/ce00107619/Downloads/downloaded images"
#
# for root, dirs, files in os.walk(yourpath, topdown=False):  # crop
#     for name in files:
#         if os.path.splitext(os.path.join(root, name))[1].lower() == ".jpg":
#             img_input = os.path.join(name)
#             # print (img_input)
#             string = img_input[0:-4]
#             # print(img_input[0:-5])
#             im = Image.open('/media/ce00107619/a4f1adca-486c-4569-93b0-952e59adf44e/mnt/BFP-mask-rcnn-master/data/val'
#                             '/new/' + img_input)
#             width, height = im.size  # Get dimensions
#             new_width = 3584
#             new_height = 3584
#             left = (width - new_width) / 2
#             top = (height - new_height) / 2
#             right = (width + new_width) / 2
#             bottom = (height + new_height) / 2
#
#             # Crop the center of the image
#             im = im.crop((left, top, right, bottom))
#             im.save('/media/ce00107619/a4f1adca-486c-4569-93b0-952e59adf44e/mnt/BFP-mask-rcnn-master/data/val/test/'+string+'.jpg')



