# Radial_Basis_Function.py
import numpy as np
from scipy.stats import norm


def RBF_G(epsilon, x, xi):

    # Gaussian: e^(-(epsilon*r)**2)
    # L_G = Gaussian RBF
    # L_x_G = first order derivatives of Gaussian Quandric RBF
    # L_xx_G = second order derivatives of Gaussian Quadric RBF

    N = len(x)
    L_G = np.zeros((N, N))
    L_x_G = np.zeros((N, N))
    L_xx_G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            r = x[i] - xi[j]
            L_G[i][j] = np.exp(-(epsilon * r ** 2))
            L_x_G[i][j] = -2 * epsilon ** 2 * r * np.exp(-((epsilon * r) ** 2))
            L_xx_G[i][j] = 4 * epsilon ** 4 * r ** 2 * np.exp(-((epsilon * r) ** 2)) - 2 * epsilon ** 2 * np.exp(-((epsilon * r) ** 2))

    return L_G, L_x_G, L_xx_G


def RBF_MQ(epsilon, x, xi):

    # Multi_Quadric: sqrt(1+(e(x-xi))**2)
    # L_MQ = Multi_Quadric RBF
    # L_x_MQ = first order derivatives of Multi-Quadric RBF
    # L_xx_MQ = second order derivatives of Multi-Quadric RBF

    N = len(x)
    L_MQ = np.zeros((N, N))
    L_x_MQ = np.zeros((N, N))
    L_xx_MQ = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            r = x[i] - xi[j]
            L_MQ[i][j] = np.sqrt(1 + (epsilon * r) ** 2)
            L_x_MQ[i][j] = (epsilon * r) / np.sqrt((epsilon * r) ** 2 + 1)
            L_xx_MQ[i][j] = epsilon / np.sqrt((epsilon * r) ** 2 + 1) - (epsilon * r) ** 2 / (np.sqrt((epsilon * r) ** 2 + 1)) ** 3

    return L_MQ, L_x_MQ, L_xx_MQ
