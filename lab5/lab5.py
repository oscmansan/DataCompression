#!/usr/bin/python3.4
from itertools import product
from math import sqrt, cos, pi

import numpy as np
from matplotlib.pyplot import figure, imshow, show, cm
from scipy.misc import imread

Q_JPEG_standard = np.array([
    [16, 11, 10, 16, 24, 40, 51, 61],
    [12, 12, 14, 19, 26, 58, 60, 55],
    [14, 13, 16, 24, 40, 57, 69, 56],
    [14, 17, 22, 29, 51, 87, 80, 62],
    [18, 22, 37, 56, 68, 109, 103, 77],
    [24, 35, 55, 64, 81, 104, 113, 92],
    [49, 64, 78, 87, 103, 121, 120, 101],
    [72, 92, 95, 98, 112, 100, 103, 99]])


def T_DCT_matrix(N=8):
    mat = np.zeros((N, N))
    for j in range(N):
        mat[0, j] = sqrt(1 / N)
        for i in range(1, N):
            mat[i, j] = cos(i * (j + 0.5) * pi / N) * sqrt(2 / N)
    return mat


def encode(X, T, Q):
    Y = T.dot(X).dot(np.transpose(T))
    return np.rint(Y / Q)


def decode(Y, T, Q):
    X = Y * Q
    return np.rint(np.linalg.inv(T).dot(X).dot(np.linalg.inv(np.transpose(T))))


def lossy_transform(img, T, Q):
    # TODO: refactor to accept variable N
    img = np.atleast_3d(img)
    height, width, depth = img.shape
    newimg = np.empty((height, width, depth), dtype=np.uint8)

    # split into 8 x 8 pixels blocks
    img_blocks = [(i, j) for (i, j) in product(range(0, height, 8), range(0, width, 8))]
    for i, j in img_blocks:
        for k in range(depth):
            B = img[i:i + 8, j:j + 8, k]
            shape = B.shape
            if shape != (8, 8):
                aux = np.zeros((8, 8))
                aux[:B.shape[0], :B.shape[1]] = B
                B = aux
            Benc = encode(B, T, Q)
            Bdec = decode(Benc, T, Q)
            Bdec = np.clip(Bdec, np.iinfo(np.uint8).min, np.iinfo(np.uint8).max)
            newimg[i:i + 8, j:j + 8, k] = Bdec[:shape[0], :shape[1]]

    return newimg.squeeze()


T = T_DCT_matrix()
Q = Q_JPEG_standard

img = imread('../data/ILSVRC2012_val_00014184.JPEG')
newimg = lossy_transform(img, T, Q)
imgerr = np.abs(img.astype(np.int8) - newimg.astype(np.int8)).astype(np.uint8)

figure('original')
imshow(img)
figure('compressed')
imshow(newimg)
figure('error')
imshow(imgerr)
show()

'''B = np.array([[142,144,130,92,84,77,72,85],
              [138,150,138,115,105,119,125,130],
              [136,142,139,135,135,130,133,137],
              [139,142,144,141,140,143,141,138],
              [139,138,141,138,142,146,146,147],
              [142,141,142,150,147,149,149,151],
              [142,143,149,151,148,152,151,153],
              [145,148,151,152,151,154,148,157]])
Benc = encode(B,T,Q)
Bdec = decode(Benc,T,Q)'''
