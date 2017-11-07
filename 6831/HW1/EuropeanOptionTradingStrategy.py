# EuropeanOptionTradingStrategy.py
from EuropeanOptionPayoff import EuropeanCallOptionPayoff, EuropeanPutOptionPayoff

def StraddleStrategy(stock_price, strike_price):
    # compute the straddle strategy by calling the functions in EuropeanOptionPayoff.py
    straddle_strategy = EuropeanCallOptionPayoff(stock_price, strike_price) + EuropeanPutOptionPayoff(stock_price, strike_price)
    return straddle_strategy


def ButterflyStrategy(stock_price, strike_price_1, strike_price_3):
    strike_price_2 = (strike_price_1 + strike_price_3) / 2
    # compute the straddle strategy by calling the functions in EuropeanOptionPayoff.py
    butterfly_strategy = EuropeanCallOptionPayoff(stock_price, strike_price_1) + EuropeanCallOptionPayoff(
        stock_price, strike_price_3) - 2 * EuropeanCallOptionPayoff(stock_price, strike_price_2)
    return butterfly_strategy
