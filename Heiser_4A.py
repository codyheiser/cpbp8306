# -*- coding: utf-8 -*-
"""
HW4A.py - Fits the data in HW4.dat to a straight line
see https://en.wikipedia.org/wiki/Simple_linear_regression
@author: Cody Heiser
"""
import numpy as np
import matplotlib.pyplot as plt

# Import from the file 'HW4.dat'
vec1 = np.loadtxt('HW4.dat')  # This is an 11x2 array

# calculate sums
Sx, Sy = vec1.sum(axis=0) 

# calculate sums of squares
Sxx, Syy = (vec1**2).sum(axis=0) 
Sxy = vec1.prod(axis=1).sum(axis=0)

# Calculate parameters
n = vec1.shape[0] # get length of array (number of x and y)
Slope = (n*Sxy - Sx*Sy)/(n*Sxx - Sx**2) # calculate slope of best-fit
Inter = (Sy - Slope*Sx)/n # calculate intercept of best-fit

# calculate uncertainties
s2e = (1/(n*(n-2)))*(n*Syy - Sy**2 - (n*Sxx - Sx**2)*Slope**2)
s2Slope = n*s2e/(n*Sxx - Sx**2)
s2Inter = s2Slope*Sxx/n

# print regression stats to the console
print('The data has a best-fit regression with a slope of {:.5} +/- {:.5}, and a y-intercept of {:.5} +/- {:.5}'.format(Slope, s2Slope, Inter, s2Inter))

# generate best-fit line for plotting
Xfit = np.linspace(1.4,1.9,num=25)
Yfit = Inter + Slope*Xfit 

# plot results
fig = plt.figure() # initiate figure object
plt.plot(vec1[:,0],vec1[:,1],'bo',Xfit,Yfit,'r-') # define x, y, and what they look like
plt.xlabel('Independent Variable (x)') # add x-axis label
plt.ylabel('Dependent Variable (y)') # add y-axis label
plt.title('HW4A Linear Regression') # add plot title
plt.legend(['Raw data','Linear Regression'], loc=4) # add legend for points and best-fit line
plt.annotate(xy=[1.4,70], s='y = {:.5}*x + {:.5}'.format(Slope, Inter)) # add regression metrics to plot area
plt.show() # print figure to window
