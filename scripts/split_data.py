#!/usr/bin/env python


"""
Split data set into training, development and test set

Usage: split_data.py [--out_train OUT] [--out_dev OUT] [--out_test OUT] TRAIN DEV < INPUT 
                                                                                                                                                                                         
Arguments:                                                                                                                                                                               
 INPUT           input feature file in CoNLL format
 TRAIN DEV       percentage for training and development respectively. The rest goes to test.

OPTIONS:
 -out_train OUT        output file for training data. Default is 'train'.
 -out_dev OUT          output file for developemnt data. Default is 'dev'.
 -out_test OUT        output file for test data. Default is 'test'.
 """


from util import paragraphs

if __name__ == "__main__":
    import sys
    import getopt

    opts, args = getopt.getopt(sys.argv[1:], "", ["out_train=", "out_dev=", "out_test="])
    train_out = 'train'
    dev_out = 'dev'
    test_out = 'test'
    for o, v in opts:
        if o == "--out_train":
            train_out = v
        elif o == "--out_dev":
            dev_out = v
        elif o == "--out_test":
            test_out = v
        else:
            print >> sys.stderr, "Unknown option : ", o

    assert len(args) == 2

    data = list(paragraphs(sys.stdin))
    total = len(data)
    train_split, dev_split = map(lambda i : int(i) * total / 100, args)
    test_split = total - train_split - dev_split
    data_iter = iter(data)

    for no_instances, output in zip([train_split, dev_split, test_split], [train_out, dev_out, test_out]):
        fout = open(output, 'wb')
        for i in xrange(no_instances):            
            fout.write(next(data_iter) + '\n')
        

        
