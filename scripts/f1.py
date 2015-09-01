#!/usr/bin/env python 


"""                                                                                                                                                                                      

Compute F1 measure for sequence tagging

Usage: conll_format.py [-d DELIM] GOLD PREDICTION
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 GOLD        Gold standard file, last column is considered as labels.
 PREDICTION  System prediction, single column of labels.

Options:
 -d DELIM    Column delimiter, default TAB.

"""


from collections import namedtuple

label = namedtuple("label", "start end category")


def read_tags(source, delim):
    last_col = lambda x: x.strip().split(delim)[-1]
    return [map(last_col, block.split("\n")) for block in source.split("\n\n") if block.strip() != '']
    

def extract_labels(tags):
    start, end, category = None, None, None
    for index, tag in (tag for tag in enumerate(tags) if tag[1] != 'O'):
        if tag == 'B' or tag.startswith("B-"):
            if start:
                yield label(start, end, category)
            start = index
            end = index
            if tag.startswith("B-"):
                category = tag[2:]
        elif tag == 'I' or tag.startswith("I-"):
            end = index
    if start:
        yield label(start, end, category)
 

if __name__ == "__main__":
    import sys    
    import getopt

    opts, args = getopt.getopt(sys.argv[1:], "d:")
    delim = "\t"
    for o, v in opts:
        if o == "-d":
            delim = v
        else:
            print >> sys.stderr, "Unknown option : ", o

    assert len(args) == 2

    # read gold labels
    with open(args[0], 'r') as fin:
        gold = list(read_tags(fin.read(), delim))

    # read system predictions
    with open(args[1], 'r') as fin:
        system = list(read_tags(fin.read(), delim))

    # compute necessary statistics
    correct = 0.0
    proposed = 0.0
    actual = 0.0
    assert len(gold) == len(system)
    for gold_tags, system_tags in zip(gold, system):
        gold_labels = set(extract_labels(gold_tags))
        system_labels = set(extract_labels(system_tags))
        correct += len(gold_labels.intersection(system_labels))
        proposed += len(system_labels)
        actual += len(gold_labels)
    
    # compute precision, recall, f1-measure
    p = correct / proposed
    r = correct / actual
    f1 = 2 * p * r / (p + r)
    
    print "Precision   : %.4f" % p
    print "Recall      : %.4f" % r
    print "F1-measure  : %.4f" % f1
