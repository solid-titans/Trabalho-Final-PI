# This Python file uses the following encoding: utf-8
import utils.image_processor_utils as ImageProcessorUtils
import utils.os_utils as OsUtils

from utils.stopwatch import Stopwatch

from sklearn import svm

class ImageClassifier():

    def __init__(self) -> None:
        self.__classifier = svm.LinearSVC()

    def train_classifier(self,image_to_predict,training_images_folder_path):
        
        training_images_characteristics = self.get_images_characteristics(training_images_folder_path)

        self.feed_classifier_with_data(training_images_characteristics)

    def get_images_characteristics(self,file_path):
        
        images_subfolders = OsUtils.folders_in_with_prefix(file_path)

        characteristics = ()

        for folder in images_subfolders:
            
            images = OsUtils.get_images_from_path()

            for image in images:
                pass

        return characteristics

    def feed_classifier_with_data(self,image_characteristics):
        pass

    def process_an_image(self,image):

        processing_time = Stopwatch()

        processing_time.start()

        image = ImageProcessorUtils.quantization(32)
        image = ImageProcessorUtils.equalization()
        image = ImageProcessorUtils.median_blur(image,3)

        processing_time.stop()

        return image

    
