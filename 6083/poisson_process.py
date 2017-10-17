import numpy as np
from scipy.stats import poisson
import matplotlib.pyplot as plt


x = np.random.poisson(lam=2, size=10000)  # lam为λ size为k
pillar = 5
a = plt.hist(x, bins=pillar, normed=True, range=[0, pillar], color='b', alpha=0.5)
p = [0]
for i in range(5):
	a[0][i] += a[0][i-1]
	p.append(a[0][i])

plt.plot(p, 'r')
#plt.grid()
plt.show()


'''
rvs(mu, loc=0, size=1)	Random variates.
pmf(x, mu, loc=0)	Probability mass function.
logpmf(x, mu, loc=0)	Log of the probability mass function.
cdf(x, mu, loc=0)	Cumulative density function.
logcdf(x, mu, loc=0)	Log of the cumulative density function.
sf(x, mu, loc=0)	Survival function (1-cdf — sometimes more accurate).
logsf(x, mu, loc=0)	Log of the survival function.
ppf(q, mu, loc=0)	Percent point function (inverse of cdf — percentiles).
isf(q, mu, loc=0)	Inverse survival function (inverse of sf).
stats(mu, loc=0, moments=’mv’)	Mean(‘m’), variance(‘v’), skew(‘s’), and/or kurtosis(‘k’).
entropy(mu, loc=0)	(Differential) entropy of the RV.
expect(func, mu, loc=0, lb=None, ub=None, conditional=False)	Expected value of a function (of one argument) with respect to the distribution.
median(mu, loc=0)	Median of the distribution.
mean(mu, loc=0)	Mean of the distribution.
var(mu, loc=0)	Variance of the distribution.
std(mu, loc=0)	Standard deviation of the distribution.
interval(alpha, mu, loc=0)	Endpoints of the range that contains alpha percent of the distribution


fig, ax = plt.subplots(1, 1)
mu = 2
mean, var, skew, kurt = poisson.stats(mu, moments='mvsk')
x = np.arange(poisson.ppf(0.01, mu), poisson.ppf(0.99, mu))
ax.plot(x, poisson.pmf(x, mu), 'bo', ms=8, label='poisson pmf')
ax.vlines(x, 0, poisson.pmf(x, mu), colors='b', lw=5, alpha=0.5)
rv = poisson(mu)
ax.vlines(x, 0, rv.pmf(x), colors='k',
          linestyles='-', lw=1, label='frozen pmf')
ax.legend(loc='best', frameon=False)
plt.show()
'''
