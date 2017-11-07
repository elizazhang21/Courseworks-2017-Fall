# main.py
import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from EuropeanOptionPayoff import EuropeanCallOptionPayoff, EuropeanPutOptionPayoff
from EuropeanOptionTradingStrategy import StraddleStrategy, ButterflyStrategy
from BlackScholesEuropeanOption import BlackScholesEuropeanCall, BlackScholesEuropeanPut

# Data initialization
t = np.linspace(0, 1, 100, endpoint=False)
T = 1
stock_price = np.linspace(0.5, 100, 200, endpoint=True)
strike_price = 50
strike_price_1 = 20
strike_price_3 = 80
interest_rate = 0.2
dividend_yield = 0.05
volatility = 0.1

# --------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- 2-D Figures --------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------
straddle_strategy = []
butterfly_strategy = []
bs_call = []
bs_put = []

for s in stock_price:
    # straddle_strategy = StraddleStrategy()
    straddle_strategy.append(StraddleStrategy(s, strike_price))

    # butterfly_strategy = ButterflyStrategy()
    butterfly_strategy.append(ButterflyStrategy(
        s, strike_price_1, strike_price_3))

    try:
        # BS_european_call_price, BS_european_call_delta, BS_european_call_gamma, BS_european_call_theta, BS_european_call_vega
        bs_call.append(BlackScholesEuropeanCall(
            0, T, s, strike_price, interest_rate, dividend_yield, volatility)[0])
        bs_put.append(BlackScholesEuropeanPut(
            0, T, s, strike_price, interest_rate, dividend_yield, volatility)[0])
    except:
        continue

# ------------------------------------------ 2-D Figure for the Trading Strategies ------------------------------------------

fig, ax = plt.subplots()
ax.plot(stock_price, straddle_strategy, 'k--',
        color='blue', label='Straddle Strategy')
ax.plot(stock_price, butterfly_strategy, 'k:',
        color='red', label='Butterfly Strategy')
legend = ax.legend(loc='upper right')
plt.xlabel('Stock Price')
plt.ylabel('Strategy Payoff')
plt.title('2-D Figure for Trading Strategies')
plt.show()

# ------------------------------------------ 2-D Figure for payoff and price ------------------------------------------

fig, ax = plt.subplots()
ax.plot(stock_price, bs_call, 'k--',
        color='blue', label='European Call Option')
ax.plot(stock_price, bs_put, 'k:',
        color='red', label='European Put Option')
legend = ax.legend(loc='upper right')
plt.xlabel('Stock Price')
plt.ylabel('Option Payoff')
plt.title('2-D Figure for Payoff and Price')
plt.show()

# --------------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------- 3-D Figures --------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------ 3-D figure for Black-Scholes price surface ------------------------------------------
# Subplot 1 is for Call Option. Subplot 2 is for Put Option.


# Align input data using meshgrid
stock_price, t = np.meshgrid(stock_price, t)
c, c_delta, c_gamma, c_theta, c_vega = BlackScholesEuropeanCall(t, T, stock_price, strike_price, interest_rate, dividend_yield, volatility)
p, p_delta, p_gamma, p_theta, p_vega = BlackScholesEuropeanPut(t, T, stock_price, strike_price, interest_rate, dividend_yield, volatility)

# Plot 3D figure
fig = plt.figure()

ax = fig.add_subplot(2, 1, 1, projection='3d')
surf = ax.plot_surface(stock_price, T - t, c)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('BS - Prices')
plt.title('3-D Figures for Call Price Surface')

ax = fig.add_subplot(2, 1, 2, projection='3d')
surf = ax.plot_surface(stock_price, T - t, p)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('BS - Prices')
plt.title('3-D Figures for Put Price Surface')

plt.show()


# ------------------------------------------ 3-D figure for the Greeks of Call Option ------------------------------------------
# x-axis is stock price, y-axis is time to maturity, z-axis is the value of the Greeks


fig = plt.figure()

# The first figure is for delta
ax = fig.add_subplot(2, 2, 1, projection='3d')
surf = ax.plot_surface(stock_price, T - t, c_delta)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Delta')

# The second figure is for gamma
ax = fig.add_subplot(2, 2, 2, projection='3d')
surf = ax.plot_surface(stock_price, T - t, c_gamma)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Gamma')

# The third figure is for theta
ax = fig.add_subplot(2, 2, 3, projection='3d')
surf = ax.plot_surface(stock_price, T - t, c_theta)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Theta')

# The last figure is for vega
ax = fig.add_subplot(2, 2, 4, projection='3d')
surf = ax.plot_surface(stock_price, T - t, c_vega)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Vega')

fig.suptitle('3-D Figures for Greeks of Call Option')
plt.show()

# ------------------------------------------ 3-D figure for the Greeks of Put Option ------------------------------------------


fig = plt.figure()

# The first figure is for delta
ax = fig.add_subplot(2, 2, 1, projection='3d')
surf = ax.plot_surface(stock_price, T - t, p_delta)
ax.set_xlabel('Stock Price')
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Delta')

# The second figure is for gamma
ax = fig.add_subplot(2, 2, 2, projection='3d')
surf = ax.plot_surface(stock_price, T - t, p_gamma)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Gamma')

# The third figure is for theta
ax = fig.add_subplot(2, 2, 3, projection='3d')
surf = ax.plot_surface(stock_price, T - t, p_theta)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Theta')

# The last figure is for vega
ax = fig.add_subplot(2, 2, 4, projection='3d')
surf = ax.plot_surface(stock_price, T - t, p_vega)
ax.set_ylabel('Time to Maturity')
ax.set_zlabel('Vega')

fig.suptitle('3-D Figures for Greeks of Put Option')
plt.show()
