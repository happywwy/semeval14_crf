#!/bin/bash


#
# Create CoNLL style column format
#

#for F in `cd input_xml; ls *.xml`
F="Restaurants_Test.xml"
#do
G=${F%.xml}
cat ${F} | ./conll_test.py > ${G}.conll
#done

#-d ' '
#cat input_xml/${F} | ./scripts/conll_format.py > ${G}.conll