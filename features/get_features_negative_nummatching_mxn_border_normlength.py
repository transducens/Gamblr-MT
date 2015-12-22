# -*- coding: utf-8 -*-

###############################################################################
# Script that reads both the source and target segments of a training/testing #
# dataset for word-level quality estimation and compute a collection of NxM   #
# features, being N and M the lengths of the sub-segment in source and target #
# languages, respectively. These are negative features, that is features that #
# indicate that a word needs to be post-edited. The features reperesent the   #
# number of sub-segments that match partially in the translation hypothesis   #
# (for which the first and last words can be matched in the translation       #
# hypothesis) and that do not match for the word w. This value takes into     #
# acount the length of the sub-segment in target language and the distance    #
# between those words matching at the beggining and the end of the            #
# sub-segment.                                                                #
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

def levenshtein(s1, s2):

  it = iter(s2)
  if all(any(c == ch for c in it) for ch in s1):
    return []
  else:

    editions = [[0 for x in range(len(s2)+1)] for x in range(len(s1)+1)]

    previous_row = range(len(s2) + 1)

    insertions=0
    deletions=0
    substitutions=0

    for i, c1 in enumerate(s1):
      current_row = [i + 1]
      for j, c2 in enumerate(s2):
        insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
        deletions = current_row[j] + 1       # than s2
        substitutions = previous_row[j] + (c1 != c2)
        current_row.append(min(insertions, deletions, substitutions))
        if c1 == c2:
          editions[i][j]="E"
        else:
          if insertions < deletions:
            if insertions < substitutions:
              editions[i][j]="I"
            else:
              editions[i][j]="S"
          else:
            if deletions < substitutions:
              editions[i][j]="D"
            else:
              editions[i][j]="S"

      previous_row = current_row

    editionstring=""
    i=len(s1)-1
    j=len(s2)-1
    while i >= 0 and j >= 0:
      if editions[i][j]=="I":
        i-=1
      elif editions[i][j]=="D":
        editionstring+=editions[i][j]
        j-=1
      else:
        editionstring+=editions[i][j]
        i-=1
        j-=1

    while j >= 0:
      editionstring+="D"
      j-=1

    return editionstring[::-1]



oparser = argparse.ArgumentParser(description="Script that reads both the source and target segments of a training/testing dataset for word-level quality estimation and compute a collection of NxM features, being N and M the lengths of the sub-segment in source and target languages, respectively. These are negative features, that is features that indicate that a word needs to be post-edited.")
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
  if field1 not in phrasedic:
    phrasedic[field1]=Set([])
  phrasedic[field1].add(" ".join(PunktWordTokenizer().tokenize(fields[2])).lower())

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
  negative={}

  targetseg=target.decode("utf-8").strip()
  twords=targetseg.split()
  for n in xrange(0,len(twords)):
    features[n]={}

  for sseg in ssegs:
    slen=len(sseg.split())
    if sseg.lower() in phrasedic:
      matchingtsegs=phrasedic[sseg.lower()]
      for seg in matchingtsegs:
        splitseg=seg.lower().split()
        editions=levenshtein(splitseg,twords)
        if editions.count('E') > 1:

          headeds=editions.split("E")[0]
          taileds=editions.split("E")[-1]
          if "S" not in headeds and "S" not in taileds:
            tlen=editions.count('E')
            initpos=editions.find('E')
            lastpos=editions.rfind('E')
            for pos in xrange(initpos+1,lastpos):
              if editions[pos] != "E":
                if pos not in features:
                  features[pos]={}
                if tlen not in features[pos]:
                  features[pos][tlen]={}
                if slen in features[pos][tlen]:
                  features[pos][tlen][slen]+=1.0/(lastpos-initpos)
                else:
                  features[pos][tlen][slen]=1.0/(lastpos-initpos)

  for w in xrange(len(twords)):
    feat_string=""
    for tl in xrange(2,options.maxlen+1):
      if tl in features[w]:
        for sl in xrange(2,options.maxlen+1):
          if sl in features[w][tl]:
            feat_string+=str(features[w][tl][sl])
            feat_string+=","
          else:
            feat_string+="0.0,"
      else:
        for z in xrange(2,options.maxlen+1):
          feat_string+="0.0,"
    print feat_string[:-1]

