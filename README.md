# Gamler-MT

This project is aimed at developing software for estimating the quality in machine translation (MT) at the word level. The method developed is based on the use of sources of bilingual information (SBI) that are obtained by splitting both the source language segment and the translation hypothesis and using any SBI available to translate them in both translation directions. A collection of positive and negative features is obtained for each word, and a multilayer perceptron inplemented in the toolkit [Weka](http://weka.sourceforge.net/doc.dev/weka/classifiers/functions/MultilayerPerceptron.html) is then used to estimate their quality. The name of the project refers to a song by Kenny Rogers called "The Gambler"; one of the verses says: "Every gambler knows that the secret to survivin' is knowin' what to throw away and knowin' what to keep".

## Description of the code

The code in this repository is divided in two directories: `features`, `utils` and `wlqe`. The directory `features` contains the collection of scripts to compute the features for the words in a translation hypotheisis. The directory `utils` contains additional scripts that perform some formatting on the output of the classifier to adapt it to the evalution script. This evaluation script is not included in this package since its license is not specified; however Finally, the directory `wlke` contains a collection of scripts that ease the task of obtaining word-level quality estimations conduct the task of word-level quality estimation. All these scripts are described in the next sections.

## Features scripts

There are two kinds of feature scripts: those that compute features using SBI to translate sub-segments of the source language segment into the target language, and those using SBI to translate sub-segments of the translation hypothesis into the source language. 
