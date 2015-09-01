#!/bin/bash

#
# Extract text and perform tokenization and POS tagging
#

MODEL=english-bidirectional-distsim.tagger
#MODEL=english-left3words-distsim.tagger

for F in `cd test_input; ls *.xml`
do
    G=${F%.xml}
    cat input/$F | \
	./scripts/parse_xml.py > ${G}.tmp
    
    java -mx2048m -classpath stanford-postagger.jar edu.stanford.nlp.tagger.maxent.MaxentTagger -tokenize false -model models/${MODEL} -textFile ${G}.tmp > ${G}.pos
    rm ${G}.tmp
done
