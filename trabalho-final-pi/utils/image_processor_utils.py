# This Python file uses the following encoding: utf-8
import cv2 as cv

def sharpen(image,parameters=0):
    pass

def brightness_and_contrast(image,parameters):
    pass


def gaussian_blur(image,ksize =(3,3),border = cv.BORDER_DEFAULT):
    return cv.GaussianBlur(image,ksize,border)

def equalization(image,parameters):
    pass

def select_image_area(image,xi,yi,xf,yf):
    pass


if __name__ == "__main__":
    img = cv.imread('../assets/imgs/imagem1.jpg')
    cv.imshow('Original', img)
    cv.imshow('saida 3x3',gaussian_blur(img,ksize=(7,7)))
    cv.imshow('saida 7x7',gaussian_blur(img))
    cv.imshow('saida 15x15',gaussian_blur(img,ksize=(15,15)))
    cv.waitKey(0)