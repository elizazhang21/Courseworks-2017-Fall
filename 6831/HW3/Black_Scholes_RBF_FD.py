# Black_Scholes_RBF_FD.py

import numpy as np
from scipy.stats import norm
from numpy.linalg import inv
from Radial_Basis_Function import RBF_G, RBF_MQ


def Call_Payoff(stock_price, strike_price):
    return max(stock_price - strike_price, 0)


def Put_Payoff(stock_price, strike_price):
    return max(strike_price - stock_price, 0)


def BS_Call(t, T, S, K, r, delta, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol * vol) * (T - t)) / vol / np.sqrt(T - t)
    d2 = d1 - vol * np.sqrt(T - t)
    call_price = S * norm.cdf(d1) * np.exp(-delta * (T - t)) - K * np.exp(-r * (T - t)) * norm.cdf(d2)
    return call_price


def BS_Put(t, T, S, K, r, delta, vol):
    d1 = (np.log(S / K) + (r + 0.5 * vol * vol) * (T - t)) / vol / np.sqrt(T - t)
    d2 = d1 - vol * np.sqrt(T - t)
    put_price = K * np.exp(-r * (T - t)) * norm.cdf(-d2) - S * norm.cdf(-d1) * np.exp(-delta * (T - t))
    return put_price


def Discount(i, r, delta, dt):
    return np.exp(-(r - delta) * i * dt)


def Black_Scholes_RBF_FD(s_max, s_min, M, N, T, t, r, delta, sigma, RBF, payoff_function):

    tau = T - t
    epsilon = 1
    dt = tau / (N - 1)
    strike_price = 0.5 * (s_max + s_min)
    # choose collocation points
    x = np.linspace(np.log(s_min), np.log(s_max), M)
    time = np.linspace(0, T, N)
    stock_price = np.exp(x)

    # calculate the weighting matrix W
    W_initial = np.zeros((M - 2, 3))
    W_final = np.zeros((M - 2, M - 2))
    I = np.identity(M - 2)
    s = x[0:3]
    phi = np.array(RBF(epsilon, s, s))
    # use the nearest neighbor conditions
    W_i = inv(np.round(phi[0], 8)) .dot((r - sigma ** 2 / 2) * phi[1][1] + sigma ** 2 / 2 * phi[2][1] - r * phi[0][1])
    W_initial = W_i

    # generate the final weighting matrix
    W_final[0][0] = W_initial[1]
    W_final[0][1] = W_initial[2]
    W_final[M - 3][M - 4] = W_initial[0]
    W_final[M - 3][M - 3] = W_initial[1]
    for i in range(1, M - 3):
        W_final[i][i - 1] = W_initial[0]
        W_final[i][i] = W_initial[1]
        W_final[i][i + 1] = W_initial[2]

    # boundary condition
    addition = np.zeros(M - 2)
    v = np.zeros((M - 2, N))
    for i in range(M - 2):
        v[i][0] = payoff_function(stock_price[i + 1], strike_price)
    # calculate the initial value v(x, t1)
    for i in range(1, N):
        addition[0] = W_initial[0] * (payoff_function(s_min, Discount(i - 1, r, delta, dt) * strike_price) + payoff_function(s_min , Discount(i, r, delta, dt) * strike_price)) * dt / 2
        addition[M - 3] = W_initial[2] * (payoff_function(s_max, Discount(i - 1, r, delta, dt) * strike_price) + payoff_function(s_max , Discount(i, r, delta, dt) * strike_price)) * dt / 2
        v[:, i] = inv(np.round(I - dt / 2 * W_final, 8)).dot((I + dt / 2 * W_final) @ v[:, i - 1] + addition)
    return v.T
