window = rasterio.windows.Window(, 0, 1000, 490)
filepath="/mnt/vol2/Dhruv_Raghav/DATES/28_june/Chunk_01.tif"
with rasterio.open(filepath) as src:
    subset = src.read(1, window=window)

plt.figure(figsize=(16,18.5))
plt.imshow(subset)