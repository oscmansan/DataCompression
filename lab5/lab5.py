#!/usr/bin/python3.4
from itertools import product

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np
from scipy.misc import face, imresize

jpeg_quantiz_matrix = np.array([[16, 11, 10, 16, 24, 40, 51, 61],
                                [12, 12, 14, 19, 26, 58, 60, 55],
                                [14, 13, 16, 24, 40, 57, 69, 56],
                                [14, 17, 22, 29, 51, 87, 80, 62],
                                [18, 22, 37, 56, 68, 109, 103, 77],
                                [24, 35, 55, 64, 81, 104, 113, 92],
                                [49, 64, 78, 87, 103, 121, 120, 101],
                                [72, 92, 95, 98, 112, 100, 103, 99]])


def lossy_transform(img, T, Q):
    height, width, depth = img.shape
    # split into 8 x 8 pixels blocks
    img_blocks = [(i, j) for (i, j) in product(range(0, height, 8), range(0, width, 8))]
    for i, j in img_blocks:
        block = img[i:i + 8, j:j + 8, :]
        print(i, j)
        plt.imshow(block)
        plt.draw()
        plt.pause(0.000001)
    plt.show()


I = np.identity(8)
T = cv.dct(I)
Q = jpeg_quantiz_matrix
img = face()
img = imresize(img, (512, 512))
plt.imshow(img)
plt.show()
lossy_transform(img, T, Q)
