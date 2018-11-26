# -*- coding: utf-8 -*-
"""
HW4B.py - Uses a Monte Carlo approach to test Central Limit Theorem
@author: Cody Heiser

From command line, run: 
	python Heiser_4B.py

You will be prompted to enter a number of 'experiments' to perform by picking random values from a uniform distribution.
Then, you will be prompted for the number of values to pick per experiment. 

A plot will be generated showing the density distribution of the original data, which should be flat, or uniformly-distributed.
Then, the sum of each 'experiment' will be taken and plotted in another density distribution, with an overlay of a true Gaussian 
curve that has the same mean and SD as the population of sums.

As the number of samples per experiment and total number of experiments are increased, the resulting distribution should 
approach a true Gaussian, demonstrating the Central Limit Theorem.
"""
import numpy as np
import matplotlib.pyplot as plt

# get number of random samples to take from terminal
Nexperiments = int(input('How many experiments?: '))

# get desired number of values to take per sample from terminal
nsamples = int(input('\nHow many values per sample?: '))

# generate uniform random numbers and adjust so mean is zero
data = np.random.rand(Nexperiments,nsamples) - 0.5 

# convert matrix of data to a 1-D vector for initial histogram 
# should be a uniform distribution
plt.figure('Figure 1')
plt.hist(np.reshape(data,np.size(data)),density=True,bins=100)
plt.xlabel('Random Samples from Uniform Dist.') # add x-axis label
plt.ylabel('Probability Density') # add y-axis label
plt.title('HW4B Central Limit Theorem - Random Samples') # add plot title

# sum data along nsamples 
sums = data.sum(axis=1)

# generate Gaussian to overlay on results of random sample sums
vr = sums.var(ddof=1) # define standard deviation based on sample sums
me = sums.mean() # define mean based on sample sums
x = np.linspace(sums.min(),sums.max(),num=100) # generate evenly-spaced numbers between 0 and 1 to build Gaussian
y = (1./np.sqrt(2*np.pi*vr))*np.exp(-(x-me)**2/(2*vr)) # calculate y values for Gaussian using above parameters

# create histogram of sums
# as nsamples increases the distribution should approach a Gaussian
plt.figure('Figure 2')
plt.hist(sums,density=True,color = [0.2,0.8,0],bins=100) 
plt.plot(x,y,'r-')
plt.xlabel('Sum of Random Samples from Uniform Dist.') # add x-axis label
plt.ylabel('Probability Density') # add y-axis label
plt.title('HW4B Central Limit Theorem - Sample Sums') # add plot title
plt.legend(['Sum of Random Samples','Normal Distribution'], loc=2) # add legend for points and best-fit line

# show both figures in new windows
plt.show()
