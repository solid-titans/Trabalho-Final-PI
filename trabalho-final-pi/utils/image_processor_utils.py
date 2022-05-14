import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt

SHARPEN_3X3 = [[-1,-1,-1], [-1,9,-1], [-1,-1,-1]]
SHARPEN_5X5 = [[0,0,-1,0,0],[0,-1,-2,-1,0],[-1,-2,16,-2,-1],[0,-1,-2,-1,0],[0,0,-1,0,0]]
def sharpen(image, stype=SHARPEN_3X3):
    kernel = np.array(stype)
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
    cv.imshow('Original', original)  

    sh3x3 = sharpen(original)
    cv.imshow('3x3', sh3x3) 

    sh5x5 = sharpen(original,stype=SHARPEN_5X5)
    cv.imshow('5x5', sh5x5)   

cv.waitKey(0)

