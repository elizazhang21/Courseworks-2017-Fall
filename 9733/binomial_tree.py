import scipy
import numpy as np
import math



# T = expiration time 4 years
# S = stock price 581
# K = strike price 578
# q = dividend yield 0
# n = height of the binomial tree 4
# r = interest rate = 0.12

def binomial_tree(n, S, up, down):
    c = np.zeros((n+1, n+1))
    c[0][0] = S
    for i in range(n):
        for j in range(i+1):
            c[i+1][j+1] = up * c[i][j]
        c[i+1][0] = down * c[i][0]
    return c


def call_payoff(T,steps,S, K, r, up, down, q):
	n = int(T/steps)
	p_up = (math.exp(r*2)-down)/(up - down)
	p_down = 1 - p_up
	c = binomial_tree(n, S, up, down)
	return c


print(call_payoff(4, 2, 581, 578, 0.12, 1.3, 0.8, 4))

