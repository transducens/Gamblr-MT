# Gamler-MT

This project is aimed at developing software for estimating the quality in machine translation (MT) at the word level. The method developed is based on the use of sources of bilingual information (SBI) that are obtained by splitting both the source language segment and the translation hypothesis and using any SBI available to translate them in both translation directions. A collection of positive and negative features is obtained for each word, and a multilayer perceptron implemented in the toolkit [Weka](http://weka.sourceforge.net/doc.dev/weka/classifiers/functions/MultilayerPerceptron.html) is then used to estimate their quality. The name of the project refers to a song by Kenny Rogers called "The Gambler"; one of the verses says: "Every gambler knows that the secret to survivin' is knowin' what to throw away and knowin' what to keep".

## Description of the code

The code in this repository is divided in two directories: `features`, `utils` and `wlqe`. The directory `features` contains the collection of scripts to compute the features for the words in a translation hypothesis. The directory `utils` contains additional scripts that perform some formatting on the output of the classifier to adapt it to the evalution script. This evaluation script is not included in this package since its license is not specified; however Finally, the directory `wlke` contains a collection of scripts that ease the task of obtaining word-level quality estimations conduct the task of word-level quality estimation. All these scripts are described in the next sections.

## Features scripts

There are two kinds of feature scripts: those that provide negative evidence, i.e. evidence that a word needs to be post-edited, and those that provide positive evidence, i.e. evidence that a word does not need to be post-edited. The script that generates the negative features is:

* `get_features_negative_nummatching_mxn_border_normlength.py`: This script is based on SBI that translate sub-sgements of the source language segment into the target language. Once this is done, the sub-segment translations are partially matched to the translation hypothesis. Those sub-segments for which the first and last words can be matched are used as a negative evidence. The words in the translation hypothesis in the middle of two words matched with a translated sub-segment are affected by this evidence.

As regards the positive features, two kinds of these features can be obtained: those that compute features using SBI to translate sub-segments of the source language segment into the target language, and those using SBI to translate sub-segments of the translation hypothesis into the source language. 

The features that use translations from source language to target language are:

* `get_features_onedimension_norm.py`: this script computes features that represent the percentage of sub-segments that cover the every word and are the result of translating a sub-segment from the source segment
* `get_features_onedimension_normoccs.py`: this script uses information about the translation frequency, and weights the features obtained by `get_features_onedimension_norm.py` with this freqency.

The two additional scripts compute the equivalent features when using SBI in the inverse translation direction.

* `get_features_reversetrans_norm.py`
* `get_features_reverse_normoccs.py`

All the scripts share the same parameters:
* `-s`: Path to the file containing the source language segments (one per line)
* `-t`: Path to the file containing the translation hypotheses (one per line)
* `-p`: Path to the file containing the pairs of sub-segments obtained by means of SBI
* `-m`: Maximum sub-segment length
 
The file containing the sub-segment pairs contains three fields separated by tabs: the name of the SBI used to obtain the translations, the source language sub-segment and the target language sub-segment. This is a sample of the these kind of files:

```txt
apertium        13 partners building    13 socios que construyen
apertium        14 lies that            14 mentiras que
apertium        15 minutes to show      15 minutos para mostrar
...             ...                     ...
```

When using an SBI that provides information about the translation frequency, it can be added to the field as an additional field:

```txt
apertium        13 partners building    13 socios que construyen       50
apertium        13 partners building    13 socios que hacen            10
apertium        13 partners building    13 compañeros que construyen   5
...             ...                     ...
```
The freqency is normalised for different translations of the same segment. This means that this value can be provided as the number of occurrences of each translation or as a percentage.
