#! /bin/bash


###############################################################################
# Author: Miquel Esplà-Gomis [mespla@dlsi.ua.es]                              #
# License: GPLv3 [http://www.gnu.org/licenses/quick-guide-gplv3.en.html]      #
###############################################################################


BASEDIR=$(readlink -f "$(dirname $0)/../..")
METHODNAME=$(basename $(readlink -f $(dirname $0)))

OUTDATADIR=$BASEDIR/data/intermediate/prediction
source $(dirname $0)/heading.sh

#Classifier parameters
#seed value for initialisation of weights
seed=8
#neural network configuration (see parameter -H in http://weka.sourceforge.net/doc.dev/weka/classifiers/functions/MultilayerPerceptron.html)
neur="i"

for langpair in "${langpairs[@]}"; do
    #Languages of the language pair
    lang1=$(echo $langpair | cut -d '-' -f 1)
    lang2=$(echo $langpair | cut -d '-' -f 2)

    #Creating output directory
    mkdir -p $OUTDATADIR/$langpair/${seed}_$neur
    #Classifier
    MODEL_FILE=$MODELSDIR/$langpair/${seed}_$neur/model.cls.obj
    #Test file
    TEST_FILE=$TESTFILESDIR/$langpair/feat.cls$tset.arff

    #Ouput file for the classification
    OUTPUT=$OUTDATADIR/$langpair/${seed}_$neur/wekaout.cls$tset

    #Running the classifier
    java -Xmx2g -cp "$WEKAJAR" weka.classifiers.functions.MultilayerPerceptron -p 0 -T $TEST_FILE -l $MODEL_FILE | tail -n+6 | sed 's/^\s*//g' | sed -r 's/\s+/ /g' | cut -d ' ' -f 3 | cut -d ':' -f 2 > $OUTPUT

    #Adapting the output to the input needed by the evaluation script
    cat $OUTPUT | sed 's/^OK$/GOOD/g' | python $BASEDIR/scripts/individual/rebuild_classification_output.py $INTESTDATADIR/$langpair/test.target | python $BASEDIR/scripts/individual/into_class_format.py | sed 's/^GOOD$/OK/g' > $OUTPUT.txt

    #Evaluation
    python $evalscript $INTESTDATADIR/$langpair/test.tags $OUTPUT.txt

done
