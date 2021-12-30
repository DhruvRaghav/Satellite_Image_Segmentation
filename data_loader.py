import cv2
import numpy as np
from datasets1 import tiles_from_slippy_map
import os
# class sat_dataloader():
#     def __int__(self):
class SlippyMapTiles():
    """Dataset for images stored in slippy map format.
    """

    def __init__(self, root1,root2,mmi_root1=None,mmi_root2=None,transform=None):
        super().__init__()

        self.tiles = []
        # self.transform = transform

        # self.tiles = [(path, path1) for path, path1 in tiles_from_slippy_map(root1,root2)]
        # self.tiles.sort(key=lambda tile: tile[0])
        # self.mmi_tiles=[(os.path.join(mmi_root1,image),os.path.join(mmi_root2,image))for image in os.listdir(mmi_root1)]
        if mmi_root2 and mmi_root1 is not None:
            for image in os.listdir(mmi_root1):
                self.tiles.append((os.path.join(mmi_root1,image),os.path.join(mmi_root2,image)))
    def __len__(self):
        return len(self.tiles)
    def item(self, i):
        # print(i)
        path, path1 = self.tiles[i]
        # print(self.tiles[i])
        image = cv2.imread(path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(Image.open(path))
        # print(image.mode)
        # print(os.path.basename(path))
        # print(path1)
        if os.path.basename(path1)[-3:] != 'jpg':
            target= cv2.imread(path1[:-4]+'png')
            if target is None:
                target=cv2.imread(path1)
            target[target == [108, 136, 249]] = 255
            target[target != [255, 255, 255]] = 0
            target=cv2.resize(target,(256,256))
        else:
            target= cv2.imread(path1)
            target = cv2.resize(target, (256, 256))
        # if self.transform is not None:
        #     image = self.transform(image)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        mask = np.expand_dims(target, axis=-1)
        mask = mask / 255
        mask[mask < 0.5] = 0
        mask[mask >= 0.5] = 1
        mask = np.array(mask, dtype=np.uint8)
        return image, mask

