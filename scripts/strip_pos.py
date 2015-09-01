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

for line in sys.stdin:
    delim = "_"
    print ' '.join((strip_last(word, delim) for word in line.split() if strip_last(word, delim)))

