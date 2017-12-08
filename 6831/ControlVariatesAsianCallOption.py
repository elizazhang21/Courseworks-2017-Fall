# ControlVariatesAsianCallOption.py
import numpy as np
from scipy.stats import gmean, norm
from MonteCarloForStockPrice import Jump_Diffusion_Process_At_Fixed_Dates


def Arithmetic_Average_Price_Asian_Call(S_0, T, n, r, sigma, d, Lambda, a, b, K):
    price = 0
    # set the number of paths
    for i in range(10000):
        PriceList = Jump_Diffusion_Process_At_Fixed_Dates(S_0, T, n, r, sigma, d, Lambda, a, b)
        # calculate the arithmetic average price of each path
        S_avg = np.mean(PriceList)
        # add up to a total number
        price += np.max(S_avg - K, 0)
    # return the expected value
    return np.exp(-r * T) * price / 10000

# print(Arithmetic_Average_Price_Asian_Call(20, 1, 252, 0.05, 0.2, 0.01, 100, 0, 0, 10))


def Geometric_Average_Price_Asian_Call(S_0, T, n, r, sigma, d, Lambda, a, b, K):
    price = 0
    # set the number of paths
    for i in range(10000):
        PriceList = Jump_Diffusion_Process_At_Fixed_Dates(S_0, T, n, r, sigma, d, Lambda, a, b)
        # calculate the geometric average price of each path
        S_avg = gmean(PriceList)
        # add up to a total number
        price += np.max(S_avg - K, 0)
    # return the expected value
    return np.exp(-r * T) * price / 10000
# print(Geometric_Average_Price_Asian_Call(20, 1, 252, 0.05, 0.2, 0.01, 100, 0, 0, 10))


def BS_Geometric_Average_Price_Asian_Call(S, K, r, sigma, delta, T):
    b = 0.5 * (r + delta + sigma ** 2 / 6)
    sigma = sigma / (3 ** 0.5)
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2 - b) * T) / sigma / np.sqrt(T)
    d2 = d1 - sigma * T ** 0.5
    price = S * np.exp(-b * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return price
# print(BS_Geometric_Average_Price_Asian_Call(20, 10, 0.05, 0.2, 0.01, 1))


def Control_Variates_Arithmetic_Average_Asian_Call(S, K, r, sigma, d, t, T, step, round):
    # Yi represents Arithmetic Average Price Asian Call Price
    # Xi represents Control variates, which is the price of geometric average price Asian call
    # EX represents BS Geometric Average Price Asian Call

    # simulate payoffs of arithmetic Asian Call using control variance
    # round is the number of simulation times. User may get price be apply

    # St should be a number here so function only compute price of one
    # initial stock price per time

    EX = BS_Geometric_Average_Price_Asian_Call(S, K, r, sigma, d, T - t)
    Y = np.zeros(round)
    X = np.zeros(round)
    discount = np.exp(-r * (T - t))

    for k in range(2, round + 1):
        PriceList = Jump_Diffusion_Process_At_Fixed_Dates(S, T, k, r, sigma, d, 100, 0, 0)
        S_amean = np.mean(PriceList)
        S_gmean = gmean(PriceList)
        Y[k - 1] = discount * np.max(S_amean - K, 0)
        X[k - 1] = discount * np.max(S_gmean - K, 0)

    b = np.cov(X, Y)
    b = b[1][0] / np.var(X)
    Y = Y - b * (X - EX)
    return np.mean(Y)

# print(Control_Variates_Arithmetic_Average_Asian_Call(20, 10, 0.05, 0.2, 0.01, 0, 1, 252, 1000))


'''
Sample results:
9.89989328178
9.82989284354
9.83202776473
9.89805459141
[Finished in 36.4s]
'''