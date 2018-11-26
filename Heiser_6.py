# -*- coding: utf-8 -*-
"""
Heiser_6.py
@author: Cody Heiser


usage: Heiser_6.py [-h] [--truncate] file

Analyze a .txt file containing a DNA sequence

positional arguments:
  file        input filename

optional arguments:
  -h, --help  show this help message and exit
  --truncate  truncate printing of complimentary sequences to reduce console output 


Using DNA sequence from AE1.txt, generates reverse complimentary sequence in both DNA and RNA,
tallies counts of each nucleotide base, and plots base distribution of sequence as a bar graph.
"""

import numpy as np
import matplotlib.pyplot as plt
import argparse


def rev_comp(s, nucleic_acid):
	'''
	Generate reverse compliment to given sequence, s, 
	in desired nucleic acid format (i.e. DNA or RNA).
	Output is reported 3' to 5'.
	'''
	# define base complements
	bases = {
	'A':{'DNA':'T', 'RNA':'U'}, 
	'T':{'DNA':'A', 'RNA':'A'}, 
	'G':{'DNA':'C', 'RNA':'C'}, 
	'C':{'DNA':'G', 'RNA':'G'}
	}
	# return reverse complimentary string (3' - 5')
	return ''.join([bases[x][nucleic_acid] for x in s])[::-1]

def base_metrics(s):
	'''
	Count the appearance of each nucleotide base in a sequence, s, 
	print to console and return as array.
	'''
	metrics = {
	'A':s.count('A'),
	'T':s.count('T'),
	'C':s.count('C'),
	'G':s.count('G')
	}
	print('\nSequence has the following base counts:\n\tA : {}\n\tT : {}\n\tG : {}\n\tC : {}\n'.format(metrics['A'], metrics['T'], metrics['G'], metrics['C']))
	return metrics


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze a .txt file containing a DNA sequence')
    parser.add_argument('file', help='input filename')
    parser.add_argument('--truncate', help='truncate printing of complimentary sequences to reduce console output', action='store_true')
    args = parser.parse_args()


# get sequence data to play with
f = open(args.file, 'r') # open file containing DNA sequence. 'r' = read only
seq = f.read() # read DNA sequence into variable
f.close() # close file after reading


# generate reverse compliment and RNA sequences
if args.truncate: 
	print_len = 81

else:
	print_len = -1

dna_comp = rev_comp(seq, 'DNA')
print("\nSequence's reverse compliment is:\n    {}...".format(dna_comp[:print_len]))
rna_comp = rev_comp(seq, 'RNA')
print("\nSequence's RNA reverse compliment is:\n    {}...".format(rna_comp[:print_len]))


# calculate base diversity metrics for seq
out = base_metrics(seq) 

# plot results
plt.figure('Figure 1')
plt.bar(np.arange(len(out.keys())), out.values(), align = 'center')
plt.xticks(np.arange(len(out.keys())), out.keys())
plt.ylabel('Nucleotide Count (n)') # add y-axis label
plt.title('Sequence Base Diversity') # add plot title
plt.show()
