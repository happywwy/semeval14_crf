#!/bin/bash


#
# Split data sets into training, development, and test set
#

TRAIN=60
DEV=20
#for F in `cd input; ls *.conll`
#for F in `ls *.conll`

F="Restaurants_Train.conll"

#do
G=${F%.conll}
cat ${F} |./scripts/split_data.py --out_train ${G}.train.conll --out_dev ${G}.dev.conll --out_test ${G}.test.conll $TRAIN $DEV < input/${F}
#done

#cat input/${F} |./scripts/split_data.py --out_train ${G}.train.conll --out_dev ${G}.dev.conll --out_test ${G}.test.conll $TRAIN $DEV < input/${F}