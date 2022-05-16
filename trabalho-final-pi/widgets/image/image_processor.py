# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QFileDialog, QLabel, QDialog, QMessageBox
from PyQt6.QtCore import Qt, pyqtSignal as Signal
import numpy as np

import cv2

import utils.image_processor_utils as ImageProcessingUtils
import utils.os_utils as OsUtils

TMP_FOLDER_NAME     = "image_processor/"
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
        self.__folder_path            = OsUtils.join_paths(OsUtils.get_os_tmp_path,TMP_FOLDER_NAME)

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

        file = QFileDialog.getSaveFileName(self, "Save File As", OsUtils.get_user_home(),filter="JPG(*.jpg);;PNG(*.png)")[0]

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

    #@Slot
    def apply_quantization(self):
        self.__image = ImageProcessingUtils.quantization(self.__image,6)
        self.set_image()

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

        self.__training_images_folder = file


    #@Slot
    def train_classifiers(self):

        dlg = QDialog(self)
        dlg.setWindowTitle("Train classifiers")
        dlg.resize(630, 300)
        dlg.exec()




