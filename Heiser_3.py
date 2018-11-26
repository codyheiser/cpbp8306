"""
CPBP8306 - Data Analysis for the Biomedical Sciences
Homework 3
Cody Heiser

# 1-5
From command line, run: 
	python Heiser_3.py

You will be prompted to enter a total number of values to generate a Normally-distributed population.  Pick a large number.
Then, you will take m samples of n values from that population with the following two prompts. 

Results will report the average of the means of each sample, and the average variances and standard deviations calculated 
with both DoF==1 (N-1 denominator) and DoF==0 (N denominator).

The mean of the population should be 0 and the variance should be 1. As you increase n and m, the variance and SD with 
DoF==0 becomes a better approximation of the true variance, but DoF==1 is always more representative of the true distribution, 
especially at small n.

# Bonus
If drawing numbers from a distribution that is not Normal, the above findings hold true, because as the number of values per
sample and number of samplings get infinitely large, the sample means will be Normally-distributed around the population mean
and the sample variances/SDs will approach true approximations of the population variance/SD.
"""

import numpy as np
import matplotlib.pyplot as plt

def sample_mean_var(x, size):
    '''
    Returns average of means and variances (with ddof==0 and ddof==1) 
    of m random samples of n values from population x.
    
    x = array of population to sample from
    size = size of sample to take. can be array dimensions (n,m) where n is number of
        values per sample and m is number of samples to take.
    '''
    samp = np.random.choice(x, size, replace = False)
    
    plt.figure(2)
    plt.hist(samp, bins = 10)
    plt.title('Distribution of Population Samples')
    
    means = np.mean(samp, axis=0)
    vars_dof1 = np.var(samp, axis=0, ddof=1)
    sd_dof1 = np.sqrt(vars_dof1)
    vars_dof0 = np.var(samp, axis=0)
    sd_dof0 = np.sqrt(vars_dof0)
    
    print('\nAverage sample mean: '+str(np.mean(means)))
    print('Average sample variance with DoF==1: '+str(np.mean(vars_dof1)))
    print('Average sample SD with DoF==1: '+str(np.mean(sd_dof1)))
    print('Average sample variance with DoF==0: '+str(np.mean(vars_dof0)))
    print('Average sample SD with DoF==0: '+str(np.mean(sd_dof0)))
    plt.show()


# get total number of normally-distributed values 
tot = int(input('How many total values in population? (>1000): '))

# get desired number of values to take per sample
n1 = int(input('\nHow many values per sample?: '))

# get desired number of samples to take
n2 = int(input('\nHow many samples?: '))

# generate population
pop = np.random.randn(tot)
# plot histogram of total population
plt.figure(1)
plt.hist(pop, bins = int(tot/50))
plt.title('Distribution of Total Population ('+str(tot)+' values)')

# perform function with inputs
sample_mean_var(pop, (n1,n2))
