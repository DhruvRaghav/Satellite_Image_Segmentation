"""PyTorch-compatible datasets.

Guaranteed to implement `__len__`, and `__getitem__`.

See: http://pytorch.org/docs/0.3.1/data.html
"""

# import torch
import cv2
import numpy as np
from PIL import Image
import matplotlib.image as mpimg
# import torch.utils.data
import os
# from robosat.tiles import tiles_from_slippy_map



def tiles_from_slippy_map(root,root1):
    """Loads files from an on-disk slippy map directory structure.

    Args:
      root: the base directory with layout `z/x/y.*`.

    Yields:
      The mercantile tiles and file paths from the slippy map directory.
    """

    # The Python string functions (.isdigit, .isdecimal, etc.) handle
    # unicode codepoints; we only care about digits convertible to int
    def isdigit(v):
        try:
            _ = int(v)  # noqa: F841
            return True
        except ValueError:
            return False

    for z in os.listdir(root):
        if not isdigit(z):
            continue

        for x in os.listdir(os.path.join(root, z)):
            if not isdigit(x):
                continue

            for name in os.listdir(os.path.join(root, z, x)):
                y = os.path.splitext(name)[0]

                if not isdigit(y):
                    continue

                # tile = mercantile.Tile(x=int(x), y=int(y), z=int(z))
                path = os.path.join(root, z, x, name)
                path1=os.path.join(root1,z,x,name)
                yield path,path1



# Single Slippy Map directory structure
class SlippyMapTiles():
    """Dataset for images stored in slippy map format.
    """

    def __init__(self, root1,root2, transform=None):
        super().__init__()

        self.tiles = []
        self.transform = transform

        self.tiles = [(path, path1) for path, path1 in tiles_from_slippy_map(root1,root2)]
        # self.tiles.sort(key=lambda tile: tile[0])

    def __len__(self):
        return len(self.tiles)
    def __getitem__(self, i):
        path, path1 = self.tiles[i]
        image = cv2.imread(path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        # print(Image.open(path))
        # print(image.mode)
        print(os.path.basename(path))
        target= cv2.imread(path1[:-4]+'png')
        target[target == [108, 136, 249]] = 255
        target[target != [255, 255, 255]] = 0
        target=cv2.resize(target,(256,256))

        # if self.transform is not None:
        #     image = self.transform(image)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        mask = np.expand_dims(target, axis=-1)
        mask = mask / 255
        mask[mask < 0.5] = 0
        mask[mask >= 0.5] = 1
        mask = np.array(mask, dtype=np.uint8)
        return image, mask, os.path.basename(path)[:-5]



# Multiple Slippy Map directories.
# Think: one with images, one with masks, one with rasterized traces.
class SlippyMapTilesConcatenation():
    """Dataset to concate multiple input images stored in slippy map format.
    """

    def __init__(self, inputs, target, joint_transform=None):
        super().__init__()

        # No transformations in the `SlippyMapTiles` instead joint transformations in getitem
        self.joint_transform = joint_transform

        self.inputs = [SlippyMapTiles(inp) for inp in inputs]
        self.target = SlippyMapTiles(target)

        assert len(set([len(dataset) for dataset in self.inputs])) == 1, "same number of tiles in all images"
        assert len(self.target) == len(self.inputs[0]), "same number of tiles in images and label"

    def __len__(self):
        return len(self.target)

    def __getitem__(self, i):
        # at this point all transformations are applied and we expect to work with raw tensors
        inputs = [dataset[i] for dataset in self.inputs]

        images = [image for image, _ in inputs]
        tiles = [tile for _, tile in inputs]

        mask, mask_tile = self.target[i]

        assert len(set(tiles)) == 1, "all images are for the same tile"
        assert tiles[0] == mask_tile, "image tile is the same as label tile"

        if self.joint_transform is not None:
            images, mask = self.joint_transform(images, mask)

        return torch.cat(images, dim=0), mask, tiles



#
# # Todo: once we have the SlippyMapDataset this dataset should wrap
# # it adding buffer and unbuffer glue on top of the raw tile dataset.
# class BufferedSlippyMapDirectory(torch.utils.data.Dataset):
#     """Dataset for buffered slippy map tiles with overlap.
#     """
#
#     def __init__(self, root, transform=None, size=512, overlap=32):
#         """
#         Args:
#           root: the slippy map directory root with a `z/x/y.png` sub-structure.
#           transform: the transformation to run on the buffered tile.
#           size: the Slippy Map tile size in pixels
#           overlap: the tile border to add on every side; in pixel.
#
#         Note:
#           The overlap must not span multiple tiles.
#
#           Use `unbuffer` to get back the original tile.
#         """
#
#         super().__init__()
#
#         assert overlap >= 0
#         assert size >= 256
#
#         self.transform = transform
#         self.size = size
#         self.overlap = overlap
#         self.tiles = list(tiles_from_slippy_map(root))
#
#     def __len__(self):
#         return len(self.tiles)
#
#     def __getitem__(self, i):
#         tile, path = self.tiles[i]
#         image = buffer_tile_image(tile, self.tiles, overlap=self.overlap, tile_size=self.size)
#
#         if self.transform is not None:
#             image = self.transform(image)
#
#         return image, torch.IntTensor([tile.x, tile.y, tile.z])
#
#     def unbuffer(self, probs):
#         """Removes borders from segmentation probabilities added to the original tile image.
#
#         Args:
#           probs: the segmentation probability mask to remove buffered borders.
#
#         Returns:
#           The probability mask with the original tile's dimensions without added overlap borders.
#         """
#
#         o = self.overlap
#         _, x, y = probs.shape
#
#         return probs[:, o : x - o, o : y - o]
