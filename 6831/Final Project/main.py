# main.py

import numpy as np
import scipy
from OptionValuer import OptionValuer
from Brownian_Motion import BM
from JumpDiffusion import JumpDiffusion


# option parameters:
St = np.linspace(34, 46, 13, endpoint=True)
r = 0.06
sigma = 0.4
T = 2
K = 40

# payoff function
def Call_Payoff(stock_price, strike_price):
    return max(stock_price - strike_price, 0)


def Put_Payoff(stock_price, strike_price):
    return max(strike_price - stock_price, 0)

payoff = Call_Payoff(St.all(), K)

# number of exercise points in one year
times = 50
# number of simulations, total paths number would be 2N
N = 10000

# steps between exercise points when generating paths
step = 100
step_year = step * times
