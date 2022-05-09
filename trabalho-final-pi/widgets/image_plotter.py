# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget,QVBoxLayout

from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from skimage import io

class ImagePlotter(QWidget):
    def __init__(self,*args,**kwargs):
        QWidget.__init__(self,*args,**kwargs)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def remove_children(self):
        for i in reversed(range(self.layout.count())):
            self.imageInfoColumn.itemAt(i).widget().setParent(None)

    def plot_histogram(self,file_path):

        image = io.imread(file_path)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.remove_children()

        self.layout.addWidget(NavigationToolbar(static_canvas, self))
        self.layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()

        self._static_ax.set_xlabel('Intensity Value')
        self._static_ax.set_ylabel('Count')
        self._static_ax.hist(image.ravel(), 256,[0,256])
