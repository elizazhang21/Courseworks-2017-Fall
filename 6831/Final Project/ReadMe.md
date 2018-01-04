# Valuing American Options by Simulation
Final Project - FRE 6831

## 1 Overview
Longstaff(2001)[1] proposed a pricing model for American options by simulation. The model is flexible and applicable in path-dependent and multi-factor situations where traditional finite difference techniques cannot be used. In this project, we implemented this pricing model in Python and briefly evaluated this mode. Also we developed FD and binomial method for American options and the results turn out to be really close and verify the feasibility of these methods.

## 2 Mathematical Details
### 2.1 Valuation Framework
We value American options by simulating enough paths of underlying asset price and compute option price of these paths at each time backwards. At a certain time $t_k$ and outcome $\omega$, we choose greater one of its early-exercise and continuation value as option price:
$$ Y(t_K, \omega) = \max(P(t_K, \omega), F(t_k, \omega))$$

### 2.2 Compute Continuation Value
In order to estimate continuation value only using our simulated asset price processes, we project continuation value on
current asset value X(tk;w) and assume it can be expressed as linear combination of a set of base function dependent
only on X.

### 2.3 Algorithm

## 3 Experiment Settings
### 3.1 Price Simulation
We first use geometric Brownian motion as in Black-Sheol model to simulate underlying asset price:

### 3.2 Base Functions
As mentioned in original paper, we use first 3 terms of Laguerre polynomials as well as a constant term as our base
functions:

### 3.3 Other Parameters
As in original paper, we set number of early exercise times as 50 per year, i.e. we take 50 points per year with equal
interval from simulated paths. Since early experiment results suggests higher simulation number doesn’t affect valued
price, we set it as 20,000 (10,000 antithetic in case of geometric Brownian motion) to instead of 100,000 as in original
paper, in order to speed up our program.

## 4 Experiment Result
We first applied our model on American put options and compared results with finite difference method.

### 4.1 Valuing American Put Option

## 5 Conclusion

## Reference
[1] Longstaff F A, Schwartz E S. Valuing American options by simulation: a simple least-squares approach[J]. Review
of Financial studies, 2001, 14(1): 113-147.
