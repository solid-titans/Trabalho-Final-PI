# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QStatusBar

class MyStatusBar(QStatusBar):

    def __init__(self,*args,**kwargs):
        QStatusBar.__init__(self,*args,**kwargs)

    def new_image_loaded(self,file_path):
        self.showMessage('file opened: ' + str(file_path), msecs = 2500)
