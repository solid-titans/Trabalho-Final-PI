# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QLabel
from PyQt6.QtCore import Qt, pyqtSignal as Signal

import tempfile

import cv2

import os

from widgets.image.image_histogram import ImageHistogram

TMP_FOLDER_NAME = "image_processor/"
TMP_IMAGE_FILE_NAME = "tmp"

class ImageProcessor(QWidget):

    # Custom Signals
    new_image   = Signal(str)
    file_opened = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.__image                  = []
        self.__image_cache            = []
        self.__last_image_path        = ""
        self.__training_images_folder = ""
        self.__folder_path            = os.path.join(tempfile.gettempdir(),TMP_FOLDER_NAME)

        if(not os.path.exists(self.__folder_path)):
            os.mkdir(self.__folder_path)
        else:
            for root, dirs, files in os.walk(self.__folder_path):
                for f in files:
                    os.unlink(os.path.join(root, f))
                for d in dirs:
                    shutil.rmtree(os.path.join(root, d))

    """
    # Open/Save images
    """

    #@Slot
    def load_image_from_system(self):

        #Read image from system
        file = QFileDialog.getOpenFileName(self,
            str("Open Image"), os.path.expanduser('~'), str("Image Files (*.png *.jpg)"))[0]

        if not file:
            return

        self.open_image(file)

    #@Slot
    def open_image(self,file):
        self.file_opened.emit(file)

        image_file_extension = file.split(".")[1]

        self.__image           = cv2.imread(file)
        self.__last_image_path = self.generate_image_file_path(image_file_extension)
        self.__image_cache.append(self.__last_image_path)

        cv2.imwrite(self.__last_image_path,self.__image)

        self.new_image.emit(self.__last_image_path)


    def generate_image_file_path(self,file_extension):
        image_cache_length = len(self.__image_cache)
        return self.__folder_path + TMP_IMAGE_FILE_NAME + str(image_cache_length) + "." + file_extension

    #@Slot
    def save_image(self):

        file = QFileDialog.getSaveFileName(self, "Save File As", os.path.expanduser('~'),filter="JPG(*.jpg);;PNG(*.png)")[0]

        cv2.imwrite(file,self.__image)

    """
    # Filters
    """

    #@Slot
    def apply_sharpen(self):
        pass

    #@Slot
    def apply_gaussian(self):
        pass

    #@Slot
    def apply_brightness_and_contrast(self):
        pass

    """
    # Training images
    """

    #@Slot
    def open_training_images_folder(self):

        file = QFileDialog.getExistingDirectory(self, "Open training images folder",
                                                os.path.expanduser('~'))

        self.__training_images_folder = file


