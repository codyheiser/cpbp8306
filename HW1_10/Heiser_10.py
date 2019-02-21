# -*- coding: utf-8 -*-
"""
Heiser_10.py
@author: Cody Heiser


usage: Heiser_10.py [-h] [-H HEADS] [-T TAILS] [-A] [-B]

Bayesian Inference Testing

optional arguments:
  -h, --help            show this help message and exit
  -H HEADS, --Heads HEADS
                        How many Heads observed to update posterior for Part B?
  -T TAILS, --Tails TAILS
                        How many Tails observed to update posterior for Part B?
  -A                    Show Part A of homework 10
  -B                    Show Part B of homework 10

"""
import argparse
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns; sns.set_style("white")


class distribution:
	def __init__(self):
		self.x = np.linspace(0, 1, 200) # generate 200 independent, linearly-spaced variables in range [0, 1]
		self.dist = self.x # initiate distribution attribute with x values as placeholder


class _beta(distribution):
	def __init__(self, a, b):
		distribution.__init__(self) # _beta class inherits from distribution class
		self.a = np.round(a, 4)
		self.b = np.round(b, 4)
		self.dist = stats.beta.pdf(self.x, self.a, self.b) # generate beta probability density function given x, alpha, beta

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


class _gauss(distribution):
	def __init__(self, m, s):
		distribution.__init__(self) # _gauss class inherits from distribution class
		self.m = np.round(m, 4)
		self.s = np.round(s, 4)
		self.dist = stats.norm.pdf(self.x, self.m, self.s) # generate gaussian probability density function given x, mu, sigma

	def to_beta(self):
		'''return beta distribution for corresponding mu and sigma values'''
		alpha = (self.m**2)*(((1-self.m)/(self.s**2))-(1/self.m))
		beta = alpha*(1/self.m - 1)
		return _beta(alpha, beta) # return beta probability density function given x, mu, sigma



if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Bayesian Inference')
	parser.add_argument('-H', '--Heads', help='How many Heads observed in 100 coin flips for Part B?', default=50)
	parser.add_argument('-T', '--Tails', help='How many Tails observed in 100 coin flips for Part B?', default=50)
	parser.add_argument('-A', help='Show Part A of homework 10', action='store_true') # flag to show A
	parser.add_argument('-B', help='Show Part B of homework 10', action='store_true') # flag to show B
	args = parser.parse_args()

	if args.A and args.B: # if both flags are up, switch off to show both plots
		args.A=False
		args.B=False


	if not args.B: # if only A flag is up, show plot for part A
		# Part A #
		'''
		For distributions with less variability, the Gaussian very closely approximates the Beta distribution. 
		With wider distributions, the two strategies are further apart from one another.
		'''
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
			d0 = _beta(p[0],p[1]) # generate Beta distribution
			d1 = d0.to_gauss() # generate Gaussian distribution from Beta distribution
			# plot Beta distribution
			plt.plot(d0.x, d0.dist, '-', c=p[2], label="$\\alpha={}$, $\\beta={}$".format(d0.a, d0.b))
			# plot Gaussian generated from Beta parameters
			plt.plot(d1.x, d1.dist, '--', c=p[2], label="$\\mu={}$, $\\sigma={}$".format(d1.m, d1.s))

		plt.title("Influence of $\\alpha$ and $\\beta$ on Beta Distribution", loc='left')
		plt.xlabel("$\\theta$, Fairness")
		plt.ylabel("Density")
		plt.legend(title="Parameters", loc='best')


	if not args.A: # if only B flag is up, show plot for part B
		# Part B #
		'''
		The Bayesian prior has little effect on the posterior when you give it enough data.
		For example, after 100 coin flips with 50 heads and 50 tails, all beta distributions look roughly
		the same regardless of their priors. As you increase observations, the posterior distributions 
		will converge to a consensus based on the data, with little effect from the prior assumption distribution.
		'''
		# define sets of mu and sigma parameters for Bayesian priors
		priors = [
		(0.5, np.round(np.sqrt(1/12),3), 'blue'),
		(0.5, 0.1, 'red'),
		(0.75, 0.1, 'green')
		]

		plt.figure('Part B', figsize=(8,6)) # create figure for Part B

		# loop through mu and sigma parameter pairs and plot Bayesian priors and posteriors
		for p in priors:
			d0 = _gauss(p[0], p[1]) # generate Gaussian distribution given mu and sigma
			d1 = d0.to_beta() # get Beta distribution from Gaussian object
			# plot prior Beta distribution generated from Gaussian parameters
			plt.plot(d1.x, d1.dist, '--', c=p[2], label="Prior $\\alpha={}$, $\\beta={}$".format(d1.a, d1.b))
			
			# create posterior beta distribution following n_heads and n_tails observations
			d2 = d1.calc_posterior(n_heads=int(args.Heads), n_tails=int(args.Tails))
			# plot posterior Beta distribution
			plt.plot(d1.x, d2, '-', c=p[2], label="Posterior $\\alpha={}$, $\\beta={}$".format(int(args.Heads) + 1, int(args.Tails) + 1))

		plt.title("P($\\theta$|D) Following {} Heads and {} Tails with Given Priors".format(args.Heads, args.Tails), loc='left')
		plt.xlabel("Probability of Heads")
		plt.ylabel("Density")
		plt.legend(title="Parameters", loc='best')

	plt.show() # show the plots
