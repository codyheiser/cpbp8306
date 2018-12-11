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


	def pymc3(self, name="theta"):
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


	def pymc3(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Kumaraswamy(name, a=self.a, b=self.b)



class _uniform(distribution):
	def __init__(self):
		distribution.__init__(self)
		self.dist = stats.uniform.pdf(self.x)


	def pymc3(self, name="theta"):
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


	def pymc3(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.Triangular(name, lower=self.lower, upper=self.upper)



class _logitnormal(distribution):
	def __init__(self, m, s):
		distribution.__init__(self)
		self.m = np.round(m, 4)
		self.s = np.round(s, 4)
		self.dist = stats.norm.pdf(logit(self.x), loc=m, scale=s) * 1/(self.x * (1-self.x))


	def pymc3(self, name="theta"):
		'''PyMC3 implementation of distribution'''
		return pymc3.LogitNormal(name, mu=self.m, sd=self.s)



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Bayesian inference testing with Markov Chain Monte Carlo')
	parser.add_argument('iter', help='How many MCMC iterations to run')
	parser.add_argument('n', help='How many total coin flips?')
	parser.add_argument('z', help='How many Heads observed in n coin flips?')
	parser.add_argument('-alg', help='Step method algorithm to use ("Metropolis" or "NUTS")', default='Metropolis')
	args = parser.parse_args()

	# grab parameter values from command line args
	n = int(args.n)
	z = int(args.z)
	iterations = int(args.iter)
	bins=60 # set number of bins for histogram results

	# make list of prior objects
	priors = [_beta(12, 12), _uniform(), _kumaraswamy(2, 2), _logitnormal(0, 0.3), _triangular(0, 1)]
	# make list of labels for plots
	labels = ['Beta','Uniform','Kumaraswamy','Logit-Normal','Triangular']
	# make list of colors for plots
	colors = ['blue','red','green','orange','purple']
	# make list of names for priors
	prior_names = ['theta0','theta1','theta2','theta3','theta4']
	# make list of names for posteriors
	post_names = ['y0','y1','y2','y3','y4']
	# make list of iterators
	iterators = [1, 2, 3, 4, 5]

	# initiate figure for plotting Part A
	plt.figure('Homework 11', figsize=(12,6))

	# iterate through distribution objects and metadata to run MCMC simulations and plot results
	for prior, label, color, prior_name, post_name, iter in zip(priors, labels, colors, prior_names, post_names, iterators):
		# Use PyMC3 to construct a model context
		with pymc3.Model() as basic_model:
			theta = prior.pymc3(prior_name)
			y = pymc3.Binomial(post_name, n=n, p=theta, observed=z)

			start = pymc3.find_MAP()

			if args.alg == 'Metropolis':
				# Use the Metropolis algorithm
				step = pymc3.Metropolis()
			elif args.alg == 'NUTS':
				# use the NUTS algorithm
				step = pymc3.NUTS()
			else:
				raise Exception('Please provide a valid PyMC3 step method ("Metropolis" or "NUTS")')

			# Calculate the trace
			trace = pymc3.sample(iterations, step, start, random_seed=1, progressbar=True)

		# plot prior distribution
		plt.subplot(2,3,iter)
		prior.plot_dist(label='Prior', color=color)
		# plot MCMC posterior histogram
		plt.hist(trace[prior_name], bins, histtype='step', density=True, linewidth=1.2, label='Posterior', color=color)

		plt.title(label)
		plt.xlabel("$\\theta$, Fairness", fontsize=9)
		plt.ylabel("Density", fontsize=9)
		plt.legend(title=None, loc="best", fontsize=9)

	plt.text(1.5, 2, 'n = {}\nz = {}\nIterations = {}'.format(n, z, iterations), fontsize=14)
	plt.tight_layout()
	plt.show()
