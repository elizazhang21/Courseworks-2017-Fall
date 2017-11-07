# BlackScholesEuropeanOption.py
import numpy as np
from scipy.stats import norm


def log(x):
    return np.log(x)


def sqrt(x):
    return np.sqrt(x)


def exp(x):
    return np.exp(x)


def cdf(x):
    return norm.cdf(x)


def pdf(x):
    return norm.pdf(x)


def BlackScholesEuropeanCall(t, T, stock_price, strike_price, interest_rate,
                             dividend_yield, volatility):
    # compute the Black Scholes European Call
    r = interest_rate
    maturity = T - t
    delta = dividend_yield
    S = stock_price
    K = strike_price
    d1 = (log(S / K) + (r + 0.5 * volatility * volatility) * maturity) / volatility / sqrt(maturity)
    d2 = d1 - volatility * sqrt(maturity)

    BS_european_call_price = S * \
        cdf(d1) * exp(-delta * maturity) - K * exp(-r * maturity) * cdf(d2)
    BS_european_call_delta = exp(- delta * maturity) * cdf(d1)
    BS_european_call_gamma = pdf(
        d1) * exp(-delta * maturity) / S / volatility / sqrt(maturity)
    BS_european_call_theta = -exp(-delta * maturity) * S * pdf(d1) * volatility / 2 / sqrt(
        maturity) - r * K * exp(-r * maturity) * cdf(-d2) - delta * S * exp(-delta * maturity) * cdf(-d1)
    BS_european_call_vega = S * exp(-delta * maturity) * pdf(d1) * sqrt(maturity)

    return BS_european_call_price, BS_european_call_delta, BS_european_call_gamma, BS_european_call_theta, BS_european_call_vega


def BlackScholesEuropeanPut(t, T, stock_price, strike_price, interest_rate,
                            dividend_yield, volatility):
    # compute the Black Scholes European Call
    r = interest_rate
    maturity = T - t
    delta = dividend_yield
    S = stock_price
    K = strike_price
    d1 = (log(S / K) + (r + 0.5 * volatility * volatility) *
          maturity) / volatility / sqrt(maturity)
    d2 = d1 - volatility * sqrt(maturity)

    BS_european_put_price = K * \
        exp(-r * maturity) * cdf(-d2) - S * cdf(-d1) * exp(-delta * maturity)
    BS_european_put_delta = exp(- delta * maturity) * cdf(-d1)
    BS_european_put_gamma = pdf(
        d1) * exp(-delta * maturity) / S / volatility / sqrt(maturity)
    BS_european_put_theta = -exp(-delta * maturity) * S * pdf(d1) * volatility / 2 / sqrt(
        maturity) + r * K * exp(-r * maturity) * cdf(-d2) - delta * S * exp(-delta * maturity) * cdf(-d1)
    BS_european_put_vega = S * exp(-delta * maturity) * pdf(d1) * sqrt(maturity)

    return BS_european_put_price, BS_european_put_delta, BS_european_put_gamma, BS_european_put_theta, BS_european_put_vega
