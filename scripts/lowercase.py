#!/usr/bin/env python

#
# Lowercase text
#
# Usage: python lowercase.py < INPUT > OUTPUT
#


import sys


for line in sys.stdin:
    print line.strip().lower()

