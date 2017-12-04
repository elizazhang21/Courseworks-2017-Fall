# OptionValuer.py

import numpy as np
import scipy
from scipy.stats import norm
from scipy.linalg import inv
from scipy import stats
from sklearn.linear_model import LinearRegression


def Call_Payoff(stock_price, strike_price):
    return np.max(stock_price - strike_price, 0)


def Put_Payoff(stock_price, strike_price):
    return max(strike_price - stock_price, 0)


def BS_Call(t, T, S, K, r, delta, vol):
    maturity = T - t
    d1 = (np.log(S / K) + (r + 0.5 * vol * vol) * maturity) / vol / np.sqrt(maturity)
    d2 = d1 - vol * np.sqrt(maturity)
    call_price = S * norm.cdf(d1) * np.exp(-delta * maturity) - K * np.exp(-r * maturity) * norm.cdf(d2)
    return call_price


def BS_Put(t, T, S, K, r, delta, vol):
    maturity = T - t
    d1 = (np.log(S / K) + (r + 0.5 * vol * vol) * maturity) / vol / np.sqrt(maturity)
    d2 = d1 - vol * np.sqrt(maturity)
    put_price = K * np.exp(-r * maturity) * norm.cdf(-d2) - S * norm.cdf(-d1) * np.exp(-delta * maturity)
    return put_price


def OptionValuer(paths, payoff, r, times, steps):
    # paths is a N-step matrix of simulated asset price
    # payoff is a function compute exercise value at certain t and asset price
    # (early exercise) payoff of option
    # r is risk free rate used to compute discount factor
    # times is exercise times every year
    # steps are number of steps between exercise time
    # discount is discount factor between each steps

    N = len(paths)   # number of simulated paths (numbers of arrays)
    K = len(paths[1]) // steps   # number of total time steps (numbers of columns)
    discount = np.exp(-r / times)

    # declare variables for computing
    Y = np.zeros(N)
    P = np.zeros(N)
    X = np.zeros((N, 3))

    # initialize Y_t+1 with option value at maturity
    for i in range(N):
        Y[i] = payoff(paths[i], K * steps)

    for i in range(K - 1, 1, -1):
        # prepare early exercise value vector
        for j in range(N):
            P[j] = payoff(paths[j], i * steps)

        # discount T_t+1
        Y = Y * discount

        # prepare lagurre polinomial values of asset price
        count = 0
        for j in range(N):
            if P[j] > 0:
                count = count + 1
                x = paths[j][i * steps]
                X[j][0] = (1 - x)
                X[j][1] = (1 - 2 * x + 0.5 * x ** 2)
                X[j][2] = (1 - 3 * x + 1.5 * x ** 2 - x ** 3 / 6)

        if count >= 0.01 * N:
            X_train = []
            Y_train = []
            for i in range(N):
                if P[i] > 0:
                    X_train.append(X[i, :])
                    Y_train.append(Y[i])
            print(X_train)
            print(Y_train)
            # solve lsm
            model = LinearRegression()
            model.fit(X_train, Y_train)
            X_test = X_train
            Y_test = Y_train
            predictions = model.predict(X_test)
            for i, prediction in enumerate(predictions):
                print('Predicted: ', prediction, 'Target: ', Y_test[i])
            # print('R-squared: ', model.score(X_test, Y_test))

        else:
            # too few paths have positive early exercise value, skip fit
            for j in range(N):
                if P[j] > 0:
                    Y[j] = max(P[j], Y[j])
    print(Y)
    return Y

paths = np.array([[100, 200, 300, 200, 100, 200, 100, 300, 200, 200], [100, 200, 100, 200, 100, 200, 100, 300, 200, 100]])
OptionValuer(paths, Call_Payoff, 0.1, 10, 2)
