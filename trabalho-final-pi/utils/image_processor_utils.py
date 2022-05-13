import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

def sharpen(image, parameters=0):
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    return cv.filter2D(image, -1, kernel)

def gaussian_blur(image, ksize=(15, 15), border=cv.BORDER_DEFAULT):
    return cv.GaussianBlur(image, ksize, border)


def equalization(image):
    R, G, B = cv.split(image)

    output1_R = cv.equalizeHist(R)
    output1_G = cv.equalizeHist(G)
    output1_B = cv.equalizeHist(B)
    return cv.merge((output1_R, output1_G, output1_B))


def select_image_area(image, xi, yi, xf, yf):
    pass


if __name__ == '__main__':

	original = cv.imread("../assets/imgs/imagem1.jpg")


cv.waitKey(0)

