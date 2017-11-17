# BlackScholesEuropeanOption.py
import numpy as np
from scipy.stats import norm


# Define values of prices and greeks of call option. This function returns a tuple of all the values.
def BlackScholesEuropeanCall(t, T, stock_price, strike_price, interest_rate,
                             dividend_yield, volatility):
    # compute the Black Scholes European Call
    r = interest_rate
    maturity = T - t
    delta = dividend_yield
    S = stock_price
    K = strike_price
    d1 = (np.log(S / K) + (r + 0.5 * volatility * volatility) * maturity) / volatility / np.sqrt(maturity)
    d2 = d1 - volatility * np.sqrt(maturity)

    BS_european_call_price = S * \
        norm.cdf(d1) * np.exp(-delta * maturity) - K * np.exp(-r * maturity) * norm.cdf(d2)
    BS_european_call_delta = np.exp(- delta * maturity) * norm.cdf(d1)
    BS_european_call_gamma = norm.pdf(
        d1) * np.exp(-delta * maturity) / S / volatility / np.sqrt(maturity)
    BS_european_call_theta = -np.exp(-delta * maturity) * S * norm.pdf(d1) * volatility / 2 / np.sqrt(
        maturity) - r * K * np.exp(-r * maturity) * norm.cdf(-d2) - delta * S * np.exp(-delta * maturity) * norm.cdf(-d1)
    BS_european_call_vega = S * np.exp(-delta * maturity) * norm.pdf(d1) * np.sqrt(maturity)

    return BS_european_call_price, BS_european_call_delta, BS_european_call_gamma, BS_european_call_theta, BS_european_call_vega


# Define values of prices and greeks of put option. This function returns a tuple of all the values.
def BlackScholesEuropeanPut(t, T, stock_price, strike_price, interest_rate,
                            dividend_yield, volatility):
    # compute the Black Scholes European Call
    r = interest_rate
    maturity = T - t
    delta = dividend_yield
    S = stock_price
    K = strike_price
    d1 = (np.log(S / K) + (r + 0.5 * volatility * volatility) *
          maturity) / volatility / np.sqrt(maturity)
    d2 = d1 - volatility * np.sqrt(maturity)

    BS_european_put_price = K * \
        np.exp(-r * maturity) * norm.cdf(-d2) - S * norm.cdf(-d1) * np.exp(-delta * maturity)
    BS_european_put_delta = np.exp(- delta * maturity) * norm.cdf(-d1)
    BS_european_put_gamma = norm.pdf(
        d1) * np.exp(-delta * maturity) / S / volatility / np.sqrt(maturity)
    BS_european_put_theta = -np.exp(-delta * maturity) * S * norm.pdf(d1) * volatility / 2 / np.sqrt(
        maturity) + r * K * np.exp(-r * maturity) * norm.cdf(-d2) - delta * S * np.exp(-delta * maturity) * norm.cdf(-d1)
    BS_european_put_vega = S * np.exp(-delta * maturity) * norm.pdf(d1) * np.sqrt(maturity)

    return BS_european_put_price, BS_european_put_delta, BS_european_put_gamma, BS_european_put_theta, BS_european_put_vega
