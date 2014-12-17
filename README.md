aeiouado_g2p
============

##Overview
**aeiouado_g2p** is a grapheme-to-phoneme converter for Brazilian Portuguese, based on the dialect of São Paulo (city). It was designed primarily for Speech Technologies, such as Automatic Speech Recognition Systems and Speech Synthesizers. However, it may also be used by linguists, speech therapists, lexicographers, students of Brazilian Portuguese as a second language, and whoever is interested in the sound structure of Brazilian Portuguese.

##Technical Information
**aeiouado_g2p** makes use of a hybrid approach for converting graphemes into phonemes, which takes advantage of both manual transcription rules and machine learning algorithms. The transcription task is carried out in a two-step process: 

1. Words are submitted to a set of transcription rules, in which predictable graphemes (mostly consonants) are transcribed; 
2. a machine learning classifier is used to predict the transcription of the remaining graphemes (mostly vowels). 

The classifier employs a Decision Tree to decide, given a certain grapheme, which phone should be transcribed. The method was evaluated through 5-fold cross-validation; results showed a F1-score of 0.98.

##Usage


##How to cite
If you are using **aeiouado_g2p** in a scientific paper, we would appreciate if you could cite the paper:

>Gustavo Mendonca, Sandra Aluisio (2014). Using a hybrid approach to build a pronunciation dictionary for Brazilian Portuguese. To appear in: Proceedings INTERSPEECH 2014, 15th Annual Conference of the International Speech Communication Association. ISCA. Singapure, August 25-29, 2014.

``` 
BIBTEX ENTRY
@article{MendoncaAluisio2014,
 author = {Mendon\c{c}a, Gustavo and Alu\'isio, Sandra},
 title = {Using a hybrid approach to build a pronunciation dictionary for Brazilian Portuguese},
 journal = {Proceedings of INTERSPEECH 2014 -- 15th Annual Conference of the International Speech Communication Association},
 issue_date = {August 2014},
 year = {2014},
 publisher = {ISCA},
 address = {Singapure},
} 
``` 



