from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QImage
import cv2, imutils

import utils.image_processor_utils as ImageProcessingUtils

class QuantizationEditor(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadUi()

        self.filename = None 
        self.tempImage = None 
        self.quantization_value = 0

        self.save_image = None

    def set_image_saving_function(self,function):
        self.save_image = function

    def loadUi(self):
        self.setWindowTitle("Training configuration")
        self.setObjectName("MainWindow")
        self.resize(750, 350)
        self.setFixedSize(750, 350)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        """
        Quantization Slider
        """
        self.quantizationLabel= QtWidgets.QLabel(self)
        self.quantizationLabel.setObjectName("quantizationLabel")
        self.quantizationLabel.setText("Quantization: 1")

        self.verticalLayout.addWidget(self.quantizationLabel)

        self.quantizationSlider = QtWidgets.QSlider(self)
        self.quantizationSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.quantizationSlider.setObjectName("quantizationSlider")
        self.verticalLayout.addWidget(self.quantizationSlider)

        self.quantizationSlider.setMinimum(1)
        self.quantizationSlider.setMaximum(32)
        self.quantizationSlider.setValue(1)
        self.quantizationSlider.setTickInterval(1)

        """
        Spacer
        """
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        """
        Save and Cancel Button
        """
        self.saveButton = QtWidgets.QPushButton(self)
        self.saveButton.setObjectName("saveButton")
        self.saveButton.setText("Save")

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancel")

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.horizontalLayout2.addWidget(self.saveButton)
        self.horizontalLayout2.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.cancelButton.clicked.connect(self.cancel_operation)
        self.saveButton.clicked.connect(self.save_quantization)

        self.quantizationSlider.valueChanged['int'].connect(self.change_quantization)

    def cancel_operation(self):
        self.close()

    def change_quantization(self,value):
        self.quantizationLabel.setText("Quantization: " + str(value))
        self.quantization_value = value

    def save_quantization(self):
        self.save_image(self.quantization_value)
        self.close()
