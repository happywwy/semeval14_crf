#!/usr/bin/env python


"""
Equivalent like Unix head command but with support for paragraphs

Usage: head.py [-n N] [-f FORMAT] < INPUT > OUTPUT
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 INPUT       input text
 OUTPUT      first N lines or paragraphs of input

OPTIONS:
 -n N        number N of items to be output.
 -f FORMAT   Either 'lines' or 'paragraphs', default is 'lines'.
 """



from util import paragraphs




if __name__ == "__main__":
    import sys
    import getopt


    opts, args = getopt.getopt(sys.argv[1:], "n:f:")
    n = 10
    item_getter = lambda x: x
    item_separator = ''
    assert len(args) == 0
    for o, v in opts:
        if o == "-n":
            n = int(v)
        elif o == '-f':
            if v == 'lines':
                item_getter = lambda x:x
            elif v == 'paragraphs':
                item_getter = paragraphs
                item_separator = "\n"
            else:
                print >> sys.stderr, "Unknown format : ", v
        else:
            print >> sys.stderr, "Unknown option : ", o

    for i in range(n):
        try:
            item = next(item_getter(sys.stdin))
            print item.strip() 
            if i < n-1:
                print item_separator
        except StopIteration:
            # input ended early
            pass

         




