# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys
import numpy as np

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import QFile, QCoreApplication, Qt
from PySide6.QtUiTools import QUiLoader

from widgets.image_displayer import ImageDisplayer
from widgets.image_plotter   import ImagePlotter

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):

        # Initiate the ui
        super().__init__(*args, **kwargs)
        self.load_ui()
        self.ui.setWindowTitle('Trabalho PI')
        self.connect_ui_signals()

        # Initiate widgets
        self.image_displayer = ImageDisplayer(self.ui.imageLabel)
        self.image_plotter   = ImagePlotter(self.ui.imageInfoColumn)

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

    def connect_ui_signals(self):
        self.ui.openFile.triggered.connect(self.load_image_file)

    def show(self):
        return self.ui.show()

    def load_image_file(self):

        file_path = self.image_displayer.get_image_from_system(self)

        self.ui.statusbar.showMessage('file opened: ' + str(file_path), timeout = 2500)

        self.image_plotter.plot_histogram(self,file_path)

if __name__ == "__main__":

    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    qt_app = QApplication(sys.argv)
    widget = MainWindow()
    widget.show()
    sys.exit(qt_app.exec())
