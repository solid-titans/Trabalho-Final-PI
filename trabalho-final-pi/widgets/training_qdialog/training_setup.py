from PyQt6 import QtCore, QtWidgets
from PyQt6.QtWidgets import QDialog

import utils.os_utils as OsUtils

import numpy as np

class TrainingSetup(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadUi()

        self.medianBlurValue = 0
        self.equalizeImage = False 
        self.brightnessValue = 0 
        self.contrastValue = 0
        self.quantization = 2

        self.train= None

    def set_training_function(self,function):
        self.train = function

    def loadUi(self):
        self.setWindowTitle("Training configuration")
        self.setObjectName("MainWindow")
        self.resize(750, 510)
        self.setFixedSize(750, 510)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")

        """
        Training path
        """
        self.trainingPathLabel = QtWidgets.QLabel(self)
        self.trainingPathLabel.setObjectName("trainingPathLabel")
        self.trainingPathLabel.setText("Training images path")
        self.verticalLayout.addWidget(self.trainingPathLabel)

        self.trainingImagesPath = QtWidgets.QLineEdit(self)
        self.trainingImagesPath.setEnabled(False)
        self.trainingImagesPath.setObjectName("trainingImagesPath")

        self.searchFolderButton = QtWidgets.QPushButton(self)
        self.searchFolderButton.setObjectName("searchFolderButton")
        self.searchFolderButton.setText("Select path")

        self.trainingLayout = QtWidgets.QHBoxLayout()
        self.trainingLayout.setObjectName("trainingLayout")
        self.trainingLayout.addWidget(self.trainingImagesPath)
        self.trainingLayout.addWidget(self.searchFolderButton)
        self.verticalLayout.addLayout(self.trainingLayout)

        """
        Median Blur Slider
        """
        self.medianBlurLabel = QtWidgets.QLabel(self)
        self.medianBlurLabel.setObjectName("medianBlurLabel")
        self.medianBlurLabel.setText("Median Blur: ")
        self.verticalLayout.addWidget(self.medianBlurLabel)

        self.medianBlurSlider = QtWidgets.QSlider(self)
        self.medianBlurSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.medianBlurSlider.setObjectName("medianBlurSlider")
        self.verticalLayout.addWidget(self.medianBlurSlider)

        """
        Brightness Slider
        """
        self.brightnessLabel = QtWidgets.QLabel(self)
        self.brightnessLabel.setObjectName("brightnessLabel")
        self.brightnessLabel.setText("Brightness: ")
        self.verticalLayout.addWidget(self.brightnessLabel)

        self.brightnessSlider = QtWidgets.QSlider(self)
        self.brightnessSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.verticalLayout.addWidget(self.brightnessSlider)

        """
        Contrast Slider
        """
        self.contrastLabel = QtWidgets.QLabel(self)
        self.contrastLabel.setObjectName("contrastLabel")
        self.contrastLabel.setText("Contrast: ")
        self.verticalLayout.addWidget(self.contrastLabel)

        self.contrastSlider = QtWidgets.QSlider(self)
        self.contrastSlider.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.contrastSlider.setObjectName("contrastSlider")
        self.verticalLayout.addWidget(self.contrastSlider)

        """
        Equalization
        """

        self.equalizationCheckbox = QtWidgets.QCheckBox(self, text="Equalize image:")
        self.equalizationCheckbox.setObjectName("equalizationCheckbox")
        self.equalizationCheckbox.setChecked(False)
        self.verticalLayout.addWidget(self.equalizationCheckbox)        

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

        self.quantizationSlider.setMinimum(2)
        self.quantizationSlider.setMaximum(32)
        self.quantizationSlider.setValue(2)
        self.quantizationSlider.setTickInterval(1)

        """
        Spacer
        """
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        """
        Training and Cancel Button
        """
        self.trainingButton = QtWidgets.QPushButton(self)
        self.trainingButton.setObjectName("trainingButton")
        self.trainingButton.setText("Train")

        self.cancelButton = QtWidgets.QPushButton(self)
        self.cancelButton.setObjectName("cancelButton")
        self.cancelButton.setText("Cancel")

        self.horizontalLayout2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout2.setObjectName("horizontalLayout2")
        self.horizontalLayout2.addWidget(self.trainingButton)
        self.horizontalLayout2.addWidget(self.cancelButton)

        self.verticalLayout.addLayout(self.horizontalLayout2)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        QtCore.QMetaObject.connectSlotsByName(self)

        self.cancelButton.clicked.connect(self.cancel_operation)
        self.trainingButton.clicked.connect(self.start_training)
        self.searchFolderButton.clicked.connect(self.search_training_folder)

        self.brightnessSlider.valueChanged['int'].connect(self.set_brightness_value)
        self.contrastSlider.valueChanged['int'].connect(self.set_contrast_value)
        self.medianBlurSlider.valueChanged['int'].connect(self.set_median_blur_value)
        self.quantizationSlider.valueChanged['int'].connect(self.change_quantization)
        self.equalizationCheckbox.toggled.connect(self.set_equalization)


    def cancel_operation(self):
        self.close()

    def start_training(self):

        if not self.trainingImagesPath.text():
            msg = QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setText("Error!")
            msg.setInformativeText("No path to training images was configured")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        parameters = {"brightness": self.brightnessValue,
                      "contrast":   self.contrastValue,
                      "median_blur": self.medianBlurValue,
                      "equalize_image": self.equalizeImage,
                      "quantization": self.quantization}

        self.train(self.trainingImagesPath.text(),parameters)
        self.close()

    def set_training_images_folder_path(self,file_path):
        self.trainingImagesPath.setText(file_path)

    def set_brightness_value(self,value):
        self.brightnessLabel.setText("Brightness: " + str(value))
        self.brightnessValue = value

    def change_quantization(self,value):
        self.quantizationLabel.setText("Quantization: " + str(value))
        self.quantization = value

    def set_contrast_value(self,value):
        self.contrastLabel.setText("Contrast: " + str(value))
        self.contrastValue = value

    def set_median_blur_value(self,value):
        if value % 2 != 1:
            return
        self.medianBlurLabel.setText("Median Blur " + str(value))
        self.medianBlurValue = value

    def set_equalization(self): 
        self.equalizeImage = self.equalizationCheckbox.isChecked

    def search_training_folder(self):
        file = QtWidgets.QFileDialog.getExistingDirectory(self, "Open training images folder",
                                                OsUtils.get_user_home())

        if not file:
            return

        if not np.array_equal(OsUtils.folders_in(file),['4','3','1','2']):
            msg = QtWidgets.QMessageBox()

            msg.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            msg.setText("Error on loading training images folder!")
            msg.setInformativeText("Please choose a folder which has folders named \'1\',\'2\',\'3\',\'4\'")
            msg.setWindowTitle("Error!")

            msg.exec()
            return

        self.trainingImagesPath.setText(file)
