# -*- coding: utf-8 -*-

###############################################################################
# Script that reads both the source and target segments of a training/testing #
# dataset for word-level quality estimation and compute a collection of N     #
# features, being N the lengths of the sub-segment in target language. These  #
# are positive features, that is features that indicate that a word does not  #
# need to be post-edited. The features represent how many sub-segments t of   #
# the translation hypothesis with a length l in [1,N] cover the word w (and   #
# are the result of translating a sub-segment from the source language        #
# segment) out of the total number of sub-segments with length l that cover   #
# the word w.                                                                 #
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
sys.setdefaultencoding("utf-8")

oparser = argparse.ArgumentParser(description="Script that reads both the source and target segments of a training/testing dataset for word-level quality estimation and compute a collection of N features, being N the lengths of the sub-segment in target language. These are positive features, that is features that indicate that a word does not need to be post-edited. The features represent how many sub-segments t of the translation hypothesis with a length l in [1,N] cover the word w and their translation is matched in the source language segment out of the total number of sub-segments with length l that cover the word w.")
oparser.add_argument("-s", "--source", help="Document containing the source segments of the wl-QE dataset", dest="source_path", required=True)
oparser.add_argument("-t", "--target", help="Document containing the target (annotated) segments of the wl-QE dataset", dest="target_path", required=True)
oparser.add_argument("-p", "--phrases", help="Document containing the phrases pairs used to align the sub-segments of the wl-QE dataset", dest="phrases_path", required=True)
oparser.add_argument("-m", "--maxlen", help="Maximum length of the sub-segments used", dest="maxlen", type=int, required=True)

options = oparser.parse_args()

phrasedic={}
phrasesreader=open(options.phrases_path, "r")
for phrase in phrasesreader:
  fields=phrase.decode("utf-8").replace(u"¿",u"¿ ").replace(u"¡",u"¡ ").strip().lower().split("\t")
  field1=" ".join(PunktWordTokenizer().tokenize(fields[1]))
  if field1 not in phrasedic:
    #phrasedic[field1]=[]
    phrasedic[field1]=Set([])
  #phrasedic[field1].append(fields[2])
  phrasedic[field1].add(" ".join(PunktWordTokenizer().tokenize(fields[2])))


sourcereader=open(options.source_path, "r")
targetreader=open(options.target_path, "r")

for source, target in izip(sourcereader, targetreader):
  sourceseg=source.decode("utf-8").strip()

  ssegs=[]
  for l in xrange(1,options.maxlen+1):
    words=sourceseg.split()
    for pos in xrange(0,len(words)-l+1):
      ssegs.append(" ".join(words[pos:pos+l]))

  features={}
  tsegs={}

  targetseg=target.decode("utf-8").strip()
  twords=targetseg.split()
  for n in xrange(0,len(twords)):
    features[n]={}

  for l in xrange(1,options.maxlen+1):
    for pos in xrange(0,len(twords)-l+1):
      ts=" ".join(twords[pos:pos+l]).lower()
      if ts not in tsegs:
        tsegs[ts]=Set()
      for p in xrange(pos,pos+l):
        tsegs[ts].add(p)

  for sseg in ssegs:
    slen=len(sseg.split())
    if sseg.lower() in phrasedic:
      matchingtsegs=phrasedic[sseg.lower()]
      for seg in matchingtsegs:
        if seg in tsegs:
          for pos in tsegs[seg]:
            tlen=len(seg.split())
            if tlen in features[pos]:
              features[pos][tlen].add(seg)
            else:
              features[pos][tlen]=Set([])
              features[pos][tlen].add(seg)


  for w in xrange(len(twords)):
    feat_string=""
    for tl in xrange(1,options.maxlen+1):
      leftlimit=(w+1)-tl
      rightlimit=(len(twords)-(w))-tl
      if leftlimit > 0:
        leftlimit=0
      if rightlimit > 0:
        rightlimit=0
      maxcover=tl+leftlimit+rightlimit
      if tl in features[w]:
        feat_string+=str(len(features[w][tl])/float(maxcover))
        feat_string+=","
      else:
        feat_string+="0.0,"
    print feat_string[:-1]
