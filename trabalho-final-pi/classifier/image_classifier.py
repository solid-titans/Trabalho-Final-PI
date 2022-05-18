# This Python file uses the following encoding: utf-8
# Add this to debug

import sys

sys.path.append('../')

import pandas as pd

import utils.image_processor_utils as ImageProcessorUtils
import utils.os_utils as OsUtils
from utils.stopwatch import Stopwatch

import numpy as np

from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score

from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy

from skimage.io import imread

class ImageClassifier():

    def __init__(self) -> None:
        self.__classifier       = svm.SVC(probability=True)
        self.__model            = None
        self.__model_param_grid = {'C':[0.1,1,10,100],'gamma':[0.0001,0.001,0.1,1],'kernel':['rbf','poly']}
        self.__birad_classes    = None

    def train_classifier(self,training_images_folder_path):

        training_timer = Stopwatch()
        training_timer.start()

        flat_data_arr = []
        target_arr    = []

        images_subfolders = OsUtils.folders_in_with_prefix(training_images_folder_path)
        self.__birad_classes     = OsUtils.folders_in(training_images_folder_path)

        for i in range(len(images_subfolders)):

            images = self.__extract_images_from_folder(images_subfolders[i])

            for img in images:

                img = self.__apply_filters_to_image(img)
                texture_descriptor = self.__extract_image_texture_descriptors(img) 
                flat_data_arr.append(texture_descriptor)
                target_arr.append(self.__birad_classes.index(self.__birad_classes[i]))


        flat_data = np.array(flat_data_arr)
        target    = np.array(target_arr)

        df = pd.DataFrame(flat_data)

        df['Target'] = target 

        x = df.iloc[:,:-1]

        y = df.iloc[:,-1]   

        self.__model = GridSearchCV(self.__classifier,self.__model_param_grid)

        x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.75,shuffle=True)

        self.__feed_classifier_with_data(x_train,y_train)

        y_pred = self.__model.predict(x_test)

        print('accuracy score: ', accuracy_score(y_test,y_pred))

        training_timer.stop()

        print('total training time: ', training_timer.get_time() , 's')

    def predict_birad_from_image(self,image):
        
        prediction_timer = Stopwatch()
        prediction_timer.start()

        image_descriptors = self.__extract_image_texture_descriptors(image)
        birad_class = self.__model.predict([image_descriptors])[0]

        prediction_timer.stop()

        return self.__birad_classes[birad_class]

    def __extract_images_from_folder(self,image_folder):

        images = []

        images_paths = OsUtils.get_images_from_path(image_folder)

        for file in images_paths:
            image = imread(file,as_gray=True)
            images.append(image)

        return images

    def __extract_image_texture_descriptors(self,image):

        characteristics = []

        glcm = graycomatrix(image, 
                            [1,2,4,8,16],
                            [0, np.pi / 2, np.pi / 4, np.pi / 8, 3 * np.pi / 4, 5 * np.pi / 8, 7 * np.pi/8],
                            symmetric=False, 
                            normed=True)

        characteristics.append(shannon_entropy(glcm,base=2))
        characteristics.append(graycoprops(glcm,"energy"))
        characteristics.append(graycoprops(glcm,"correlation"))
        characteristics.append(graycoprops(glcm,"dissimilarity"))
        characteristics.append(graycoprops(glcm,"homogeneity"))

        characteristics = np.concatenate(characteristics,axis=None)

        return characteristics 


    def __feed_classifier_with_data(self,x_train,y_train):

        train_model_timer = Stopwatch()
        train_model_timer.start()

        self.__model.fit(x_train,y_train)

        train_model_timer.stop()

    def __apply_filters_to_image(self,image):

        processing_time = Stopwatch()

        processing_time.start()

        #image = ImageProcessorUtils.quantization(image,32)
        #image = ImageProcessorUtils.equalization(image)
        image = ImageProcessorUtils.median_blur(image,3)

        processing_time.stop()

        return image
    
if __name__ == "__main__":

    classifier = ImageClassifier()

    classifier.train_classifier("../assets/training-images")

    image = imread("../assets/training-images/4/p_g_left_cc(12).png", as_gray=True)

    birad = classifier.predict_birad_from_image(image)

    print('image birad:', birad)
