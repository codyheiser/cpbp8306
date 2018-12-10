# -*- coding: utf-8 -*-
"""
Heiser_11.py
@author: Cody Heiser
"""
import argparse
import numpy as np
import scipy.stats as stats
from scipy.special import logit
import matplotlib.pyplot as plt
plt.style.use("ggplot")
import seaborn as sns; sns.set_style("white")
import pymc3


class distribution:
	def __init__(self):
		self.x = np.linspace(0, 1, 200) # generate 200 independent, linearly-spaced variables in range [0, 1]
		self.dist = self.x # initiate distribution attribute with x values as placeholder


	def plot_dist(self, label=None, color='blue'):
		plt.plot(self.x, self.dist, "--", label=label, color=color)



class _beta(distribution):
	def __init__(self, a, b):
		distribution.__init__(self) # _beta class inherits from distribution class
		self.a = np.round(a, 4)
		self.b = np.round(b, 4)
		self.dist = stats.beta.pdf(self.x, a, b) # generate beta probability density function given x, alpha, beta


	def pymc3_beta(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Beta(name, alpha=self.a, beta=self.b)


	def to_gauss(self):
		'''return gaussian distribution for corresponding alpha and beta values'''
		mu = self.a/(self.a + self.b)
		sigma = np.sqrt((self.a*self.b)/(((self.a + self.b)**2)*(self.a + self.b + 1)))
		return _gauss(mu, sigma) # return gaussian probability density function given x, alpha, beta


	def calc_posterior(self, n_heads, n_tails):
		'''create posterior beta distribution following n_heads and n_tails observations'''
		post = _beta(a = n_heads + 1, b = n_tails + 1) # add observations to parameters from prior
		F = np.nan_to_num(post.dist)*np.nan_to_num(self.dist) # multiply posterior by prior
		return F/np.trapz(F, x=self.x) # normalize to integral of resulting distribution


	def plot_posterior(self, n_heads, n_tails, label=None, color='blue'):
		'''plot posterior beta distribution following n_heads and n_tails observations'''
		post = _beta(a = n_heads + 1, b = n_tails + 1) # add observations to parameters from prior
		F = np.nan_to_num(post.dist)*np.nan_to_num(self.dist) # multiply posterior by prior
		plt.plot(self.x, F/np.trapz(F, x=self.x), "-", label=label, color=color)



class _gauss(distribution):
	def __init__(self, m, s):
		distribution.__init__(self) # _gauss class inherits from distribution class
		self.m = np.round(m, 4)
		self.s = np.round(s, 4)
		self.dist = stats.norm.pdf(self.x, m, s) # generate gaussian probability density function given x, mu, sigma


	def to_beta(self):
		'''return beta distribution for corresponding mu and sigma values'''
		alpha = (self.m**2)*(((1-self.m)/(self.s**2))-(1/self.m))
		beta = alpha*(1/self.m - 1)
		return _beta(alpha, beta) # return beta probability density function given x, mu, sigma



class _kumaraswamy(distribution):
	def __init__(self, a, b):
		distribution.__init__(self)
		self.a = np.round(a, 4)
		self.b = np.round(b, 4)
		self.dist = (a*b*self.x**(a-1))*(1-self.x**a)**(b-1)


	def pymc3_kumaraswamy(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Kumaraswamy(name, a=self.a, b=self.b)



class _uniform(distribution):
	def __init__(self):
		distribution.__init__(self)
		self.dist = stats.uniform.pdf(self.x)


	def pymc3_uniform(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Uniform(name, lower=self.x[0], upper=self.x[-1])



class _triangular(distribution):
	def __init__(self, lower, upper):
		distribution.__init__(self)
		self.upper = upper
		self.lower = lower
		self.center = (upper+lower)/2
		scale = upper - lower
		c_ = (self.center - lower)/scale
		self.dist = stats.triang.pdf(self.x, loc = lower, c=c_, scale=scale)


	def pymc3_triang(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Triangular(name, lower=self.lower, upper=self.upper)



class _logitnormal(distribution):
	def __init__(self, m, s):
		distribution.__init__(self)
		self.m = np.round(m, 4)
		self.s = np.round(s, 4)
		self.dist = stats.norm.pdf(logit(self.x), loc=m, scale=s) * 1/(self.x * (1-self.x))


	def pymc3_logitnormal(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.LogitNormal(name, mu=self.m, sd=self.s)



if __name__ == '__main__':
	# Parameter values for prior and analytic posterior
	n = 50
	z = 10
	# How many iterations of the Metropolis algorithm to carry out for MCMC
	iterations = 10000
	# number of bins for histogram results
	bins=50

	# Plot the posterior histogram from MCMC analysis
	plt.figure('Part A', figsize=(12,6))
	plt.xlabel("$\\theta$, Fairness")
	plt.ylabel("Density")

	plt.subplot(2,3,1)
	beta_prior = _beta(12, 12)
	beta_prior.plot_dist(label='Prior')
	beta_prior.plot_posterior(n_heads=10, n_tails=40, label='Posterior (Analytic)')

	plt.subplot(2,3,2)
	uniform_prior = _uniform()
	uniform_prior.plot_dist(label='Prior (Uniform)', color='pink')

	plt.subplot(2,3,3)
	kumaraswamy_prior = _kumaraswamy(2, 2)
	kumaraswamy_prior.plot_dist(label='Prior (Kumaraswamy)', color='green')

	plt.subplot(2,3,4)
	logitnorm_prior = _logitnormal(0, 0.3)
	logitnorm_prior.plot_dist(label='Prior (LogitNormal)', color='indigo')

	plt.subplot(2,3,5)
	triang_prior = _triangular(0, 1)
	triang_prior.plot_dist(label='Prior (Triangular)', color='orange')

	# Use PyMC3 to construct a model context
	with pymc3.Model() as basic_model:
		theta0 = beta_prior.pymc3_beta("theta0")
		y0 = pymc3.Binomial("y0", n=n, p=theta0, observed=z)
		theta1 = uniform_prior.pymc3_uniform("theta1")
		y1 = pymc3.Binomial("y1", n=n, p=theta1, observed=z)
		theta2 = kumaraswamy_prior.pymc3_kumaraswamy("theta2")
		y2 = pymc3.Binomial("y2", n=n, p=theta2, observed=z)
		theta3 = logitnorm_prior.pymc3_logitnormal("theta3")
		y3 = pymc3.Binomial("y3", n=n, p=theta3, observed=z)
		theta4 = triang_prior.pymc3_triang("theta4")
		y4 = pymc3.Binomial("y4", n=n, p=theta4, observed=z)
		# Carry out the MCMC analysis using the Metropolis algorithm
		# Use Maximum A Posteriori (MAP) optimisation as initial value for MCMC
		start = pymc3.find_MAP()
		# Use the Metropolis algorithm (as opposed to NUTS or HMC, etc.)
		step = pymc3.Metropolis()
		# Calculate the trace
		trace = pymc3.sample(iterations, step, start, random_seed=1, progressbar=True)

	plt.subplot(2,3,1)
	plt.hist(trace["theta0"],bins,histtype="step", density=True,
		label="Posterior (MCMC) Beta", color="red"
	)
	plt.legend(title="Parameters", loc="best")

	plt.subplot(2,3,2)
	plt.hist(trace["theta1"], bins,
		histtype="step", density=True,
		label="Posterior (MCMC) Uniform", color="pink"
	)
	plt.legend(title="Parameters", loc="best")

	plt.subplot(2,3,3)
	plt.hist(
		trace["theta2"], bins,
		histtype="step", density=True,
		label="Posterior (MCMC) Kumaraswamy", color="green"
	)
	plt.legend(title="Parameters", loc="best")

	plt.subplot(2,3,4)
	plt.hist(
		trace["theta3"], bins,
		histtype="step", density=True,
		label="Posterior (MCMC) Logit Normal", color="indigo"
	)
	plt.legend(title="Parameters", loc="best")

	plt.subplot(2,3,5)
	plt.hist(
		trace["theta4"], bins,
		histtype="step", density=True,
		label="Posterior (MCMC) Triangular", color="orange"
	)
	plt.legend(title="Parameters", loc="best")

	plt.show()
