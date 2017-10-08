import numpy as np
import math

# Set the parameters
ttm = 4.0 #time to maturity
tSteps = 2
r = 0.12 #intertst rate
d = 0 #divident yield
strike = 578 #strike price
spot = 581 #current stock price

dt = ttm / tSteps
up = 1.3
down = 0.8
discount = math.exp(-r*dt) 
p_up = (math.exp(r*2)-down)/(up - down)
print('Possibility of going up = ' + str(p_up)+'\n')
p_down = 1- p_up

# Build a binominal tree
lattice = np.zeros((tSteps+1, tSteps+1))
lattice[0][0] = spot
for i in range(tSteps):
    for j in range(i+1):
        lattice[i+1][j+1] = up * lattice[i][j]
    lattice[i+1][0] = down * lattice[i][0]
print('Binominal tree is ')
print(lattice)
print(' ')

# Calculate payoffs
def call_payoff(spot):
    global strike
    return max(spot - strike, 0.0)

# Backtrack the binominal tree
for i in range(tSteps, 0, -1):
    for j in range(i, 0, -1):
        if i == tSteps:
            lattice[i-1][j-1] = discount * \
                (p_up * call_payoff(lattice[i][j]) +
                 p_down * call_payoff(lattice[i][j-1]))
        else:
            lattice[i-1][j-1] = discount * \
                (p_up * lattice[i][j] + p_down * lattice[i][j-1])
print('Call price = ')
print(lattice[0][0])

