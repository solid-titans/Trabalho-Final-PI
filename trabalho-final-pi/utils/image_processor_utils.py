import numpy as np
import cv2 as cv
from sklearn.cluster import MiniBatchKMeans

MAX_PIXEL_VALUE = 255

SHARPEN_3X3 = [[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]
SHARPEN_5X5 = [[0, 0, -1, 0, 0], [0, -1, -2, -1, 0],
    [-1, -2, 16, -2, -1], [0, -1, -2, -1, 0], [0, 0, -1, 0, 0]]


def sharpen(image, stype=SHARPEN_3X3):
    kernel = np.array(stype)
    return cv.filter2D(image, -1, kernel)


def gaussian_blur(image, ksize=(15, 15), border=cv.BORDER_DEFAULT):
    return cv.GaussianBlur(image, ksize, border)

def median_blur(image,ksize=1):
    return cv.medianBlur(image,ksize)

def convert_to_grayscale(image):
    return cv.cvtColor(image,cv.COLOR_BGR2GRAY)

def equalization(image):
    R, G, B = cv.split(image)

    output1_R = cv.equalizeHist(R)
    output1_G = cv.equalizeHist(G)
    output1_B = cv.equalizeHist(B)
    return cv.merge((output1_R, output1_G, output1_B))

def select_image_area(image, xi, yi, xf, yf):
    return image[xi:xf, yi:yf]

def quantization(image, k):

    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    gray = gray.astype(np.float32)/255

    # quantize and convert back to range 0 to 255 as 8-bits
    result = 255*np.floor(gray*k+0.5)/k
    result = result.clip(0,31).astype(np.uint8)

    return result

def brightness_contrast(img, brightness=255,
			contrast=127):

    brightness = int((brightness - 0) * (255 - (-255)) / (510 - 0) + (-255))

    contrast = int((contrast - 0) * (127 - (-127)) / (254 - 0) + (-127))

    cal = 0

    if brightness != 0:

        if brightness > 0:

            shadow = brightness
            max = 255

        else:

            shadow = 0
            max = 255 + brightness

        al_pha = (max - shadow) / 255
        ga_mma = shadow

        cal = cv.addWeighted(img, al_pha,img, 0, ga_mma)

    else:
        cal = img

        if contrast != 0:

            Alpha = float(131 * (contrast + 127)) / (127 * (131 - contrast))
            Gamma = 127 * (1 - Alpha)

            # The function addWeighted calculates
            # the weighted sum of two arrays
            cal = cv.addWeighted(cal, Alpha,cal, 0, Gamma)

    return cal

"""
if __name__ == '__main__':

    original = cv.imread("../assets/imgs/imagem1.jpg")
    cv.imshow('Original', original)  

    simag = brightness_contrast(original,brightness=250)
    cv.imshow('brightness_contrast', simag)  
"""
if __name__ == '__main__':
    image = cv.imread('../assets/imgs/imagem1.jpg')

    image = quantization(image,32)

    cv.imshow('image',image)

    cv.waitKey(0) 

