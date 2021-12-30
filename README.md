SATELLITE IMAGE SEGMENTATION 
-DHRUV RAGHAV



CONTENTS

    1. Documents and References
    2. Environment Creation
    3. Model Architecture
    4. Data Preparation
    5. Pre-processing
    6. Training Model
    7.  Validations and Prediction
    8. Code and Implementation
    9. Miscellaneous 
    10. Seperate Work



CHAPTER-1
Documents and References:
    1. Single Api - Yes(api_deploy.py)
    2. Batch Api - No
    3. Batch processing - make_prediction.py
    4. Github Code Reference - No
    5. PPT – Yes



CHAPTER-2 : Environment Creation:(footprints 1.yml)
There are two ways to create enviornment. Below are the mentioned ways :
    • Manual installing packages in an enviornment.
    • Installing packages in the enviornment via YML file
Manual installing packages in an enviornment
    • open terminal window of any python IDLE you are using
    • create the enviornment
        1) conda create env_name
    • Activate the enviornment
        1) conda activate env_name
    • Install packages using pip command or conda command.
        1) pip install package_name
        1) conda install package_name
packages to be installed : 
    1. Tensorflow 1.14.0 with gpu same version
    2. flask
    3. Gdal and Geoio
    4. Pandas
    5. Scikit-learn
    6. open cv - 3.4.6 above version
    7. Matplotlib 
    8. Numpy
    9. Keras
       
       
       Installing packages in the enviornment via YML file
     1  Create yml file on the terminal of the IDLE:
         1.1  Activate the enviornment whose yaml file you want to create
         1.2  Export the enviornment whose yaml file you want to create using the following command :
                     Conda env export > enviornment_name1 .yml
         1.3  Create the new enviornment where you want to import the packages of the predecessor enviornment using the following command:
           conda env create -–name enviornment_name2 -–file= enviornment_name1.yml
 	


CHAPTER-3 : Model Architecture (Unet)
Building:
Extended U-net is used in building segmentation which contains extended vgg16 model as encoder and decoder. Extended vgg includes addition of convolutional layers in vgg16 model. 
Road:
Modified U-net is used in road segmentation where some convolutions layers are added.
Code folder:
Satellite_image_segmentation




CHAPTER-4 :DATA PREPARATION

Annotations reading and conversion:
    1. We will be taking annotations from annotators and corresponding images with TAB files. Then we will run data_to_xy file which converts the lat lon in the tab file  into pixels and save that pixels into a  csv file separately.
    2. We will provide saved pixels csv path(The csv which is created in the data_to_xy file) as input  with same corresponding images with TAB files into gen_fp_masks.py and we will get masks out of that and masks will be stored at one place.( To the address one will provide)
    3. Same goes  for Roads.(data_to_xy) & (gen_rd_masks.py)
    1. Annotation Type:(CSV files for road and building footprints)
       (   CSV file for Building : FP_Buildings.csv   ) 
       (   CSV file for Roads : RD_LATLON_WITH_GRID.csv  )
EdgeID - unique number which defines each building or road.
Grid No - image name
Sqn_no - (road structure or building structure )represents sequence of points
centroid_X,y - latitude and longitude.
    2. MASKS GENERATION THROUGH ANNOTATIONS :
Data_to_xy.py
Input - annotation Csv path(which has values in lat long form),Image folder path,output csv path
Output - path where csv(values in pixels form) to be stored.

Gen_fp_masks.py for buildings
Input : data_to_xy generated csv path ,image folder path, output path to store images
Output : masks images 
Gen_rd_masks.py for roads
Input : data_to_xy generated csv path ,image folder path, output images path
Output : masks images 
/mnt/vol1/TTS_Test_data/Tacotron



CHAPTER-5:

PREPROCESSING
File names = Cache_train.py, Extra_functions.py
Dataset_path = /mnt/vol1/Datasets/Satellite_Images/

    1. Cache_train.py- masks path as an input and h5 file name can be changed.it is the final data for training. This will be in h5 format {a.train(input images),b. train_ masks, c. train_ids(filenames or image name)} and finally it will be saved in cache folder.
    2. Extra_functions.py-
    1. in read_image function, we will be providing input images path.
    2. In Read_mask function,we will be providing masks path. (Same given in cache_train.py)
    3. Read_image_test function,test images path on which we want to do predictions.





CHAPTER-6:

TRAINING MODEL
File name= train_roads.py and Train_building.py (other reference file: train_building_test.py and train_building.py)
        Data usage : 4800*3705 for building (41 images) jpg with tab files
                              4800*3705 for roads (27 images) jpg with tab files
    1. Image size can be different (best size for buildings = 512 and for roads=256)
    2. Number of epochs can be different (buildings= 50 and roads = 100)
    3. Number of steps under epochs ,we have to give after dividing folder images with epochs.This won’t take automatically.
    4. Training data will be given in .h5 file from cache in f variable and provide data_path “cache” in the program
    5. .snapshots will be saving the training weights
    6. Loss pdf and accuracy pdf will be saved in the end of training and we will find the best weights out of this by guessing.
Output weights for buildings : 45.h5(citylevel) currently used,49.h5(state level)not used.
Output weights for Roads: 100.h5(citylevel) and 83.h5 (citylevel),state level not trained.




CHAPTER-7:

VALIDATIONS /Predictions
File name = make_predictions_building.py
Paths = Model loading path
Test images folder and same path will be given in extra functions too and it will be called automatically
Output saving path for masks (masks will be an output) and overlays too
Important = Testing images size should be same training images in code.(512- buildings and 256 for roads)

API_DEPLOYMENT:
RUN - API_Deploy.py (model loaded globally)
Geotiff.py - gdal_convert() function - infile is input_image from UI in the png format,outfile will be having tif extension of same input image converted by gdal function below in the code.Tab file is also being created in ‘f’ variable and saved in provided path in upload folder
Predict.py - predict(model,image_id,graph,image_size) function -  make_prediction_cropped function will be called from extra_functions.py where cropping will be done and return mask.predict function will concatenate 4 predicted mask and final mask will be generated and stored in upload folder. 
Pixel_to_lat_lon.py - geojson() function - tif and mask files get read and removed from upload folder.we are converting pixels to lat_long and finding contours with india latitude and longitude. At last we are returning Geo json as output of API and removing tab file.
Git_api_test:
Git_api.py = Model loaded locally
Git_predict.py = model loading.



CHAPTER-8:

CODE AND IMPLEMENTATION
Postman body parameters: name(pass without image extension),southeast,northwest and bounds(se and nw same)

Steps to Run the files from start
    1. Run data_to_xy.py to generate pixels csv from annotated lat long csv.
    2. Run gen_fp_masks.py to generate masks of building and for roads gen_rd_masks.py
    3. Run cache_train.py to generate training data in h5 format.
    4. Run train_building.py  and training_roads.py
    5. Run Make_predictions_buildings.py
    6. Api_deploy.py















CHAPTER-9:
MISCELLANEOUS
Redis -server : after installation of redis we need to run redis-server.sh file by using >> ./redis-server.sh 
Celery : celery -A <celery-config-file> worker --loglevel=info

Note: for frontend code we need to uncomment all os.remove lines and for postman testing we need to comment that os.remove code lines.





























CHAPTER-10:
Separate Work 

Cropping of images - img_crop.py
    1. Root and root1 can be the same for mask cropping and input images cropping also.
    2. But if we want to crop input images wrt to masks then root1 will be input images and root will be masks path

GEOJSON CREATION
Pixel_to_lat_lon.py(final file) and pixel_lat_long(ref file)
We can change the tiff extension into jpg or png if required And contours will get stored from masks into geojson
Input folders= input images with TAB files in data_path and corresponding masks in data_path2
Output path = where geojson will get stored can be anything
SHAPE FILE CREATION :
java -jar <jar-file-name>.jar <geojson-folder path> <output-shapefile-path>






TO CHECK GEOTAGGING OF AN IMAGE(to know the lat longs of the image)
import geoio
geoimg=GeoImage(“file path”
print(geoimg)

WHY GPU
    1) GPUs use stream processing to achieve high throughput
    2) GPUs designed to solve problems that tolerate high latencies
    3) High latency tolerance
    4) Lower cache requirements
    5) Less transistor area for cache
    6) More area for computing units
    7) More computing units
    8) 10,000s of SIMD threads and high throughput
       GPUs win ☺
Additionally:
• Easier to increase parallelism by adding more processors
• So, fundamental unit of a modern GPU is a stream processor...
