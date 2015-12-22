#! /bin/bash


###############################################################################
# Author: Miquel Esplà-Gomis [mespla@dlsi.ua.es]                              #
# License: GPLv3 [http://www.gnu.org/licenses/quick-guide-gplv3.en.html]      #
###############################################################################


#Base directory
BASEDIR=$(readlink -f "$(dirname $0)/../..")
#Output directory
OUTDATADIR=$BASEDIR/data/intermediate/training

#Loading heading
source $(dirname $0)/heading.sh

for langpair in "${langpairs[@]}"; do
  #Languages of the language pair
  lang1=$(echo $langpair | cut -d '-' -f 1)
  lang2=$(echo $langpair | cut -d '-' -f 2)

  #Creating output directory
  mkdir -p $OUTDATADIR/$langpair/

  featn=0
  rm -f $OUTDATADIR/$langpair/$lang1.*
  for featscript in "${featscripts[@]}"; do
    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $TMTRANSDATADIR/$langpair/$lang1.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1

    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $MTTRANSDATADIR/$langpair/$lang1.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1
  done
  for featscript in "${revfeatscripts[@]}"; do
    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $TMTRANSDATADIR/$langpair/$lang2.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1

    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $MTTRANSDATADIR/$langpair/$lang2.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1
  done
  for featscript in "${contextfeat[@]}"; do
    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $TMTRANSDATADIR/$langpair/$lang1.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1
  done
  for featscript in "${revcontextfeat[@]}"; do
    python $featscript -s $INTRAINDATADIR/$langpair/train.source -t $INTRAINDATADIR/$langpair/train.target -p $TMTRANSDATADIR/$langpair/$lang2.segs.uniq -m $maxlen > $OUTDATADIR/$langpair/$lang1.features$featn
    let featn=$featn+1
  done

  #Creating ARFF file with gold standard tags
  tr ' ' '\n' < $INTRAINDATADIR/$langpair/final_fbk-apet.train-data.target.tags > $OUTDATADIR/$langpair/$lang1.cls
  echo "@relation 'word-level-qe" > $OUTDATADIR/$langpair/feat.cls.arff
  for i in $(seq 1 $nfeat)
  do
    echo "@attribute f$i real" >> $OUTDATADIR/$langpair/feat.cls.arff
  done
  echo "@attribute class {OK,BAD}" >> $OUTDATADIR/$langpair/feat.cls.arff
  echo "@data" >> $OUTDATADIR/$langpair/feat.cls.arff
  paste -d ',' $OUTDATADIR/$langpair/$lang1.features* $OUTDATADIR/$langpair/$lang1.cls$tset >> $OUTDATADIR/$langpair/feat.cls.arff
done
