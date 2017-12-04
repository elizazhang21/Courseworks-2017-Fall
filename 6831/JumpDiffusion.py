# JumpDiffusion.py

import numpy as np
from numpy import exp, sqrt, log
from numpy.random import randn, poisson
import scipy


def JumpDiffusion(St, mu, sigma, T, step, Lambda, a, b):
    # similate Jump_Diffusition Process using Algorism 5.6
    # mu and sigma are parameters of normal GBM, lambda is parameter of
    # poisson distribution, a and b are parameters of random variable Y

    price = np.zeros(step * T + 1)
    price[1] = St

    dt = T / step
    for i in range(2, step * T + 1):
        N = poisson(Lambda * dt)
        if N <= 0:
            M = 0
        else:
            M = a * N + b * sqrt(N) * randn()

        price[i] = price[i - 1] + (mu - 0.5 * sigma ** 2) * dt + sigma * sqrt(dt) * randn() + M
    return None

