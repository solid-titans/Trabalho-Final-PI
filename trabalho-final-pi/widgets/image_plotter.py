# This Python file uses the following encoding: utf-8
from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure

from skimage import io

class ImagePlotter:
    def __init__(self,ui):
        self.ui = ui

    def remove_children(self):
        for i in reversed(range(self.ui.count())):
            self.ui.itemAt(i).widget().setParent(None)

    def plot_histogram(self,main_window,file_path):

        image = io.imread(file_path)

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.remove_children()

        self.ui.addWidget(NavigationToolbar(static_canvas, main_window))
        self.ui.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()

        self._static_ax.set_xlabel('Intensity Value')
        self._static_ax.set_ylabel('Count')
        self._static_ax.hist(image.ravel(), 256,[0,256])
