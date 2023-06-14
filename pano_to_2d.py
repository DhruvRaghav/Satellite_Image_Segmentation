import cv2
import numpy as np
import matplotlib as plt


img = cv2.imread("/mnt/vol2/Dhruv_Raghav/DhruvRaghav/dataset/GSAA9387.jpg")

height, width, channels = img.shape

new_width = int(width/2)
new_height = int(height/2)

img2 = cv2.resize(img, (new_width, new_height))

# cv2.imshow("Pano Image", img2)
# cv2.waitKey()
cv2.imwrite("/mnt/vol1/Project_Deployments/satellite_image_segmentation_deploy_v2/api_deploy/uploads2/hello.jpg",img2)
cv2.destroyAllWindows()

# if __name__ == "__main__":
#   main()