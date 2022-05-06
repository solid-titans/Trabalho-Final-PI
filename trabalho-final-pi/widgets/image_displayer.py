# This Python file uses the following encoding: utf-8
from PySide6.QtWidgets import QFileDialog, QLabel
from PySide6.QtGui import QPixmap

import cv2
import os

class ImageDisplayer():
    def __init__(self,ui : QLabel):
        self.ui = ui
        self.file_path = ''
        self.ui.mousePressed.connect(

    def get_image_from_system(self,main_window) -> str:
        file = QFileDialog.getOpenFileName(main_window,
            str("Open Image"), os.path.expanduser('~'), str("Image Files (*.png *.jpg)"))

        if not all(file):
            return

        self.file_path = file[0]
        self.ui.setPixmap(QPixmap(self.file_path))

        return self.file_path

    def show_image_in_cv(self):
        pass
