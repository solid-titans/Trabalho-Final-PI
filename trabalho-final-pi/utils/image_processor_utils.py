# This Python file uses the following encoding: utf-8
import cv2 as cv

def sharpen(image,parameters=0):
    pass

def brightness_and_contrast(image,parameters):
    pass


def gaussian_blur(image,ksize =(3,3),border = cv.BORDER_DEFAULT):
    return cv.GaussianBlur(image,ksize,border)

def equalization(image):
    R, G, B = cv.split(img)

    output1_R = cv.equalizeHist(R)
    output1_G = cv.equalizeHist(G)
    output1_B = cv.equalizeHist(B)
    return cv.merge((output1_R, output1_G, output1_B))

def select_image_area(image,xi,yi,xf,yf):
    pass


if __name__ == "__main__":
    img = cv.imread('../assets/imgs/imagem1.jpg')
    cv.imshow('Original', img)

    cv.imshow('Equalization', equalization(img))

    cv.waitKey(0)