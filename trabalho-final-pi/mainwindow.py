# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import Qt
from PyQt6 import uic

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.loadUi()

        self.setWindowTitle('Trabalho PI')

    def loadUi(self):
        path = os.fspath(Path(__file__).resolve().parent / "mainwindow.ui")
        uic.loadUi(path,self)

    def load_image_from_system(self):

        file = QFileDialog.getOpenFileName(self,
            str("Open Image"), os.path.expanduser('~'), str("Image Files (*.png *.jpg)"))

        if not all(file):
            return

        self.imageLabel.set_image(file[0])
        self.imageHistogram.plot_histogram(file[0])

        self.statusbar.showMessage('file opened: ' + str(file[0]), msecs = 2500)

if __name__ == "__main__":

    qt_app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(qt_app.exec())
