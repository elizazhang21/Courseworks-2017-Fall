# __author__ = 'Eli Zhang'
# c = Se^{(b-r)T}N(d_1) - Ke^{-rT}N(d_2)
# p = Ke^{-rT}N(-d_2) - Se^{(b-r)T}N(-d_1)
# d_1 = [ln(S/X) + (b + sigma^2)T]/(sigma \time \sqrt{T})
# d_2 = d_1 - sigma \times sqrt{T}

from math import log, sqrt, exp
import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt


def Black_Scholes(type, r, maturity, spot, strike, vol):
    d1 = (log(spot / strike) + (r + 0.5 * vol * vol) *
          maturity) / vol / sqrt(maturity)
    d2 = d1 - vol * sqrt(maturity)

    if type == 'Call':
        price = spot * norm.cdf(d1) - strike * \
            exp(-r * maturity) * norm.cdf(d2)

    elif type == 'Put':
        price = strike * exp(-r * maturity) * norm.cdf(-d2) - \
            spot * norm.cdf(-d1)

    else:
        print('Error')

    return price


def price_plot(type):
    price = []
    spot = range(30, 171, 1)
    for s in range(30, 171, 1):
        price.append(Black_Scholes(type, 0.05, 0.05, s, 100, 0.01))

    fig, ax = plt.subplots()
    ax.plot(spot, price)
    ax.set(xlabel='Spot', ylabel='Option Price', title=type + ' Option Prices')
    ax.grid()
    fig.savefig('Black_Scholes_' + type + '.png')
    plt.show()

price_plot('Call')
