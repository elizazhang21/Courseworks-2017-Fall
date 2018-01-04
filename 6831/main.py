# main.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from MarkowitzPortfolioOptimization import *


def initial_portfolio(data):
    cov = np.cov(data)
    exp_ret = np.zeros(len(data))

    dev = np.zeros(len(data))
    for i in range(len(data)):
        exp_ret[i] = np.mean(data[i])
        dev[i] = np.std(data[i])
    return exp_ret, cov, dev


start = '1/1/2008'
end = '12/1/2017'

SPY_ret = pd.read_csv('SPY.csv')['Return'][1:].tolist()
BND_ret = pd.read_csv('BND.csv')['Return'][1:].tolist()
GLD_ret = pd.read_csv('GLD.csv')['Return'][1:].tolist()
GOOG_ret = pd.read_csv('GOOG.csv')['Return'][1:].tolist()
JPM_ret = pd.read_csv('JPM.csv')['Return'][1:].tolist()
MS_ret = pd.read_csv('MS.csv')['Return'][1:].tolist()
AAPL_ret = pd.read_csv('AAPL.csv')['Return'][1:].tolist()

data = [SPY_ret, BND_ret, GLD_ret, GOOG_ret, MS_ret]
n = len(data)
mu, cov, _ = initial_portfolio(data)


# =======================================================================================================
# =========================        Markowitz Portfolio Optimization Mean        =========================
# =======================================================================================================
# x-axis is Risk(Standard Deviation), y-axis is Expected Return.
R_tar = np.linspace(0.004, 0.014, 30)
weights = []
expected_return = []
std = []
rtar = []
for r in R_tar:
    _, ret, sigma = Markowitz_Portfolio_Optimization_Mean(n, mu, cov, r)
    expected_return.append(r)
    std.append(sigma) 
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(std, expected_return, '-', color='blue', markersize=2)
plt.xlabel('Risk(Standard Deviation)')
plt.ylabel('Expected Return')
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(8)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(8)
plt.title('Markowitz Portfolio Optimization Mean', fontsize=10)
plt.show()

# ===========================================================================================================
# =========================        Markowitz Portfolio Optimization Variance        =========================
# ===========================================================================================================
sigma_tar = np.linspace(0.001, 0.08, 30)
expected_return = []
std = []
for sigma in sigma_tar:
    _, ret, risk = Markowitz_Portfolio_Optimization_Variance(n, mu, cov, sigma)
    expected_return.append(ret)
    std.append(risk)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(std, expected_return, '-', color='blue', markersize=2)
plt.xlabel('Risk(Standard Deviation)')
plt.ylabel('Expected Return')
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(8)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(8)
plt.title('Markowitz Portfolio Optimization Variance', fontsize=10)
plt.show()


# ===========================================================================================================
# =========================        Markowitz Portfolio Optimization Mean Variance        =========================
# ===========================================================================================================
data = [SPY_ret, BND_ret, GLD_ret, JPM_ret, AAPL_ret, GOOG_ret, MS_ret]   # APPL, JPM
n = len(data)
mu, cov, _ = initial_portfolio(data)
delta_tar = np.linspace(0.1, 1, 10)
for delta in delta_tar:
    w, ret, risk = Markowitz_Portfolio_Optimization_Mean_Variance(n, mu, cov, delta)
    print('Risk Aversion is ' + str(delta))
    print(w)
    print(ret)
    print(risk)
