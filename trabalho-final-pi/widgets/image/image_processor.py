# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget

import cv2

class ImageProcessor(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)

    def set_image(file_path):
        pass

    #@Slot
    def make_sharpen(self):
        result = ImageProcessorUtils.sharpen(self.image,10,3)


