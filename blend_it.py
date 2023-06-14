from PIL import Image

def changeImageSize(maxWidth,maxHeight,im):
    print(im.size)
    widthRatio = maxWidth / im.size[0]
    heightRatio = maxHeight / im.size[1]

    newWidth = int(widthRatio * im.size[0])
    newHeight = int(heightRatio * im.size[1])

    newImage = im.resize((newWidth, newHeight))
    im = Image.open("/mnt/vol2/Dhruv_Raghav/general_unet_model/snapshots/test_1/31_predict.png")
    im2 = Image.open("/mnt/vol2/Dhruv_Raghav/general_unet_model/data/membrane/train/image/31.png")
    image3 = changeImageSize(800, 500, im)
    image4 = changeImageSize(800, 500, im2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    alphaBlended2 = Image.blend(image5, image6, alpha=.5)
    alphaBlended2.show()
    return newImage
