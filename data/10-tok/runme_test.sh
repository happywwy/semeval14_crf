#!/bin/bash

#
# Tokenize text and convert annotation to token-level offsets
#


for F in `cd test_input; ls *.xml`
do
    cat input/$F | ./scripts/token_annotation_editID.py > ${F}
done
