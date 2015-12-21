
###############################################################################
# Author: Miquel Esplà-Gomis [mespla@dlsi.ua.es]                              #
# License: GPLv3 [http://www.gnu.org/licenses/quick-guide-gplv3.en.html]      #
###############################################################################

#Scripts that obtian features by using sub-segment pairs obtained by translating from source to target language
featscripts=("$BASEDIR/scripts/individual/get_features_negative_nummatching_mxn_border_normlength.py" "$BASEDIR/scripts/individual/get_features_onedimension_norm.py")
#Scripts that obtian features by using sub-segment pairs obtained by translating from source to target language with occurrence frequency information
contextfeat=("$BASEDIR/scripts/individual/get_features_onedimension_normoccs.py")
#Scripts that obtian features by using sub-segment pairs obtained by translating from target to source language
revcontextfeat=("$BASEDIR/scripts/individual/get_features_reverse_normoccs.py")
#Scripts that obtian features by using sub-segment pairs obtained by translating from target to source language with occurrence frequency information
revfeatscripts=("$BASEDIR/scripts/individual/get_features_reversetrans_norm.py")
#Directory where the training data is stored
INTRAINDATADIR=$BASEDIR/data/input/training
#Directory where the development data is stored
INDEVDATADIR=$BASEDIR/data/input/dev
#Directory where the test data is stored
INTESTDATADIR=$BASEDIR/data/input/test
#Directory where the sub-segment translations obtained with machine translation are stoderd
MTTRANSDATADIR=$BASEDIR/data/intermediate/segs/translations
#Directory where the sub-segment translations obtained with context are stoderd
TMTRANSDATADIR=$BASEDIR/data/intermediate/segs/context
#Directory where the features for the training set are stored
FEATURESDIR=$BASEDIR/data/intermediate/training
#Directory where the features for the development set are stored
FEATURESDEVDIR=$BASEDIR/data/intermediate/dev
#Classpath to use weka (it must include the JAR file of weka and any further aditional packages used sepparated with ":")
WEKAJAR=$BASEDIR/weka/weka-3-7-12/weka.jar:/home/mespla/wekafiles/packages/thresholdSelector/thresholdSelector.jar

#Directory where classification data is stored
MODELSDIR=$BASEDIR/data/intermediate/classmodels
#Test set
TESTFILESDIR=$BASEDIR/data/intermediate/test
#Development set
DEVFILESDIR=$BASEDIR/data/intermediate/dev
#Directory with the gold-standard data
ORIGGOLDFILESDIR=$BASEDIR/data/input/gold
#Evaluation script
evalscript=$BASEDIR/scripts/individual/wmt15_word_level_qe_evaluation.py
#evalscript=$BASEDIR/scripts/individual/evaluate_task2_WMT2014.py

#Maximum length of sub-subsegments
maxlen=$1
#Number of features
nfeat=$(echo "2*(($maxlen-1)*($maxlen-1))+6*$maxlen" | bc)
#Language pairs (this is a list, several language pairs can be specified)
langpairs=("EN-ES")
