# This Python file uses the following encoding: utf-8
import sys

sys.path.append('../')

import utils.image_processor_utils as ImageProcessorUtils
import utils.os_utils as OsUtils
from utils.stopwatch import Stopwatch

import numpy as np

import cv2 as cv

from sklearn import svm
from sklearn.model_selection import train_test_split

from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy


class ImageClassifier():

    def __init__(self) -> None:
        self.__classifier = svm.LinearSVC()

    def train_classifier(self,training_images_folder_path):

        training_timer = Stopwatch()

        training_timer.start()

        images_subfolders = OsUtils.folders_in_with_prefix(training_images_folder_path)
        #birad_classes     = OsUtils.folders_in(training_images_folder_path)

        for i in range(len(images_subfolders)):

            training_data = []
            test_data     = []

            images = self.__extract_images_from_folder(images_subfolders[i])

            training_imgs_split, test_imgs_split = train_test_split(images, train_size=75, shuffle=False)

            for img in training_imgs_split:

                texture_descriptor = self.__extract_image_texture_descriptors(img)
                training_data.append(texture_descriptor)

            for img in test_imgs_split:

                texture_descriptor = self.__extract_image_texture_descriptors(img)
                test_data.append(texture_descriptor)

            self.__feed_classifier_with_data(training_data,test_data)

        training_timer.stop()

    def predict_birad_from_image(self,image):
        
        prediction_timer = Stopwatch()
        prediction_timer.start()

        image_descriptors = self.__extract_image_texture_descriptors(image)
        birad_class = self.__classifier.predict([image_descriptors])

        prediction_timer.stop()

        return birad_class

    def __extract_images_from_folder(self,image_folder):

        images = []

        images_paths = OsUtils.get_images_from_path(image_folder)
        images = [cv.imread(file) for file in images_paths]

        return images

    def __extract_image_texture_descriptors(self,image):

        image = self.__apply_filters_to_image(image)

        characteristics = {}

        glcm = graycomatrix(image, [1,2,4,8,16],[0, np.pi/4, np.pi/2, 3*np.pi/4], levels=32,symmetric=False, normed=True)

        characteristics["entropy"]       = shannon_entropy(glcm,base=2)
        characteristics["energy"]        = graycoprops(glcm,"energy")
        characteristics["correlation"]   = graycoprops(glcm,"correlation")
        characteristics["dissimilarity"] = graycoprops(glcm,"dissimilarity")

        return characteristics


    def __feed_classifier_with_data(self,training,test):

        train_model_timer = Stopwatch()
        train_model_timer.start()

        self.__classifier.fit(training,test)

        train_model_timer.stop()

    def __apply_filters_to_image(self,image):

        processing_time = Stopwatch()

        processing_time.start()

        image = ImageProcessorUtils.quantization(image,32)
        #image = ImageProcessorUtils.equalization(image)
        image = ImageProcessorUtils.median_blur(image,3)
        
        processing_time.stop()

        return image

    
if __name__ == "__main__":

    classifier = ImageClassifier()

    classifier.train_classifier("../assets/training-images")
