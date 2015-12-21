#! /bin/bash


###############################################################################
# Author: Miquel Esplà-Gomis [mespla@dlsi.ua.es]                              #
# License: GPLv3 [http://www.gnu.org/licenses/quick-guide-gplv3.en.html]      #
###############################################################################


BASEDIR=$(readlink -f "$(dirname $0)/../..")
OUTDATADIR=$BASEDIR/data/intermediate/classmodels

source $(dirname $0)/heading.sh

#Classifier parameters
#seed value for initialisation of weights
seed=8
#neural network configuration (see parameter -H in http://weka.sourceforge.net/doc.dev/weka/classifiers/functions/MultilayerPerceptron.html)
neur="i"
#learning rate
lr="0.1"
#momentum
mom="0.03"

for langpair in "${langpairs[@]}"; do
  #Creating output directory
  mkdir -p $OUTDATADIR/$langpair/${seed}_${neur}
  #Output file
  OUTPUT=$OUTDATADIR/$langpair/${seed}_${neur}/model.cls.prec.obj
  #Features for training and  development
  FEATURES_FILE=$FEATURESDIR/$langpair/feat.cls.arff
  FEATURESDEV_FILE=$FEATURESDEVDIR/$langpair/feat.cls.arff
  #Running weka
  java -Xmx2g -cp "$WEKAJAR" weka.classifiers.meta.ThresholdSelector -t $FEATURES_FILE -d $OUTPUT -v -no-cv -C 3 -X 3 -E 2 -R 0 -M PRECISION -S $seed -W weka.classifiers.functions.MultilayerPerceptron -- -L $lr -M $mom -N 0 -V 10 -S $seed -E 20 -H $neur -C -I -D &
done
