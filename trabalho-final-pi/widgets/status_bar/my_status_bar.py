# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QStatusBar

class MyStatusBar(QStatusBar):

    def __init__(self, parent=None):
        super().__init__(parent)

    def new_image_loaded(self,file_path):
        self.showMessage('file opened: ' + str(file_path), msecs = 3500)
