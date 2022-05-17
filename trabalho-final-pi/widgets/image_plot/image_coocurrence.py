# This Python file uses the following encoding: utf-8
from PyQt6.QtWidgets import QWidget,QVBoxLayout

from matplotlib.backends.backend_qtagg import (
    FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from skimage.feature.texture import graycomatrix, graycoprops

import cv2

class ImageCoocurrence(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def remove_children(self):
        for i in reversed(range(self.layout.count())):
            self.imageInfoColumn.itemAt(i).widget().setParent(None)

    #@Slot
    def plot_image(self,file_path):

        image = cv2.imread(file_path)
        image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        """
        glcm = graycomatrix(image, [1], [0], 256, symmetric=False, normed=True)

        xs = []
        ys = []

        xs.append(graycoprops(glcm, 'dissimilarity')[0, 0])
        ys.append(graycoprops(glcm, 'correlation')[0, 0])

        static_canvas = FigureCanvas(Figure(figsize=(5, 3)))

        self.remove_children()

        self.layout.addWidget(NavigationToolbar(static_canvas, self))
        self.layout.addWidget(static_canvas)

        self._static_ax = static_canvas.figure.subplots()

        self._static_ax.imshow(glcm)
        self._static_ax.show()
        """
