# Black_Scholes_Implicit_FD.py

import numpy as np
import scipy  # scipy.sparse
from EuropeanOptionPayoff import EuropeanCallOptionPayoff, EuropeanPutOptionPayoff
from BlackScholesEuropeanOption import BlackScholesEuropeanCall, BlackScholesEuropeanPut
from LU_Decomposition_Matrix_Inverse import LU_Decomposition_Matrix_Inverse


def Black_Scholes_Implicit_FD(s_max, s_min, M, N, T, t, r, delta, sigma, payoff_function):
    # M = size of price
    # N = size of time
    # set all the parameters
    stock_price = np.linspace(s_min, s_max, M + 1, endpoint=True)
    maturity = np.linspace(0, T - t, N + 1, endpoint=True)
    strike_price = 0.5 * (s_max + s_min)
    dS = (s_max - s_min) / M  # dS is length of every price step
    dt = (T - t) / N  # dt is length of every time step

    # check the stability condition
    if 0 < dt / dS ** 2 < 0.5:
        print('The stability condition holds.')
        print('delta_t = ' + str(dt))
        print('delta_s = ' + str(dS))
    else:
        print('The stability condition does not hold.')
        print('The programme has been terminated.')
        return None

    # define the constants
    l = np.zeros(M + 1)
    d = np.zeros(M + 1)
    u = np.zeros(M + 1)
    V = np.zeros(M - 1)
    v_list = []

    for i in range(M + 1):
        s = stock_price[i]
        t = maturity[i]

        l[i] = - (sigma ** 2) * (s ** 2) / 2 * dt / (dS ** 2) + (r - delta) * s / 2 * dt / dS
        d[i] = 1 + r * dt + (sigma ** 2) * (s ** 2) * dt / (dS ** 2)
        u[i] = - sigma ** 2 * s ** 2 / 2 * dt / dS ** 2 - (r - delta) * s / 2 * dt / dS

    # form the weighting matrix A
    A = np.zeros((M - 1, M - 1))
    for i in range(M - 2):
        A[i][i] = d[i + 1]
        A[i][i + 1] = u[i + 1]
        A[i + 1][i] = l[i + 2]
        A[M - 2][M - 2] = d[M - 1]

    # initial condition
    # boundary conditions: Dirichlet Boundary Condition
    if payoff_function == 'call':
        for i in range(M - 1):
            V[i] = EuropeanCallOptionPayoff(stock_price[i + 1], strike_price)
        v_list.append(V)
    elif payoff_function == 'put':
        for i in range(M - 1):
            V[i] = EuropeanPutOptionPayoff(stock_price[i + 1], strike_price)
        v_list.append(V)

    # Implicit finite difference
    # solve the equation (A_k)V[k+1] = V_K + b
    for k in range(N):
        if payoff_function == 'call':
            # initial condition
            # boundary conditions: Dirichlet Boundary Condition
            v_0 = 0
            v_N = EuropeanCallOptionPayoff(s_max, strike_price)
            b = np.zeros(M - 1)
            b[0] = - l[1] * v_0
            b[M - 2] = - u[M - 1] * v_N
            # solve the equation (A_k)V[k+1] = b
            V = LU_Decomposition_Matrix_Inverse(A, V + b)
            v_list.append(V)

        elif payoff_function == 'put':
            v_0 = EuropeanPutOptionPayoff(s_min, strike_price)
            v_N = 0
            b = np.zeros(M - 1)
            b[0] = - l[1] * v_0
            b[M - 2] = - u[M - 1] * v_N
            # solve the equation (A_k)V[k+1] = b
            V = LU_Decomposition_Matrix_Inverse(A, V + b)
            v_list.append(V)

    option_price_implicit_FD = np.array(v_list)
    return option_price_implicit_FD  # put_option_price_explicit_FD

a = Black_Scholes_Implicit_FD(100, 0, 3, 3, 1, 0.5, 0.2, 0.1, 0.05, 'call')
print(a)
a = Black_Scholes_Implicit_FD(100, 0, 3, 3, 1, 0.5, 0.2, 0.1, 0.05, 'put')
print(a)
