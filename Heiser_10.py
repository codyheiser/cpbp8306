# -*- coding: utf-8 -*-
"""
Heiser_10.py
@author: Cody Heiser


usage: Heiser_10.py [-h]

optional arguments:
  -h, --help  show this help message and exit

"""
import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style("white")


class distribution:
	def __init__(self):
		self.x = np.linspace(0, 1, 100) # generate independent variables in range [0, 1]
		self.dist = self.x # initiate distribution attribute with x values as placeholder


class _beta(distribution):
	def __init__(self, a, b):
		distribution.__init__(self) # _beta class inherits from distribution class
		self.a = a
		self.b = b
		self.dist = stats.beta.pdf(self.x, self.a, self.b) # generate beta probability density function given x, alpha, beta

	def to_gauss(self):
		'''return gaussian distribution for corresponding alpha and beta values'''
		mu = self.a/(self.a + self.b)
		sigma = np.sqrt((self.a*self.b)/(((self.a + self.b)**2)*(self.a + self.b + 1)))
		return np.round(mu,3), np.round(sigma,3), stats.norm.pdf(self.x, mu, sigma) # return gaussian probability density function given x, alpha, beta


class _gauss(distribution):
	def __init__(self, m, s):
		distribution.__init__(self) # _gauss class inherits from distribution class
		self.m = m
		self.s = s
		self.dist = stats.norm.pdf(self.x, self.m, self.s) # generate gaussian probability density function given x, mu, sigma

	def to_beta(self):
		'''return beta distribution for corresponding mu and sigma values'''
		a = (self.m**2)*(((1-self.m)/(self.s**2))-(1/self.m))
		b = a*(1/self.m - 1)
		return np.round(a,3), np.round(b,3), stats.beta.pdf(self.x, a, b) # return beta probability density function given x, mu, sigma



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Bayesian Inference')
	parser.add_argument('-A', help='Show Part A of homework 10', action='store_true') # flag to show A
	parser.add_argument('-B', help='Show Part B of homework 10', action='store_true') # flag to show B
	args = parser.parse_args()

	if args.A and args.B: # if both flags are up, switch off to show both plots
		args.A=False
		args.B=False

	if not args.B: # if only A flag is up, show plot for part A
		# Part A #
		# define sets of alpha and beta values for plotting
		params = [
		(1, 1, 'blue'),
		(5, 5, 'red'),
		(25, 25, 'green'),
		(3, 1, 'magenta'),
		(30, 10, 'orange'),
		(75, 25, 'purple')
		]

		plt.figure('Part A', figsize=(8,6)) # create figure for Part A

		# loop through alpha and beta parameter pairs and plot Beta distribution and corresponding Gaussian distribution
		for p in params:
			d = _beta(p[0],p[1]) # generate Beta distribution
			# plot Beta distribution
			plt.plot(d.x, d.dist, '-', c=p[2], label="$\\alpha={}$, $\\beta={}$".format(d.a, d.b))
			# plot Gaussian generated from Beta parameters
			plt.plot(d.x, d.to_gauss()[2], '--', c=p[2], label="$\\mu={}$, $\\sigma={}$".format(d.to_gauss()[0], d.to_gauss()[1]))

		plt.title("Influence of $\\alpha$ and $\\beta$ on Beta Distribution", loc='left')
		plt.xlabel("$\\theta$, Fairness")
		plt.ylabel("Density")
		plt.legend(title="Parameters", loc='best')

	if not args.A: # if only B flag is up, show plot for part B
		# Part B #
		# define sets of mu and sigma parameters for Bayesian priors
		priors = [
		(0.5, np.round(np.sqrt(1/12),3), 'blue'),
		(0.5, 0.1, 'red'),
		(0.75, 0.1, 'green')
		]

		plt.figure('Part B', figsize=(8,6)) # create figure for Part B

		# loop through mu and sigma parameter pairs and plot Bayesian priors and posteriors
		for p in priors:
			d1 = _gauss(p[0], p[1]) # generate Gaussian distribution given mu and sigma
			d2 = d1.to_beta() # get Beta distribution from Gaussian object
			# plot prior Beta distribution generated from Gaussian parameters
			plt.plot(d1.x, d2[2], '--', c=p[2], label="Prior $\\alpha={}$, $\\beta={}$".format(d2[0], d2[1]))
			
			d3 = _beta(d2[0]+50, d2[1]+50) # create posterior beta distribution following 50 heads and 50 tails observations
			F = d3.dist*np.nan_to_num(d2[2]) # multiply posterior by prior
			F_norm = F/np.trapz(F, x=d3.x) # normalize F for plotting
			# plot posterior Beta distribution
			plt.plot(d3.x, F_norm, '-', c=p[2], label="Posterior $\\alpha={}$, $\\beta={}$".format(d3.a, d3.b))

		plt.title("P($\\theta$|D) Following 50 Observations of Heads and Tails with Given Priors", loc='left')
		plt.xlabel("Probability of Heads")
		plt.ylabel("Density")
		plt.legend(title="Parameters", loc='best')

	plt.show() # show the plots
