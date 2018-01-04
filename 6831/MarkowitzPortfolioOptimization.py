# MarkowitzPortfolioOptimization.py

import numpy as np
from scipy import optimize
from scipy.optimize import minimize

# outputs include the return and standard deviation of the optimal portfolio and the weight of each asset in the optimal portfolio.
# SPY, BND, GLD and other assets such as AAPL and Alphabete
# time period is from 2008-01-01 to 2017-11-30
# the return vector mu is calculated monthly.
# Sigma is the covariance matrix of the monthly returns mu_i
# target return R and target standard deviation sigma and risk-aversion constant delta is chosen by myself.


def Markowitz_Portfolio_Optimization_Mean(n, mu, cov, R_tar):
    # minimize 0.5 * x.T * cov * x
    # subject to mu.T * x >= R
    # sum(x) = 1
    # x >= 0
    fun = lambda x: x.T.dot(cov).dot(x) / 2
    cons = ({'type': 'ineq', 'fun': lambda x: mu.T.dot(x) - R_tar},
            {'type': 'ineq', 'fun': lambda x: x},
            {'type': 'eq', 'fun': lambda x: np.ones(n).T.dot(x) - 1}
            )
    res = minimize(fun, 1 / n * np.ones(n), constraints=cons)
    return res.x, mu.T.dot(res.x), (res.fun * 2) ** 0.5


def Markowitz_Portfolio_Optimization_Variance(n, mu, cov, sigma_tar):
    # maximize mu.T.dot(mu)
    # subject to x.T * cov * x <= simga^2
    fun = lambda x: -mu.T.dot(x)
    cons = ({'type': 'ineq', 'fun': lambda x: sigma_tar ** 2 - x.T.dot(cov).dot(x)},
            {'type': 'ineq', 'fun': lambda x: x},
            {'type': 'eq', 'fun': lambda x: np.ones(n).T.dot(x) - 1}
            )
    res = minimize(fun, 1 / n * np.ones(n), constraints=cons)
    return res.x, -res.fun, (res.x.T.dot(cov).dot(res.x)) ** 0.5


def Markowitz_Portfolio_Optimization_Mean_Variance(n, mu, cov, delta):
    # maximize mu.T.dot(x) - delta / 2 * x.T.dot(cov).dot(x)
    fun = lambda x: -mu.T.dot(x) + delta / 2 * x.T.dot(cov).dot(x)
    cons = ({'type': 'ineq', 'fun': lambda x: x},
            {'type': 'eq', 'fun': lambda x: np.ones(n).T.dot(x) - 1}
            )
    res = minimize(fun, 1 / n * np.ones(n), constraints=cons)
    return res.x, mu.T.dot(res.x), (res.x.T.dot(cov).dot(res.x)) ** 0.5
