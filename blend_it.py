from PIL import Image

def changeImageSize(maxWidth,maxHeight,im):
    print(im.size)
    widthRatio = maxWidth / im.size[0]
    heightRatio = maxHeight / im.size[1]

    newWidth = int(widthRatio * im.size[0])
    newHeight = int(heightRatio * im.size[1])

    newImage = im.resize((newWidth, newHeight))
    return newImage
    im = Image.open("/home/ceinfo/Desktop/4428.jpg")
    im2 = Image.open("/home/ceinfo/Desktop/1.jpg")
    image3 = changeImageSize(800, 500, im)
    image4 = changeImageSize(800, 500, im2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    alphaBlended2 = Image.blend(image5, image6, alpha=.5)
    alphaBlended2.show()