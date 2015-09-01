#!/bin/bash

#
# Parse with Stanford Parser (parse trees and dependencies)
#

#MODEL=edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz
MODEL=englishPCFG.ser.gz

for F in `cd test_input; ls *.pos`
do
    G=${F%.pos}
    cat input/$F | \
	./scripts/strip_pos.py > ${G}.tmp
    
    java -mx2048m -cp "parser/*:." edu.stanford.nlp.parser.lexparser.LexicalizedParser -tokenized -sentences newline -outputFormat "typedDependencies" ${MODEL} ${G}.tmp > ${G}.parse

    rm ${G}.tmp
done
