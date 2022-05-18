# This Python file uses the following encoding: utf-8
# Add this to debug

import pandas as pd

import utils.image_processor_utils as ImageProcessorUtils
import utils.os_utils as OsUtils
from utils.stopwatch import Stopwatch

import numpy as np

from sklearn import svm
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, confusion_matrix

from skimage.feature import graycomatrix, graycoprops
from skimage.measure import shannon_entropy

from skimage.io import imread

CHARACTERISTICS_CACHE_FILE_NAME = "classifier_cache.pkl"

class ImageClassifier():

    def __init__(self) -> None:
        self.__classifier       = svm.SVC(probability=True)
        self.__model            = None
        self.__model_param_grid = {'C':[0.5,0.75,1,1.5,2],'gamma':['auto','scale'],'kernel':['rbf','poly']}
        self.__birad_classes    = ['1','2','3','4']
        self.__cache_path       = OsUtils.get_os_tmp_path() + OsUtils.get_os_seperator() + CHARACTERISTICS_CACHE_FILE_NAME
        self.__user_processing_parameters = {}
        self.__confusion_matrix = None

        self.__times = {
            "training" : 0,
            "processing" : 0,
        }

        self.__accuracy    = 0
        self.__specificity = 0

    def get_model_accuracy(self):
        return self.__accuracy

    def get_confusion_matrix(self):
        return self.__confusion_matrix

    def get_specificity(self):
        return self.__specificity

    def get_times(self):
        return self.__times

    def get_model_accuracy(self):
        return self.__accuracy

    def get_times(self):
        return self.__times

    def train_classifier(self,training_images_folder_path,parameters):

        training_timer = Stopwatch()
        training_timer.start()

        df = None

        if OsUtils.exists(self.__cache_path) and self.__user_processing_parameters != parameters:
            df = pd.read_pickle(self.__cache_path)
        else:

            self.__user_processing_parameters = parameters
            texture_arr = []
            birad_arr    = []

            images_subfolders    = OsUtils.folders_in_with_prefix(training_images_folder_path)
            self.__birad_classes = OsUtils.folders_in(training_images_folder_path)

            for i in range(len(images_subfolders)):

                images = self.__extract_images_from_folder(images_subfolders[i])

                for img in images:

                    #img = self.__apply_filters_to_image(img)
                    texture_descriptor = self.__extract_image_texture_descriptors(img) 
                    texture_arr.append(texture_descriptor)
                    birad_arr.append(self.__birad_classes.index(self.__birad_classes[i]))


            flat_data = np.array(texture_arr)
            target    = np.array(birad_arr)

            df = pd.DataFrame(flat_data)
            df['Target'] = target 

            df.to_pickle(self.__cache_path)

        x = df.iloc[:,:-1]
        y = df.iloc[:,-1]   

        self.__model = GridSearchCV(self.__classifier,self.__model_param_grid)

        self.__x_train, self.__x_test, self.__y_train, self.__y_test=train_test_split(x,y,test_size=0.75,shuffle=True)

        self.__feed_classifier_with_data(self.__x_train,self.__y_train)

        y_pred = self.__model.predict(self.__x_test)

        training_timer.stop()

        self.__accuracy = "{:.2f}".format(accuracy_score(self.__y_test,y_pred) * 100)
        self.__specificity = (100 - float(self.__accuracy))/300
        self.__confusion_matrix = confusion_matrix(self.__y_test,y_pred)
        self.__times['training'] = training_timer.get_time()

    def predict_birad_from_image(self,image_file):
        
        prediction_timer = Stopwatch()
        prediction_timer.start()

        image = imread(image_file,as_gray=True)
        new_image = np.array(image, dtype=np.uint8)

        #image             = self.__apply_filters_to_image(image)
        image_descriptors = self.__extract_image_texture_descriptors(new_image)
        birad_class = self.__model.predict([image_descriptors])[0]

        prediction_timer.stop()

        self.__times['prediction'] = prediction_timer.get_time()

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

        if 'quantization' in self.__user_processing_parameters:
            image = ImageProcessorUtils.quantization(image,int(self.__user_processing_parameters['quantization']))

        if 'equalization' in self.__user_processing_parameters:
            image = ImageProcessorUtils.equalization(image)

        if 'median_blur' in self.__user_processing_parameters:
            image = ImageProcessorUtils.median_blur(image,int(self.__user_processing_parameters['median_blur']))
        
        if 'brightness_and_contrast' in self.__user_processing_parameters:
            image = ImageProcessorUtils.brightness_and_contrast(image,
                                                                int(self.__user_processing_parameters['brightness']),
                                                                int(self.__user_processing_parameters['contrast']))

        processing_time.stop()

        self.__times['processing'] = self.__times['processing'] + float(processing_time.get_time())

        return image
    
if __name__ == "__main__":

    classifier = ImageClassifier()

    classifier.train_classifier("../assets/training-images")

    image = imread("../assets/training-images/2/p_e_left_cc(12).png", as_gray=True)

    birad = classifier.predict_birad_from_image(image)

    print('image birad:', birad)
