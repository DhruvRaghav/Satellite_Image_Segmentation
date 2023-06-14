# from __future__ import division
import numpy as np
# from keras.models import Model
# from keras.layers import Conv2DTranspose, Input, Concatenate, Conv2D, MaxPooling2D, UpSampling2D, Cropping2D
from keras import backend as K
import keras
import h5py
# from keras.layers.normalization import BatchNormalization
from keras.optimizers import Nadam
# from keras.backend import binary_crossentropy
import matplotlib.pyplot as plt
import datetime
import os
from sklearn.model_selection import train_test_split
import random
# from keras.applications import ResNet50
#
from keras.models import model_from_json
#
# def decoderBlock(input,in_channels,out_channels):
#     conv1=Conv2D(in_channels//4,1)(input)
#     norm1=BatchNormalization()(conv1)
#     relu1= keras.layers.advanced_activations.ELU()(norm1)
#     deconv=Conv2DTranspose(filters = in_channels//4,kernel_size = (4,4),padding='valid', strides = (2,2), data_format="channels_last")(relu)
#     norm2=BatchNormalization()(deconv)
#     relu2=keras.layers.advanced_activations.ReLU()(norm2)
#     conv3=Conv2D(out_channels,1)(relu2)
#     norm3=BatchNormalization()(deconv)
#     return norm3
# def LinekNet():
#     inputs = Input((512, 512,3))
#     first = Conv2d(3, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
#     bn1 = BatchNormalization(64, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
#     relu = ReLU(inplace)
#     maxpool = MaxPool2d(kernel_size=3, stride=2, padding=1, dilation=1, ceil_mode=False)
#     return
# model=ResNet50()
# layer1=model.add
# print(model.s)


from segmentation_models import Unet
from segmentation_models.backbones import get_preprocessing
from segmentation_models.losses import bce_jaccard_loss,binary_crossentropy
from segmentation_models.metrics import iou_score
from segmentation_models import Linknet
import tensorflow as tf
def get_session():
    """ Construct a modified tf session.tree.insert(1)
    """
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

img_rows = 512
img_cols = 512


smooth = 1e-12

num_channels = 3
num_mask_channels = 1


def jaccard_coef(y_true, y_pred):
    intersection = K.sum(y_true * y_pred, axis=[0,1,2])
    sum_ = K.sum(y_true + y_pred, axis=[0,1,2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_int(y_true, y_pred):
    y_pred_pos = K.round(K.clip(y_pred, 0, 1))

    intersection = K.sum(y_true * y_pred_pos, axis= [0,1,2])
    sum_ = K.sum(y_true + y_pred_pos, axis=[0,1,2])

    jac = (intersection + smooth) / (sum_ - intersection + smooth)

    return K.mean(jac)


def jaccard_coef_loss(y_true, y_pred):
   return -K.log(jaccard_coef(y_true, y_pred)) + binary_crossentropy(y_pred, y_true)

def flip_axis(x, axis):
    x = np.asarray(x).swapaxes(axis, 0)
    x = x[::-1, ...]
    x = x.swapaxes(0, axis)
    return x


def form_batch(images,masks,batch_size):
    """images is 4D np array of shape [num_images,height,width,num_channels]
       masks is 4D np array of shape [num_images,height,width,mask_channels].
    """
    x_batch = np.zeros((batch_size,img_rows,img_cols,num_channels))
    y_batch = np.zeros((batch_size,img_rows,img_cols,num_mask_channels))
    images_height = images.shape[1]
    images_width = images.shape[2]

    for i in range(batch_size):
        random_width = random.randint(0, images_width - img_cols - 1)
        random_height = random.randint(0, images_height - img_rows - 1)
        random_image = random.randint(0, images.shape[0] - 1)
        y_batch[i] = np.array(masks[random_image,
                                    random_height: random_height + img_rows,
                                    random_width: random_width + img_cols,:])
        x_batch[i] = np.array(images[random_image,
                                     random_height: random_height + img_rows,
                                     random_width: random_width + img_cols,:])
    return x_batch, y_batch


def batch_generator(X, y, batch_size, horizontal_flip=False, vertical_flip=False, swap_axis=False):
    while True:
        X_batch, y_batch = form_batch(X, y, batch_size)

        for i in range(X_batch.shape[0]):
            xb = X_batch[i]
            yb = y_batch[i]

            if horizontal_flip:
                if np.random.random() < 0.5:
                    xb = flip_axis(xb, 0)
                    yb = flip_axis(yb, 0)

            if vertical_flip:
                if np.random.random() < 0.5:
                    xb = flip_axis(xb, 1)
                    yb = flip_axis(yb, 1)

            if swap_axis:
                if np.random.random() < 0.5:
                    xb = xb.swapaxes(0, 1)
                    yb = yb.swapaxes(0, 1)

            X_batch[i] = xb
            y_batch[i] = yb

        yield X_batch, y_batch


def save_model(model, cross):
    json_string = model.to_json()
    if not os.path.isdir('cache'):
        os.mkdir('cache')
    json_name = 'architecture_' + cross + '.json'
    weight_name = 'model_weights_' + cross + '.h5'
    open(os.path.join('cache', json_name), 'w').write(json_string)
    model.save_weights(os.path.join('cache', weight_name), overwrite=True)


def read_model(cross=''):
    json_name = 'architecture_' + cross + '.json'
    weight_name = 'model_weights_' + cross + '.h5'
    model = model_from_json(open(os.path.join('../src/cache', json_name)).read())
    model.load_weights(os.path.join('../src/cache', weight_name))
    return model


if __name__ == '__main__':
    os.environ['TF_ENABLE_AUTO_MIXED_PRECISION'] = '1'
    # keras.backend.tensorflow_backend.set_session(get_session())

    data_path = 'cache'
    version = 2
    batch_size = 1
    nb_epoch = 50
    iters_per_epoch = 500
    snapshot_path = os.path.join('./snapshots', str(datetime.date.today()), str(version))
    callbacks = []
    tensorboard_dir = os.path.join('./snapshots', str(datetime.date.today()), str(version), 'log')
    os.makedirs(tensorboard_dir, exist_ok=True)
    tensorboard_callback = keras.callbacks.TensorBoard(
        log_dir=tensorboard_dir,
        histogram_freq=0,
        batch_size=batch_size,
        write_graph=True,
        write_grads=True,
        write_images=False,
        embeddings_freq=0,
        embeddings_layer_names=None,
        embeddings_metadata=None
    )
    callbacks.append(tensorboard_callback)

    # save the model

    # ensure directory created first; otherwise h5py will error after epoch.
    os.makedirs(snapshot_path, exist_ok=True)
    checkpoint = keras.callbacks.ModelCheckpoint(
        os.path.join(
            snapshot_path,
            '{{epoch:02d}}.h5'.format()
        ),
        verbose=1,
        # save_best_only=True,
        # monitor="mAP",
        # mode='max'
    )
    callbacks.append(checkpoint)

    # callback for best validation accuracy model
    # filepath = "weights.best.hdf5"
    # val_callback = keras.callbacks.ModelCheckpoint(os.path.join(args.snapshot_path, filepath), monitor='val_acc', verbose=1,
    #                                                save_best_only=True, mode='max')
    # callbacks.append(val_callback)

    # callbacks.append(keras.callbacks.ReduceLROnPlateau(
    #     monitor='loss',
    #     factor=0.1,
    #     patience=5,
    #     verbose=1,
    #     mode='auto',
    #     epsilon=0.0001,
    #     cooldown=0,
    #     min_lr=0
    # ))

    now = datetime.datetime.now()

    print('[{}] Creating and compiling model...'.format(str(datetime.datetime.now())))

    with tf.device('/cpu:0'):
        # model = get_unet_deep()
        BACKBONE = 'resnet34'
        model = Linknet(BACKBONE, encoder_weights='imagenet')
        model.compile('Adam', loss=bce_jaccard_loss, metrics=[iou_score])

        print('[{}] Reading train...'.format(str(datetime.datetime.now())))
        f = h5py.File(os.path.join(data_path, 'train_16.h5'), 'r')

        X_train = f['train']
        X_train = np.array(X_train)
        y_train = np.array(f['train_mask'])
        y_train = np.array(y_train)
        train_ids = np.array(f['train_ids'])

        X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.1, random_state=42)

        suffix = 'buildings_3_'
        model.compile(optimizer=Nadam(lr=1e-3), loss=jaccard_coef_loss,
                      metrics=['binary_crossentropy', jaccard_coef_int])

        history = model.fit_generator(
            batch_generator(X_train, y_train, batch_size, horizontal_flip=True, vertical_flip=True, swap_axis=True),
            steps_per_epoch=iters_per_epoch,
            epochs=nb_epoch,
            verbose=1,
            validation_data=batch_generator(X_test, y_test, batch_size, horizontal_flip=False, vertical_flip=False,
                                            swap_axis=False),
            validation_steps=50, callbacks=callbacks)
        save_model(model, "{batch}_{epoch}_{suffix}".format(batch=batch_size, epoch=nb_epoch, suffix=suffix))
        print(history.history.keys())
    # summarize history for accuracy
    fig = plt.figure()
    plt.plot(history.history['jaccard_coef_int'])
    plt.plot(history.history['val_jaccard_coef_int'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    fig.savefig("accuracy_test.pdf", bbox_inches='tight')

    # summarize history for loss
    fig = plt.figure()
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.show()
    fig.savefig("loss_test.pdf", bbox_inches='tight')
    f.close()






















# BACKBONE = 'resnet34'
# preprocess_input = get_preprocessing(BACKBONE)
#
# # load your data
# x_train, y_train, x_val, y_val = load_data(...)
#
# # preprocess input
# x_train = preprocess_input(x_train)
# x_val = preprocess_input(x_val)
#
# # define model
# model = Unet(BACKBONE, encoder_weights='imagenet')
# model.compile('Adam', loss=bce_jaccard_loss, metrics=[iou_score])
#
# # fit model
# model.fit(
#     x=x_train,
#     y=y_train,
#     batch_size=16,
#     epochs=100,
#     validation_data=(x_val, y_val),
# )