# Adversarial Learning
# Loads in dataset and preprocesses data, splits data into train and test sets
# Aneja Lab | Yale School of Medicine
# Marina Joel
# Created (10/16/20)
# Updated (12/22/20)

# import dependencies
import tensorflow as tf
import numpy as np
from sklearn.model_selection import train_test_split
from utils import __resize_array_images
import cv2

# Function to load, preprocess, and split data into train/test sets
# Employed (10/16/20)
# Debugged (12/22/20)
# Created By Marina Joel
def load_dataset(dataset, path, aug):
    path = path + dataset + '/'
    if dataset == 'brain_mri':
        # # read in brain mri dataset
        if aug == False:
            # use un-augmented dataset for training
            normal_images = np.load(path + '2000_normal_images.npy')
            normal_labels = np.load(path + '2000_normal_labels.npy')
            tumor_images = np.load(path + '2000_tumor_images.npy')
            tumor_labels = np.load(path + '2000_tumor_labels.npy')
            x = np.concatenate((normal_images, tumor_images))
            y = np.concatenate((normal_labels, tumor_labels))
            # split dataset into training and testing sets
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
            # convert class vectors to binary class matrices
            y_train = tf.keras.utils.to_categorical(y_train, 2)
            y_test = tf.keras.utils.to_categorical(y_test, 2)
        elif aug == True:
        # read in augmented dataset
            x_train = np.load(path + 'x_train_aug.npy')
            x_train = np.squeeze(x_train, axis=1)
            y_train = np.load(path + 'y_train_aug.npy')
            y_train = np.squeeze(y_train, axis=1)
            x_test = np.load(path + '/' + 'x_test.npy')
            y_test = np.load(path + '/' + 'y_test.npy')

    elif dataset == 'mnist':
        # read in MNIST dataset
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()
        x_train = np.expand_dims(x_train, -1)
        x_test = np.expand_dims(x_test, -1)

        # resize images from 28x28 to 32x32, change from 1 channel to 3 channels
        x_train = __resize_array_images(x_train, 32)
        x_train = np.stack((x_train, x_train, x_train), axis=3)

        x_test = __resize_array_images(x_test, 32)
        x_test = np.stack((x_test, x_test, x_test), axis=3)
        # convert class vectors to binary class matrices
        y_train = tf.keras.utils.to_categorical(y_train, 10)
        y_test = tf.keras.utils.to_categorical(y_test, 10)

    elif dataset == 'ddsm':
        if aug == False:
            # read in CBIS-DDSM dataset
            x_train = np.load(path + 'CBIS_DDSM_x.npy')
            y_train = np.load(path + 'CBIS_DDSM_y.npy')
            x_test = np.load(path + 'CBIS_DDSM_Test_x.npy')
            y_test = np.load(path + 'CBIS_DDSM_Test_y.npy')
            y_train = tf.keras.utils.to_categorical(y_train, 2)
            y_test = tf.keras.utils.to_categorical(y_test, 2)

        elif aug == True:
            x_train = np.load(path + 'x_train_aug.npy')
            x_train = np.squeeze(x_train, axis=1)
            y_train = np.load(path + 'y_train_aug.npy')
            y_train = np.squeeze(y_train, axis=1)
            x_test = np.load(path + 'CBIS_DDSM_Test_x.npy')
            y_test = np.load(path + 'CBIS_DDSM_Test_y.npy')
            y_test = tf.keras.utils.to_categorical(y_test, 2)


    elif dataset == 'cifar':
        # read in CIFAR10 dataset
        (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
        y_train = tf.keras.utils.to_categorical(y_train, 10)
        y_test = tf.keras.utils.to_categorical(y_test, 10)

    elif dataset == 'lidc':
        if aug == False:
            # read in LIDC dataset
            x = np.load(path + 'x_balanced.npy')
            y = np.load(path + 'y_balanced.npy')
            # split dataset into training and testing sets
            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)
            np.save(path + 'x_train.npy', x_train)
            np.save(path + 'x_test.npy', x_test)
            np.save(path + 'y_train.npy', y_train)
            np.save(path + 'y_test.npy', y_test)

        elif aug == True:
            x_train = np.load(path + 'x_train_aug.npy')
            x_train = np.squeeze(x_train, axis=1)
            y_train = np.load(path + 'y_train_aug.npy')
            y_train = np.squeeze(y_train, axis=1)
            x_test = np.load(path + 'x_test.npy')
            y_test = np.load(path + 'y_test.npy')

            # convert class vectors to binary class matrices
            y_test = tf.keras.utils.to_categorical(y_test, 2)

    # convert integers to floats
    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    y_train = y_train.astype('float32')
    y_test = y_test.astype('float32')

    # preprocess data (scale images to [0, 1] range
    x_train = cv2.normalize(x_train, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
    x_test = cv2.normalize(x_test, None, alpha = 0, beta =1, norm_type = cv2.NORM_MINMAX, dtype = cv2.CV_32F)
    return x_train, y_train, x_test, y_test
