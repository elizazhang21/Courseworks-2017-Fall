# main.py
import numpy as np
from scipy.stats import lognorm, gmean, norm, describe
from scipy.stats import rv_continuous
import matplotlib.pyplot as plt
from RandomNumberGenerator import *
from MonteCarloForStockPrice import *
from ControlVariatesAsianCallOption import *


# initialize all the parameter
price = 20
strike = 10
r = 0.05
sigma = 0.2
delta = 0.00
current_time = 0
maturity = 1
step_number = 252
trajectory_numbers = 10000

# Generate the plots:
# sample trajectory of geometric Brownian motion with jumps
# histogram with log-normal distribution of St of each sample trajectory
# correlation of geometric average price Asian Call Xi and arithmetic
# average price Asian call Yi

# ================================================================================================
# ======================== sample trajectory of geometric Brownian motion ========================
# ================================================================================================
# analyze what you observe

terminal = np.zeros(10000)
geometric = np.zeros(10000)
arithmetric = np.zeros(10000)

time = np.linspace(0.01, 1, step_number)


fig = plt.figure()
ax = fig.add_subplot(111)
for i in range(10000):
    PriceList = Jump_Diffusion_Process_At_Fixed_Dates(
        price, maturity, step_number, r, sigma, delta, 100, 0, 0)
    ax.plot(time, PriceList, 'k--', c=np.random.rand(3,))
# legend = ax.legend(loc='upper right', fontsize=8)
plt.xlabel('Time to maturity', fontsize=8)
plt.ylabel('Simulated Option Price', fontsize=8)
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(6)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(6)
plt.title('10000 Sample Paths of Geometric Brownian Motion', fontsize=8)
plt.show()

# =======================================================================================================
# ===================== histogram with log-normal distribution of St of each trajectory =================
# =======================================================================================================

end = []
for i in range(10000):
    end.append(Jump_Diffusion_Process_At_Fixed_Dates(
        price, maturity, step_number, r, sigma, delta, 100, 0, 0)[-1])
shape, loc, mean = lognorm.fit(end)
x = np.linspace(0, 40, 10000)
dist = lognorm.pdf(x, shape, loc, mean)
fig = plt.figure()
ax = fig.add_subplot(111)
a = np.hstack(end)
# ax.plot(x, lognorm.pdf(x, s), 'r-', lw=5, alpha=0.6, label='lognorm pdf')
ax.plot(x, dist, color='red', label='Fitted Terminal Prices')
ax.hist(a, normed=True, bins='auto', color='blue',
        label='Simulated Terminal Prices')
legend = ax.legend(loc='upper right', fontsize=4)
plt.xlabel('Terminal Price', fontsize=10)
plt.ylabel('Density', fontsize=10)
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(8)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(8)
plt.title('Histogram with Log-normal Distribution of St', fontsize=10)
plt.legend()
plt.show()


# =======================================================================================================
# =================== correlation of geometric average and arithmetic average prices ====================
# =======================================================================================================

am_list, gm_list, cv_list = Control_Variates_Arithmetic_Average_Asian_Call(20, 10, 0.05, 0.2, 0.01, 0, 1, 252, 10000)
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(am_list, gm_list, '.', color='blue', markersize=2)
plt.xlabel('Payoff of Arithmetic Average Asian Call')
plt.ylabel('Payoff of Geometric Average Asian Call')
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(8)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(8)
plt.title('Correlation of Geometric and Arithmetic Average Asian Call', fontsize=10)
plt.show()
