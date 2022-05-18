from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QImage
import cv2, imutils

import utils.image_processor_utils as ImageProcessingUtils

class BrightnessContrastEditor(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadUi()

        self.filename = None 
        self.tempImage = None 
        self.brightness_value_now = 0
        self.constrast_value_now = 0.5

        self.save_image = None

    def set_image_saving_function(self,function):
        self.save_image = function

    def loadUi(self):
        self.setObjectName("MainWindow")
        self.resize(750, 510)
        self.setFixedSize(750, 510)

        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")

        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.brightnessSlider = QtWidgets.QSlider(self.centralwidget)
        self.brightnessSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.brightnessSlider.setObjectName("brightnessSlider")
        self.brightnessSlider.setMinimum(1)
        self.brightnessSlider.setMaximum(50)
        self.brightnessSlider.setValue(1)

        self.horizontalLayout.addWidget(self.brightnessSlider)

        self.constrastSlider = QtWidgets.QSlider(self.centralwidget)
        self.constrastSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.constrastSlider.setObjectName("constrastSlider")
        self.constrastSlider.setMinimum(1)
        self.constrastSlider.setMaximum(50)
        self.constrastSlider.setValue(1)

        self.horizontalLayout.addWidget(self.constrastSlider)

        self.horizontalLayout_3.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.horizontalLayout_3, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.cancelButton = QtWidgets.QPushButton(self.centralwidget)
        self.cancelButton.setObjectName("cancelButton")
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.saveButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveButton.setObjectName("saveButton")
        self.horizontalLayout_2.addWidget(self.saveButton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 1, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)

        self.brightnessSlider.valueChanged['int'].connect(self.set_brightness_value)
        self.constrastSlider.valueChanged['int'].connect(self.set_contrast_value)
        self.cancelButton.clicked.connect(self.cancelOperation)
        self.saveButton.clicked.connect(self.savePhoto)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Brightness and Contrast")
        self.cancelButton.setText("Cancel")
        self.saveButton.setText("Save")

    def cancelOperation(self):
        self.close()

    def loadImage(self,file_path):
        self.filename = file_path
        self.image = cv2.imread(self.filename)

        self.update()

    def setPhoto(self,image):
        self.tempImage = image
        image = imutils.resize(image,width=640)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def set_brightness_value(self,value):
        self.brightness_value_now = value
        #print('Brightness: ',value)
        self.update()

    def set_contrast_value(self,value):
        self.constrast_value_now = max(value/10,0.5)
        #print('Contrast: ',self.constrast_value_now)
        self.update()

    def changeBrightness(self,img,value):
        img = ImageProcessingUtils.brightness_and_contrast(img,self.constrast_value_now,value)
        return img

    def changeContrast(self,img,value):
        img = ImageProcessingUtils.brightness_and_contrast(img,value,self.brightness_value_now)
        return img

    def update(self):
        img = self.changeBrightness(self.image,self.brightness_value_now)
        img = self.changeContrast(img,self.constrast_value_now)
        self.setPhoto(img)

    def savePhoto(self):
        self.save_image(self.tempImage)
        self.close()


if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        self = QtWidgets.Qself()
        ui = BrightnessContrastEditor()
        ui.setupUi(self)
        self.show()
        sys.exit(app.exec())