# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap

import cv2
import os

class ImageDisplayer(QLabel):

    def __init__(self,*args,**kwargs):
        QLabel.__init__(self,*args,**kwargs)
        self.file_path = ''
        self.setAcceptDrops(True)

    def set_image(self,file_path):
        self.file_path = file_path
        super().setPixmap(QPixmap(self.file_path))

    def show_image_in_cv(self):
        pass

    """
    Drag and drop event handling
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.set_image(file_path)

            event.accept()
        else:
            event.ignore()
