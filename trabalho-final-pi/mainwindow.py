# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
from PyQt6 import uic

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.loadUi()

        self.setWindowTitle('Trabalho PI')
        self.showMaximized()

    def loadUi(self):
        path = os.fspath(Path(__file__).resolve().parent / "forms/mainwindow.ui")
        uic.loadUi(path,self)

if __name__ == "__main__":

    qt_app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(qt_app.exec())
