# main.py
import numpy as np
from scipy.stats import norm
from scipy.linalg import inv
import matplotlib.pyplot as plt


def Call(stock_price, strike_price):
    return np.maximum(stock_price - strike_price, 0)


def Put(stock_price, strike_price):
    return np.maximum(strike_price - stock_price, 0)


def RBF_G(epsilon, x, xi):

    # Gaussian: e^(-(epsilon*r)**2)
    # L_G = Gaussian RBF
    # L_x_G = first order derivatives of Gaussian Quandric RBF
    # L_xx_G = second order derivatives of Gaussian Quadric RBF

    N = len(x)
    L_G = np.zeros((N, N))
    L_x_G = np.zeros((N, N))
    L_xx_G = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            r = x[i] - xi[j]
            L_G[i][j] = np.exp(-(epsilon * r) ** 2)
            L_x_G[i][j] = -2 * epsilon ** 2 * r * np.exp(-((epsilon * r) ** 2))
            L_xx_G[i][j] = 4 * epsilon ** 4 * r ** 2 * np.exp(-((epsilon * r) ** 2)) - 2 * epsilon ** 2 * np.exp(-((epsilon * r) ** 2))

    return L_G, L_x_G, L_xx_G


def RBF_MQ(epsilon, x, xi):

    # Multi_Quadric: sqrt(1+(e(x-xi))**2)
    # L_MQ = Multi_Quadric RBF
    # L_x_MQ = first order derivatives of Multi-Quadric RBF
    # L_xx_MQ = second order derivatives of Multi-Quadric RBF

    N = len(x)
    L_MQ = np.zeros((N, N))
    L_x_MQ = np.zeros((N, N))
    L_xx_MQ = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            r = x[i] - xi[j]
            L_MQ[i][j] = np.sqrt(1 + (epsilon * r) ** 2)
            L_x_MQ[i][j] = epsilon * r / L_MQ[i][j]
            L_xx_MQ[i][j] = epsilon ** 2 / L_MQ[i][j] - (epsilon ** 2 * r) ** 2 / L_MQ[i][j] ** 3

    return L_MQ, L_x_MQ, L_xx_MQ


class BS_Global_RBF(object):

    def __init__(self, s_max, s_min, K, M, N, T, r, sigma, epsilon, option):
        self.s_max = s_max
        self.s_min = s_min
        self.K = K
        self.M = M
        self.N = N
        self.T = T
        self.r = r
        self.sigma = sigma
        self.epsilon = epsilon
        self.option = option

    def stockprice(self):
        s = np.linspace(np.log(self.s_min), np.log(self.s_max), self.M)
        s = np.exp(s)
        return s

    def BS_Call(self):
        s = self.stockprice()
        T = self.T
        K = self.K
        r = self.r
        sigma = self.sigma
        call_price = []
        for S in s:
            d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / sigma / np.sqrt(T)
            d2 = d1 - sigma * np.sqrt(T)
            call_price.append(S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2))
        return call_price

    def BS_Put(self):
        s = self.stockprice()
        T = self.T
        K = self.K
        r = self.r
        sigma = self.sigma
        put_price = []
        for S in s:
            d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / sigma / np.sqrt(T)
            d2 = d1 - sigma * np.sqrt(T)
            put_price.append(K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1))
        return put_price

    def Global_RBF_G(self):
        s_max = self.s_max
        s_min = self.s_min
        K = self.K
        M = self.M
        N = self.N
        T = self.T
        r = self.r
        sigma = self.sigma
        epsilon = self.epsilon
        option = self.option

        dt = T / (N - 1)
        # choose collocation points
        x = np.linspace(np.log(s_min), np.log(s_max), M)
        time = np.linspace(0, T, N)
        stock_price = np.exp(x)

        L, L_x, L_xx = RBF_G(epsilon, x, x)

        # boundary conditions
        v = np.apply_along_axis(option, 0, stock_price, K)
        # calculate lambda 1 using 6.2.36
        lambda_k = np.zeros(M)
        # set the initial condition v1 at T = 0
        for i in range(0, M):
            lambda_k[i] = option(stock_price[i], K)
        lambda_k[-1] = option(stock_price[-1], K * np.exp(-r * (T)))
        lambda_k = inv(L).dot(lambda_k)

        P = r * np.identity(M) - (r - 0.5 * sigma ** 2) * (inv(L)).dot(L_x) - 0.5 * (sigma ** 2) * (inv(L)).dot(L_xx)
        PP = np.identity(M) - 0.5 * dt * P
        PPinv = inv(PP)

        for k in range(1, N):
            # update boundary conditions
            v[0] = option(s_min, K * np.exp(-r * dt * k))
            v[-1] = option(s_max, K * np.exp(-r * dt * k))
            # calculate lambda_k*
            lambda_k = inv(L).dot(v)
            # calculating lambda k+1 using 6.2.30
            lambda_k = inv((np.identity(M) + 0.5 * dt * P)).dot(np.identity(M) - 0.5 * dt * P).dot(lambda_k)
            v = L.dot(lambda_k)
        return v

    def Global_RBF_MQ(self):
        s_max = self.s_max
        s_min = self.s_min
        K = self.K
        M = self.M
        N = self.N
        T = self.T
        r = self.r
        sigma = self.sigma
        epsilon = self.epsilon
        option = self.option

        dt = T / (N - 1)
        # choose collocation points
        x = np.linspace(np.log(s_min), np.log(s_max), M)
        time = np.linspace(0, T, N)
        stock_price = np.exp(x)

        L, L_x, L_xx = RBF_MQ(epsilon, x, x)

        # boundary conditions
        v = np.apply_along_axis(option, 0, stock_price, K)
        # calculate lambda 1 using 6.2.36
        lambda_k = np.zeros(M)
        # set the initial condition v1 at T = 0
        for i in range(0, M):
            lambda_k[i] = option(stock_price[i], K)
        lambda_k[-1] = option(stock_price[-1], K * np.exp(-r * (T)))
        lambda_k = inv(L).dot(lambda_k)

        P = r * np.identity(M) - (r - 0.5 * sigma ** 2) * (inv(L)
                                                           ).dot(L_x) - 0.5 * (sigma ** 2) * (inv(L)).dot(L_xx)
        PP = np.identity(M) - 0.5 * dt * P
        PPinv = inv(PP)

        for k in range(1, N):
            v = L.dot(lambda_k)
            # update boundary conditions
            v[0] = option(s_min, K * np.exp(-r * dt * k))
            v[-1] = option(s_max, K * np.exp(-r * dt * k))
            # calculate lambda_k*
            lambda_k = inv(L).dot(v)
            # calculating lambda k+1 using 6.2.30
            lambda_k = inv((np.identity(M) + 0.5 * dt * P)).dot(np.identity(M) - 0.5 * dt * P).dot(lambda_k)
        return v


RBF_call = BS_Global_RBF(400, 1, 100, 100, 50, 1, 0.1, 0.1, 10, Call)
s_call = RBF_call.stockprice()
K_call = RBF_call.K
p_G_call = RBF_call.Global_RBF_G()
p_MQ_call = RBF_call.Global_RBF_MQ()
p_BS_call = RBF_call.BS_Call()

RBF_put = BS_Global_RBF(400, 1, 100, 100, 50, 1, 0.1, 0.1, 10, Put)
s_put = RBF_put.stockprice()
K_put = RBF_put.K
p_G_put = RBF_put.Global_RBF_G()
p_MQ_put = RBF_put.Global_RBF_MQ()
p_BS_put = RBF_put.BS_Put()


# ===============================================================================================
# =========================        Figure for Call Option Prices        =========================
# ===============================================================================================

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(s_call, p_G_call, 'r+', c='red', label='Gaussian RBF')
ax.plot(s_call, p_MQ_call, 'r+', c='orange', label='MQ RBF')
ax.plot(s_call, p_BS_call, 'k-', c='blue', label='BS model')
legend = ax.legend(loc='best', fontsize=8)
plt.xlabel('Stock Price', fontsize=8)
plt.ylabel('Option Price', fontsize=8)
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(6)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(6)
plt.title('BS Global Radial Basis Function Method', fontsize=8)
plt.grid()
plt.show()

# ===============================================================================================
# =========================        Figure for Put Option Prices        ==========================
# ===============================================================================================

fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(s_put[:-5], p_G_put[:-5], 'r+', c='red', label='Gaussian RBF')
ax.plot(s_put[:-5], p_MQ_put[:-5], 'r+', c='orange', label='MQ RBF')
ax.plot(s_put[:-5], p_BS_put[:-5], 'k-', c='blue', label='BS model')
legend = ax.legend(loc='best', fontsize=8)
plt.xlabel('Stock Price', fontsize=8)
plt.ylabel('Option Price', fontsize=8)
for label in ax.xaxis.get_ticklabels():
    label.set_fontsize(6)
for label in ax.yaxis.get_ticklabels():
    label.set_fontsize(6)
plt.title('BS Global Radial Basis Function Method', fontsize=8)
plt.grid()
plt.show()
