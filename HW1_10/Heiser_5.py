# -*- coding: utf-8 -*-
"""
Heiser_5.py - Uses function to create array of i**2 - j**2 integers
@author: Cody Heiser

From command line, run: 
	python Heiser_5.py

You will be prompted for dimensions of an array, i and j, which should be integers between 1 and 5. 
If either value does not meet these criteria, a warning message will be printed to the console.
The function will return an i by j array where each element has a value of i**2 - j**2.
"""

import numpy as np 

def check_value(x, xmin, xmax):
	"""
	determine whether value falls within correct range
	x = value to test
	xmin = minimum integer value x can be
	xmax = maximum integer value x can be
	"""
	if x in range(xmin, xmax+1):
		return True

	else:
		return False


def gen_value(x, y):
	"""
	given two values x and y, return the difference of their squares
	"""
	return x**2 - y**2


def build_table(i,j):
	"""
	given the number of rows, i, and columns, j, build a matrix where each value is i**2 - j**2
	both values i and j must be integers between 1 and 5
	"""
	if check_value(i, 1, 5) and check_value(j, 1, 5):
		# if i and j are both good, proceed

		# initiate array of zeros with desired dimensions
		out = np.zeros((i,j)) 

		# iterate through rows and columns and add values to array
		for row in range(i):
			for column in range(j):
				# replace each element at i,j with the appropriate value
				# use row+1 and column+1 to avoid using 0 for first element 
				out[row, column] = gen_value(row+1, column+1)

		# return the array after all values have been calculated
		return out

	else:
		# if i and j don't meet criteria, exit and alert user
		return '\ni and j must be integers between 1 and 5'


# get dimensions from terminal
i = int(input('Provide desired dimensions of table:\ni = '))
j = int(input('j = '))


# run the program and print results to the console
print(build_table(i,j))

