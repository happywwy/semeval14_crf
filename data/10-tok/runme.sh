#!/bin/bash

#
# Tokenize text and convert annotation to token-level offsets
#


for F in `cd input; ls *.xml`
do
    cat input/$F | ./scripts/token_annotation.py > ${F}
done
