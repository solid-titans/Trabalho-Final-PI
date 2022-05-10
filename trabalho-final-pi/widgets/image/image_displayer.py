# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QFileDialog, QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import pyqtSignal as Signal

import cv2
import os

class ImageDisplayer(QLabel):

    # Custom Signals
    new_image = Signal(str)

    def __init__(self,*args,**kwargs):
        QLabel.__init__(self,*args,**kwargs)
        self.file_path = ''
        self.setAcceptDrops(True)

    #@Slot
    def load_image_from_system(self):
        file = QFileDialog.getOpenFileName(self,
            str("Open Image"), os.path.expanduser('~'), str("Image Files (*.png *.jpg)"))

        if not all(file):
            return

        self.set_image(file[0])

    def set_image(self,file_path):
        self.file_path = file_path
        super().setPixmap(QPixmap(self.file_path))
        self.new_image.emit(file_path)

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
