#!/usr/bin/env python

"""
Strip last column of CoNLL style feature file

Usage: python strip_last_column.py [-d DELIM] < INPUT > OUTPUT

Arguments:                                                                                                                                                                               
 INPUT       Tokenized CoNLL-style column file
 OUTPUT      Output with last column removed

Options:
 -d DELIM    Column delimiter, default TAB.
"""


import sys
import getopt

opts, args = getopt.getopt(sys.argv[1:], "d:")
delim = "\t"
assert len(args) == 0
for o, v in opts:
    if o == "-d":
        delim = v
    else:
        print >> sys.stderr, "Unknown option : ", o

for line in sys.stdin:
    print delim.join(line.strip().split(delim)[:-1])

