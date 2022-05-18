from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QDialog
from PyQt6.QtGui import QImage
import cv2, imutils

import utils.image_processor_utils as ImageProcessingUtils

class MedianBlurEditor(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.loadUi()

        self.filename = None 
        self.tempImage = None 
        self.brightness_value_now = 0
        self.gaussian_value_now = 1

        self.save_image = None

    def set_image_saving_function(self,function):
        self.save_image = function

    def loadUi(self):
        self.setObjectName("MainWindow")
        self.resize(750, 600)
        self.setFixedSize(750, 600)

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

        self.gaussianSlider = QtWidgets.QSlider(self.centralwidget)
        self.gaussianSlider.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.gaussianSlider.setObjectName("gaussianSlider")
        self.gaussianSlider.setMinimum(1)
        self.gaussianSlider.setMaximum(50)
        self.gaussianSlider.setValue(1)
        self.gaussianSlider.setTickInterval(3)
        self.gaussianSlider.setSingleStep(3)

        self.horizontalLayout.addWidget(self.gaussianSlider)

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

        self.gaussianSlider.valueChanged['int'].connect(self.set_gaussian_value)
        self.cancelButton.clicked.connect(self.cancelOperation)
        self.saveButton.clicked.connect(self.savePhoto)
        QtCore.QMetaObject.connectSlotsByName(self)

        self.setWindowTitle("Gaussian Blur")
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
        image = imutils.resize(image,width=500)
        frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image = QImage(frame, frame.shape[1],frame.shape[0],frame.strides[0],QImage.Format.Format_RGB888)
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def set_gaussian_value(self,value):
        if value % 2 != 1:
            return
        self.gaussian_value_now = value
        #print('Contrast: ',self.gaussian_value_now)
        self.update()

    def changeGaussian(self,img,value):
        img = ImageProcessingUtils.median_blur(img,value)
        return img

    def update(self):
        img = self.changeGaussian(self.image,self.gaussian_value_now)
        self.setPhoto(img)

    def savePhoto(self):
        self.save_image(self.tempImage)
        self.close()


if __name__ == "__main__":
        import sys
        app = QtWidgets.QApplication(sys.argv)
        self = QtWidgets.Qself()
        ui = GaussianEditor()
        ui.setupUi(self)
        self.show()
        sys.exit(app.exec())
