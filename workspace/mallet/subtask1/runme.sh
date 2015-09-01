#!/bin/bash

#
# CRF sequence tagging model for subtask 1 (aspect term extraction)
#

THREADS=16
#GRMM="/home/i073941/software/ml/mallet/grmm-0.1.3"
GRMM="/Users/wangwenya/Downloads/semevall2014_task4_sap/workspace/mallet/subtask1/grmm-0.1.3"

#for F in `cd input; ls *Train.train.conll`
#F="Restaurants_Train.train.conll"
F="Restaurants_Train.wordnet"
#do

#G=${F%.train.conll}
G="Restaurants_Test.wordnet"
    
    # train model
java -cp $GRMM/class:$GRMM/lib/mallet-deps.jar:$GRMM/lib/grmm-deps.jar \
edu.umass.cs.mallet.grmm.learning.GenericAcrfTui \
--training input/${F} \
--testing input/${G} > input/result_Restaurants.txt \
--model-file tmpls.txt > stdout_Restaurants_wordnet.txt 2> stderr_Restaurants_wordnet.txt
#done
    # test model
    # remove labels (last column)
    #  cat input/${G}.test.grmm | ./scripts/strip_last_column.py -d ' ' > $G.input
    #java -cp  "mallet/class:mallet/lib/mallet-deps.jar" cc.mallet.fst.SimpleTagger --threads ${THREADS} --viterbi-output false  --model-file ${G}.model ${G}.input > ${G}.predict
    
	#java -cp $GRMM/class:$GRMM/lib/mallet-deps.jar:$GRMM/lib/grmm-deps.jar \
    #edu.umass.cs.mallet.grmm.learning.GenericAcrfTui \ 
	#--testing  input/{G}.input tmpls.txt > ${G}.predict 2> stderr.txt
    #--model-file ${G}.model
	
	# evaluate
    #./scripts/f1.py -d ' ' input/${G}.test.conll ${G}.predict | tee ${G}.f1

#edu.umass.cs.mallet.grmm.learning.GenericAcrfTui
#cc.mallet.grmm.learning.GenericAcrfTui
#java -cp $GRMM/class:$GRMM/lib/mallet-deps.jar:$GRMM/lib/grmm-deps.jar

#--testing input/${G}.test.conll > input/result_Restaurants.txt
