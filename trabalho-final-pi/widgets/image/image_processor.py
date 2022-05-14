# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QLabel, QDialog
from PyQt6.QtCore import Qt, pyqtSignal as Signal

import tempfile
import os

import cv2

import utils.image_processor_utils as ImageProcessingUtils
import utils.os_utils as OsUtils

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
        self.__image_file_extension   = ""
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

        file = QFileDialog.getSaveFileName(self, "Save File As", os.path.expanduser('~'),filter="JPG(*.jpg);;PNG(*.png)")[0]

        if not file:
            return

        cv2.imwrite(file,self.__image)

    """
    # Filters
    """

    #@Slot
    def apply_sharpen(self):
        self.__image = ImageProcessingUtils.sharpen(self.__image)
        self.set_image()

    #@Slot
    def apply_gaussian(self):
        self.__image = ImageProcessingUtils.gaussian_blur(self.__image)
        self.set_image()

    #@Slot
    def apply_brightness_and_contrast(self):
        print("brightness and constrast de corno")

    #@Slot
    def apply_equalization(self):
        self.__image = ImageProcessingUtils.equalization(self.__image)
        self.set_image()

    """
    # Training images
    """

    #@Slot
    def open_training_images_folder(self):

        file = QFileDialog.getExistingDirectory(self, "Open training images folder",
                                                os.path.expanduser('~'))                                

        self.__training_images_folder = file


    #@Slot
    def train_classifiers(self):

        dlg = QDialog(self)
        dlg.setWindowTitle("Train classifiers")
        dlg.resize(630, 300)
        dlg.exec()


