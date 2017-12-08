# Valuing American Options by Simulation
Final Project - FRE 6831

## Overview
In this project, we would implement an algorithm to price American Options by simulation.

The model is flexible and applicable in path-dependent and multifactor situations(i.e. exercise payoff is calculted as in Asian options) where traditional finite difference techniques cannot be used..

##Specification
### Valuation Framework
We value American options by simulating enough paths of underlying asset price and compute option price of these
paths at each time backwards. At a certain time tk and outcome w, we choose greater one of its early-exercise and
continuation value as option price

### Compute Continuation Value
In order to estimate continuation value only using our simulated asset price processes, we project continuation value on
current asset value X(tk;w) and assume it can be expressed as linear combination of a set of base function dependent
only on X.

### Algorithm
