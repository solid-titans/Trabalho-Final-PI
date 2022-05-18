# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import pyqtSignal as Signal

import os

import cv2, imutils

DEFAULT_STYLESHEET = """background-color: rgb(28, 25, 32);
                     border-color: rgb(255,255,255);
                     border-style: solid;
                     border-width: 2px;
                     border-radius: 20px;""";

HIGHLIGHTED_STYLESHEET = """background-color: rgb(28, 25, 32);
                         border-color: rgb(250,100,100);
                         border-style: solid;
                         border-width: 2px;
                         border-radius: 20px;""";

class ImageDisplayer(QLabel):

    # Custom Signals
    image_dragged = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.setStyleSheet(DEFAULT_STYLESHEET)

    #@Slot
    def set_image(self,file_path):
        self.file_path = file_path

        image = cv2.imread(file_path)
        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format.Format_RGB888)
        super().setPixmap(QPixmap.fromImage(image))

    """
    Drag and drop event handling
    """
    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            self.setStyleSheet(HIGHLIGHTED_STYLESHEET)
            event.accept()
        else:
            self.setStyleSheet(DEFAULT_STYLESHEET)
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(DEFAULT_STYLESHEET)

    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            self.setStyleSheet(HIGHLIGHTED_STYLESHEET)
            event.accept()
        else:
            self.setStyleSheet(DEFAULT_STYLESHEET)
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.image_dragged.emit(file_path)
            self.setStyleSheet(DEFAULT_STYLESHEET)
            event.accept()
        else:

            event.ignore()
