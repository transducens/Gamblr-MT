# -*- coding: utf-8 -*-

###############################################################################
# Script that reads both the source and target segments of a training/testing #
# dataset for word-level quality estimation and compute a collection of N     #
# features, being N the lengths of the sub-segment in target language. These  #
# are positive features, that is features that indicate that a word does not  #
# need to be post-edited. These features use the target-to-source translation #
# frequency when it is available. The features represent the fraction of      #
# translation freqency that corresponds to the sub-segments in of translation #
# hypothesisthat cover teh word w and their translation is totally matched in #
# the source language segment.                                                #
#                                                                             #
# Author: Miquel Esplà-Gomis [mespla@dlsi.ua.es]                              #
# License: GPLv3 [http://www.gnu.org/licenses/quick-guide-gplv3.en.html]      #
###############################################################################

import sys
from nltk.tokenize.punkt import PunktWordTokenizer
import argparse
from sets import Set
from itertools import izip

reload(sys)
sys.setdefaultencoding("UTF-8")

oparser = argparse.ArgumentParser(description="Script that reads both the source and target segments of a training/testing dataset for word-level quality estimation and compute a collection of N features, being N the lengths of the sub-segment in target language. These are positive features, that is features that indicate that a word does not need to be post-edited. These features use the target-to-source translation frequency when it is available. The features represent the fraction of translation freqency that corresponds to the sub-segments in of translation hypothesis that cover teh word w and their translation is totally matched in the source language segment.")
oparser.add_argument("-s", "--source", help="Document containing the source segments of the wl-QE dataset", dest="source_path", required=True)
oparser.add_argument("-t", "--target", help="Document containing the target (annotated) segments of the wl-QE dataset", dest="target_path", required=True)
oparser.add_argument("-p", "--phrases", help="Document containing the phrases pairs used to align the sub-segments of the wl-QE dataset", dest="phrases_path", required=True)
oparser.add_argument("-m", "--maxlen", help="Maximum length of the sub-segments used", dest="maxlen", type=int, required=True)

options = oparser.parse_args()

phrasedic={}
phrasesreader=open(options.phrases_path, "r")
for phrase in phrasesreader:
  fields=phrase.decode("utf-8").lower().strip().split("\t")
  field1=" ".join(PunktWordTokenizer().tokenize(fields[1]))
  #if field1 == "de noruega":
  #  print fields
  if field1 not in phrasedic:
    #phrasedic[field1]=[]
    phrasedic[field1]={}
    phrasedic[field1][" ".join(PunktWordTokenizer().tokenize(fields[2]))]=fields[3]
  else:
    #phrasedic[field1].append(fields[2])
    phrasedic[field1][" ".join(PunktWordTokenizer().tokenize(fields[2]))]=fields[3]

sourcereader=open(options.source_path, "r")
targetreader=open(options.target_path, "r")

for source, target in izip(sourcereader, targetreader):
  sourceseg=source.decode("utf-8").strip()

  ssegs=[]
  for l in xrange(1,options.maxlen+1):
    words=sourceseg.split()
    for pos in xrange(0,len(words)-l+1):
      ssegs.append(" ".join(words[pos:pos+l]))

  features2={}
  tsegs={}

  targetseg=target.decode("utf-8").strip()
  twords=targetseg.split()
  for n in xrange(0,len(twords)):
    features2[n]={}

  for l in xrange(1,options.maxlen+1):
    for pos in xrange(0,len(twords)-l+1):
      ts=" ".join(twords[pos:pos+l]).lower()
      if ts not in tsegs:
        tsegs[ts]=Set()
      for p in xrange(pos,pos+l):
        tsegs[ts].add(p)

  for tseg in tsegs:
    tlen=len(tseg.split())
    #print tseg.lower()

    if tseg.lower() in phrasedic:
      matchingtsegs=phrasedic[tseg.lower()]
      #print "*****"+tseg+u"\t"+str(matchingtsegs)

      total=0
      for val in matchingtsegs.values():
        total+=int(val)
      #print matchingtsegs
      for seg in matchingtsegs:
        if seg in ssegs:
          for pos in tsegs[tseg]:
            #print twords[pos]+" -pos> "+tseg+" -> "+seg+" -> "+" ".join(twords)
            if tlen not in features2[pos]:
              features2[pos][tlen]=0
            features2[pos][tlen]+=float(matchingtsegs[seg])/total

  for w in xrange(len(twords)):
    feat_string=""
    for tl in xrange(1,options.maxlen+1):
      if tl in features2[w]:
        feat_string+=str(features2[w][tl])
        feat_string+=","
      else:
        feat_string+="0.0,"
    #print tdata[w]+"\t"+feat_string[:-1]
    print feat_string[:-1]
