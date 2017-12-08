# Valuing American Options by Simulation
Final Project - FRE 6831

## Overview
In this project, we would implement an algorithm to price American Options by simulation.

The model is flexible and applicable in path-dependent and multifactor situations(i.e. exercise payoff is calculted as in Asian options) where traditional finite difference techniques cannot be used..

## Specification
### Valuation Framework
We value American options by simulating enough paths of underlying asset price and compute option price of these
paths at each time backwards. At a certain time tk and outcome w, we choose greater one of its early-exercise and
continuation value as option price

### Compute Continuation Value
In order to estimate continuation value only using our simulated asset price processes, we project continuation value on
current asset value X(tk;w) and assume it can be expressed as linear combination of a set of base function dependent
only on X.

### Algorithm

## Experiment Settings
### Price Simulation
We first use geometric Brownian motion as in Black-Sheol model to simulate underlying asset price:

### Base Functions
As mentioned in original paper, we use first 3 terms of Laguerre polynomials as well as a constant term as our base
functions:

### Other Parameters
As in original paper, we set number of early exercise times as 50 per year, i.e. we take 50 points per year with equal
interval from simulated paths. Since early experiment results suggests higher simulation number doesn’t affect valued
price, we set it as 20,000 (10,000 antithetic in case of geometric Brownian motion) to instead of 100,000 as in original
paper, in order to speed up our program.

## Experiment Result
We first applied our model on American put options and compared results with finite difference method.

### Valuing American Put Option

## Conclusion
