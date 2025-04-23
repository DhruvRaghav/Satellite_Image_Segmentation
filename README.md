SATELLITE IMAGE SEGMENTATION - DHRUV RAGHAV

This repository presents a complete workflow for segmenting buildings and roads from satellite imagery using an extended U-Net architecture. It includes data preparation, model training, prediction, and deployment via API.

Documents and References

Single API is available using api_deploy.py. Batch API is not implemented. Batch processing can be done using make_prediction.py. There’s no external GitHub code reference. A project presentation slide deck is included.

Environment Setup

You can create the environment manually or using a YAML file.

For manual setup:First, create and activate the environment using: conda create -n sat_seg_env, followed by conda activate sat_seg_env.Then install the required packages using: pip install tensorflow==1.14.0 flask gdal pandas scikit-learn opencv-python matplotlib numpy keras.

For YAML setup:Export the existing environment using conda env export > footprints1.yml.Then, create a new environment with conda env create --name new_env_name --file footprints1.yml.

Model Architecture

The project uses an extended U-Net model. The encoder is a modified VGG-16 with additional convolutional layers, and the decoder is customized for semantic segmentation. Road segmentation uses a modified U-Net variant with extra convolution layers. All model code is in the Satellite_image_segmentation folder.

Data Preparation

Annotation files include FP_Buildings.csv for buildings and RD_LATLON_WITH_GRID.csv for roads. Each file contains fields like EdgeID, Grid No, Sqn_no, centroid_X, and centroid_Y.

Steps:First, run data_to_xy.py to convert latitude and longitude to pixel coordinates.Then, run gen_fp_masks.py to generate building masks and gen_rd_masks.py for road masks using the pixel coordinate CSV files and original images.

Preprocessing

Run cache_train.py to convert the dataset into .h5 format. This script takes the image and mask paths and outputs three objects: train, train_masks, and train_ids, saved in the cache folder.

Use extra_functions.py to define helper functions:read_image() reads input images, read_mask() loads the corresponding masks, and read_image_test() is used for prediction data.

The dataset is located at /mnt/vol1/Datasets/Satellite_Images/.

Training

Training scripts are train_building.py and train_roads.py. Input data is the .h5 file from the cache/ directory.

Recommended image size for buildings is 512x512 and for roads is 256x256.Train the building model for 50 epochs and the road model for 100 epochs.Snapshots of training weights are saved as .h5 files, and loss/accuracy plots are exported as PDFs.Final output weights for buildings are 45.h5 (city-level, used) and 49.h5 (state-level, not used). For roads: 83.h5 and 100.h5.

Prediction and Validation

Use make_predictions_building.py for predictions.Provide the path for test images, model weights, and the output folder for saving mask images and overlays.Ensure that the test image size matches the training size (512 for buildings, 256 for roads).

API Deployment

Run api_deploy.py to deploy the segmentation model as an API.

Supporting modules:geotiff.py converts PNG to GeoTIFF.predict.py performs cropping, segmentation, and mask stitching.pixel_to_lat_lon.py converts mask pixels to lat/lon and returns a GeoJSON file.

For local testing, use git_api.py and git_predict.py.

Execution Flow

Step-by-step:

Run data_to_xy.py to convert annotations to pixel coordinates.

Run gen_fp_masks.py for building masks and gen_rd_masks.py for road masks.

Run cache_train.py to prepare training data in .h5 format.

Train the models using train_building.py and train_roads.py.

Run predictions using make_predictions_building.py.

Deploy the model using api_deploy.py.

Separate Work

For image cropping, use img_crop.py. root is the path for masks and root1 for input images. They can be the same unless cropping input images based on masks.

GeoJSON generation is done using pixel_to_lat_lon.py or pixel_lat_long.py (reference). The output is a set of contours stored as GeoJSON files. Input folders include images with TAB files and corresponding masks. Output folder is customizable.

Shapefile generation can be done with a .jar file using the command: java -jar yourconverter.jar.

To check the geotagging of an image, use the following Python code:import geoiogeoimg = GeoImage("path/to/image")print(geoimg)

Why Use GPU?

GPUs are ideal for deep learning because they enable stream processing with high throughput. They handle high-latency tasks well, require less cache, and allocate more chip area to computation units. With 10,000+ SIMD threads running in parallel, GPUs significantly reduce training and inference time. They are designed for scalable parallelism and high-performance processing.
