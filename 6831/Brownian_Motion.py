# Brownian_Motion.py

import numpy as np
import scipy

def BM(S, r, sigma, T, step):

	# generate geometric Brownian process:
	# dS = rSdt + sigma*dW
	# a pair of paths is generated each time, where one is antithetic

	S = np.zeros((2, T * step + 1))
	dt = 1 / step

	S[0][0] = S * t
	S[1][0] = S * t