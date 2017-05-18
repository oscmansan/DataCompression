# !/usr/bin/python3
from itertools import product
from math import sqrt, cos, pi

import matplotlib.pyplot as plt
import numpy as np


def T_DCT_matrix(N=8):
    mat = np.zeros((N, N))
    for j in range(N):
        mat[0, j] = sqrt(1 / N)
        for i in range(1, N):
            mat[i, j] = cos(i * (j + 0.5) * pi / N) * sqrt(2 / N)
    return mat


N = 8
T = T_DCT_matrix(N)

plt.matshow(T)

fig = plt.figure()
for i, j in product(range(0, N), range(0, N)):
    B = np.dot(T[i][np.newaxis].T, T[j][np.newaxis])
    ax = fig.add_subplot(N, N, i * N + j + 1)
    ax.matshow(B)
    ax.xaxis.set_visible(False)
    ax.yaxis.set_visible(False)
plt.show()
