# -*- coding: utf-8 -*-
"""
Created on Thu May 21 22:37:53 2015

@author: wangwenya
"""

## CAUTION: you will most likely have to fiddle around with these functions to
##          get them to do what you want. they are meant to help you get your data
##          into the proper format for QANTA. send me an email if you have any questions
##          miyyer@umd.edu

# - given a text file where each line is a question sentence, use the
#   stanford dependency parser to create a dependency parse tree for each sentence


out_file = open('Restaurants_Test.parsenew', 'w')
"""
out_file_test = open('raw_parses_restest', 'w')
"""
# change these paths to point to your stanford parser.
# make sure to use the lexparser.sh file in this directory instead of the default!

import subprocess

p = subprocess.Popen(["bash","lexparser.sh","Restaurants_Test.sent"], stdout=subprocess.PIPE)
output, err = p.communicate()
"""

p_test = subprocess.Popen(["bash","lexparser.sh","parsedSentence_restest.txt"], stdout=subprocess.PIPE)
output_test, err_test = p_test.communicate()
"""

#parser_out = os.popen("bash lexparser.sh test.txt").readlines()


#print parser_out

for line in output:
    out_file.write(line)
    
out_file.close()
"""

for line in output_test:
    out_file_test.write(line)
    
out_file_test.close()
"""