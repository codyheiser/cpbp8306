"""
CPBP8306 - Data Analysis for the Biomedical Sciences
Homework 2
Cody Heiser
"""
import numpy as np # load Numpy package
from matplotlib import pyplot as plt # load matplotlib

# define function to convert F to C
def FtoC(tempF):
	'''
	Function to convert temperature in F (tempF) to Celsius
	'''
	return np.round_((tempF - 32)*5/9, decimals=2)


tempdataF = np.genfromtxt('temperature.dat') # using Numpy, read in the data file as an array

tempdataC = [FtoC(x) for x in tempdataF] # convert values from tempdataF to Celsius and write to another np.array

# print mean and variance of Celsius measurements to console:
temp_mean = np.round_(np.mean(tempdataC),2)
temp_var = np.round_(np.var(tempdataC),2)
print('The average temperature in Celsius is '+str(temp_mean)+', with a variance of '+str(temp_var))

plt.hist(tempdataC) # initiate a matplotlib histogram plot object 
plt.xlabel('Temperature (C)') # add x axis label
plt.ylabel('Density (n)') # add y axis label
plt.show() # print plot to window

# Sample mean represents the average of all observed values in a data set.

# Sample variance represents the average of the squared differences of each observed value in a data set from 
#   the mean of that data set.

# Variance of the mean is represented by the standard deviation, or square root of sample variance, 
#   divided by the square root of the number of values in the data set.
print('The variance of the mean for these Celsius measurements is '+str(np.round_(np.sqrt(temp_var)/np.sqrt(len(tempdataC)), 3)))

