#!/usr/bin/env python

#
# Strip _POS pos-tag suffix from words in input
#
# Usage: python strip_pos.py < INPUT > OUTPUT
#


import sys


def strip_last(word, delim):
    try:
        return word[:word.rindex(delim)]
    except ValueError:
        return None

f = open('Laptops_Test.pos', 'r').read().splitlines()
outfile = open('Laptops_Test.sent', 'w')

#for line in sys.stdin:
for line in f:
    delim = "_"
    #print ' '.join((strip_last(word, delim) for word in line.split() if strip_last(word, delim)))
    outfile.write(' '.join((strip_last(word, delim) for word in line.split() if strip_last(word, delim))))
    outfile.write('\n')
    
outfile.close()
