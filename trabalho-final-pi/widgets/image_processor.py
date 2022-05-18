# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget, QFileDialog, QMessageBox
from PyQt6.QtCore import pyqtSignal as Signal
import numpy as np

import cv2

from skimage.io import imread

import utils.image_processor_utils as ImageProcessingUtils
import utils.os_utils as OsUtils

from widgets.image_edit.brightness_contrast_editor import BrightnessContrastEditor
from widgets.image_edit.median_blur_editor import MedianBlurEditor
from widgets.image_edit.quantization_editor import QuantizationEditor
from widgets.training_qdialog.training_setup import TrainingSetup

from classifier.image_classifier import ImageClassifier

TMP_FOLDER_NAME     = "image_processor/"
TMP_IMAGE_FILE_NAME = "tmp"

class ImageProcessor(QWidget):

    # Custom Signals
    new_image         = Signal(str)
    file_opened       = Signal(str)
    training_finished = Signal(str,str,str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__image                  = []
        self.__image_cache            = []
        self.__last_image_path        = ""
        self.__training_images_folder = ""
        self.__image_file_extension   = ""
        self.__folder_path            = OsUtils.join_paths(OsUtils.get_os_tmp_path(),TMP_FOLDER_NAME)

        self.__image_classifier = ImageClassifier()

        OsUtils.create_folder(self.__folder_path)

    """
    # Open/Save images
    """

    #@Slot
    def load_image_from_system(self):

        #Read image from system
        file = QFileDialog.getOpenFileName(self,
            str("Open Image"), OsUtils.get_user_home(), filter="JPG(*.jpg);;PNG(*.png)")[0]

        if not file:
            return

        self.open_image(file)

    #@Slot
    def open_image(self,file):
        self.file_opened.emit(file)

        self.__image_file_extension = file.split(".")[1]
        self.__image                = cv2.imread(file)

        self.set_image()

    def generate_image_file_path(self):
        image_cache_length = len(self.__image_cache)
        self.__image_cache.append(self.__last_image_path)
        return self.__folder_path + TMP_IMAGE_FILE_NAME + str(image_cache_length) + "." + self.__image_file_extension

    def set_image(self):
        self.__last_image_path = self.generate_image_file_path()

        cv2.imwrite(self.__last_image_path,self.__image)

        self.new_image.emit(self.__last_image_path)

    #@Slot
    def save_image(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        file = QFileDialog.getSaveFileName(self, "Save File As", OsUtils.get_user_home(),filter="JPG(*.jpg);;PNG(*.png)")[0]

        if not file:
            return

        cv2.imwrite(file,self.__image)

    """
    # Filters
    """

    def save_filtered_image(self,image):
        self.__image = image
        self.set_image()

    #@Slot
    def apply_sharpen(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        self.__image = ImageProcessingUtils.sharpen(self.__image)
        self.set_image()

    #@Slot
    def apply_gaussian(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        ui = MedianBlurEditor(self)
        ui.set_image_saving_function(self.save_filtered_image)
        ui.loadImage(self.__last_image_path)
        ui.exec()

    #@Slot
    def apply_brightness_and_contrast(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        ui = BrightnessContrastEditor(self)
        ui.set_image_saving_function(self.save_filtered_image)
        ui.loadImage(self.__last_image_path)
        ui.exec()

    #@Slot
    def apply_equalization(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        self.__image = ImageProcessingUtils.equalization(self.__image)
        self.set_image()

    def set_quantization(self,value):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        self.__image = ImageProcessingUtils.quantization(self.__image,value)
        self.set_image()

    #@Slot
    def apply_quantization(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        ui = QuantizationEditor(self)
        ui.set_image_saving_function(self.set_quantization)
        ui.exec()


    """
    # Training images
    """

    #@Slot
    def open_training_images_folder(self):

        file = QFileDialog.getExistingDirectory(self, "Open training images folder",
                                                OsUtils.get_user_home())

        if not np.array_equal(OsUtils.folders_in(file),['4','3','1','2']):
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error on loading training images folder!")
            msg.setInformativeText("Please choose a folder which has folders named \'1\',\'2\',\'3\',\'4\'")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        self.__training_images_folder = file


    #@Slot
    def setup_training(self):

        ui = TrainingSetup(self)
        ui.set_training_function(self.train_classifier)
        ui.set_training_images_folder_path(self.__training_images_folder)
        ui.exec()

    def train_classifier(self,file_path,parameters):
        
        self.__image_classifier.train_classifier(file_path,parameters)

        msg = QMessageBox()

        msg.setText("The training is complete!")
        msg.setInformativeText("Training accuracy " + str(self.__image_classifier.get_model_accuracy()))
        msg.setDetailedText("Total training time: " + str(self.__image_classifier.get_times()["training"]) + "s\n"
                            + "Processing time: " + str(self.__image_classifier.get_times()["processing"]) )
        msg.setWindowTitle("Training")

        msg.exec()

        self.training_finished.emit(str(self.__image_classifier.get_confusion_matrix()),
                                    str(self.__image_classifier.get_model_accuracy()),
                                    str(self.__image_classifier.get_specificity()))

    def predict_birads(self):

        if not self.__last_image_path:
            msg = QMessageBox()

            msg.setIcon(QMessageBox.Icon.Critical)
            msg.setText("Error")
            msg.setInformativeText("Image not loaded")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        birad = self.__image_classifier.predict_birad_from_image(self.__last_image_path)

        msg = QMessageBox()

        msg.setText("A prediction was made!")
        msg.setInformativeText("The bi-rads of the image is: " + str(birad))
        msg.setDetailedText("Time to predict: " + str(self.__image_classifier.get_times()["prediction"]) + "s")
        msg.setWindowTitle("Predict BI-RADS")

        msg.exec()


