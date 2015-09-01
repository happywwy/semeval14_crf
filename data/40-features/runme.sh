#!/bin/bash


#
# Create CoNLL style column format
#

#for F in `cd input_xml; ls *.xml`
F="Restaurants_Train.xml"
#do
G=${F%.xml}
cat ${F} | ./conll_format.py > ${G}.wordnet
#done

#-d ' '
#cat input_xml/${F} | ./scripts/conll_format.py > ${G}.conll