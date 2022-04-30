# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox
from PySide6.QtCore import QFile, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QPixmap

from skimage import data, io, filters

import cv2

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        # Initiate the ui
        super().__init__(*args, **kwargs)
        self.load_ui()
        self.ui.setWindowTitle('Trabalho PI')
        self.connect_ui_signals()

        # Initiate variables
        self.file_path = ''

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def connect_ui_signals(self):
        self.ui.openFile.triggered.connect(self.open_image_file)
        self.ui.showImageButton.clicked.connect(self.apply_sobel)


    def show(self):
        return self.ui.show()

    def open_image_file(self):
        file = QFileDialog.getOpenFileName(self,
            str("Open Image"), os.path.expanduser('~'), str("Image Files (*.png *.jpg)"))
        if not all(file):
            return

        self.file_path = file[0]
        self.ui.imageLabel.setPixmap(QPixmap(self.file_path))

    def apply_sobel(self):

        if not self.file_path:
            QMessageBox.critical(
                self,
                "Error!",
                "No image was opened!",
                buttons=QMessageBox.Ok
            )
            return

        img = io.imread(self.file_path)
        edges = filters.sobel(img)
        cv2.imshow('teste',edges)

if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    qt_app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(qt_app.exec())
