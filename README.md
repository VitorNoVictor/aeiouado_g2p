aeiouado_g2p
============

##Overview
**aeiouado_g2p** is a grapheme-to-phoneme converter for Brazilian Portuguese, based on the dialect of São Paulo (city). It was designed primarily for Speech Technologies, such as Automatic Speech Recognition Systems and Speech Synthesizers. However, it may also be used by linguists, speech therapists, lexicographers, students of Brazilian Portuguese as a second language, and whoever is interested in the sound structure of Brazilian Portuguese.

##Technical Information
**aeiouado_g2p** makes use of a hybrid approach for converting graphemes into phonemes, which takes advantage of both manual transcription rules and machine learning algorithms. The transcription task is carried out in a two-step process: 

1. Words are submitted to a set of transcription rules, in which predictable graphemes (mostly consonants) are transcribed; 
2. a machine learning classifier is used to predict the transcription of the remaining graphemes (mostly vowels). 

The classifier employs a Decision Tree to decide, given a certain grapheme, which phone should be transcribed. The method was evaluated through 5-fold cross-validation; results showed a F1-score of 0.98.

##Installation
To install **aeiouado_g2p**, simply download the .zip of the last version and extract it. 

On Ubuntu, you can try the following command from a terminal:
>wget https://github.com/gustavoauma/aeiouado_g2p/archive/master.zip -O aeiouado_g2p.zip
>unzip aeiouado_g2p.zip

##Usage from terminal line (Basic scripts)
The G2P central class is "AeiouadoG2P" which is defined in "src/g2p_converter.py". For running this class you need an Aeiouado trained model, along with an [nlpnet](http://nilc.icmc.usp.br/nlpnet/) POS tagger model. Versions of both models are distributed in the Github package. To test the G2P with the standard models, just type (in "aeiouado_g2p" directory): 
>python g2p_test.py aeiouado_trained_model/ etc/nlpnet-pos/

A script to transcribe a list of word is also provided in "./g2p_transcribe_wlist.py". This script take as input a file contaning a list of words, with one word per line; and outputs the words' transcriptions to a file, given a certain phone convention. Basic usage:
>python g2p_transcribe_wlist.py input_wlist_file output_trans_file phone_convention
where convention might be: 'ipa', 'xsampa', 'htk' or 'aeiouado'.

##Usage as a Python module
The G2P central class is "AeiouadoG2P" which is defined in "src/g2p_converter.py". For running this class you need an Aeiouado trained model, along with an [nlpnet](http://nilc.icmc.usp.br/nlpnet/) POS tagger model. Versions of both models are distributed in the Github package (please check "./aeiouado_trained_model" and "etc/nlpnet-pos"). The "AeiouadoG2P" class has 2 main methods, one which takes a simple word as input:

```python
def transcribe_word_simple(self, word, c = 'ipa', space = False, dic = True):
        '''
        Return the transcription of a word (simple format) in a given phone convention.

        Input:
        @param word (string): word in orthographic format.
        @param c (string): phone convention, available values:
            i) ipa: International Phonetic Alphabet (IPA);
            ii) xsampa: Extended Speech Assessment Methods Phonetic Alphabe (X-SAMPA);
            iii) htk: Hidden Markov Model (HTK) dictionary friendly version (== X-SAMPA without stress and syllable marks) 
            iv) aeiouado: Aeiouado internal format.
        @param space (boolean): whether or not to include space between transcription symbols (valid only for X-SAMPA)
        @param div (boolean): checks if word is in dic and return it, instead of transcribing it online (to be implemented)

        Output:
        trans (string): the word transcription in Aeiouado format.
        '''
```
 
and another which requires its grammatical information:

```python
   def transcribe_word_delaf(self, word, pos, gender, tense, person, number, c = 'ipa', space = False, dic = True):
        '''
        Given a word and its grammatical information (pos, gender, tense, person and number)
        in Delaf format, return the word transcription in Aeiouado's phone convention.

        This method is supposed to be used along with the Delaf Class's method ".getAllGramInfo",
        check script "delaf.py". A complete description of all possible inflections can be found in:
    
        http://www.nilc.icmc.usp.br/nilc/projects/unitex-pb/web/files/Formato_DELAF_PB.pdf 

        This method achieves better performance than "_conv_simple", specially with respect to
        mid-vowels and to the transcription of the 'x' grapheme.

        Input:
        @param word (string): word in orthographic format.
        @param pos (string): word part-of-speech.
        @param gender (string): grammatical gender ('m' or 'f').
        @param tense (string): verb tense ('W','G','K','P', ...)
        @param person (string): grammatical person ('1', '2' or '3').
        @param number (string): grammatical number ('s' or 'g').
        @param c (string): phone convention, available values:
            i) ipa: International Phonetic Alphabet (IPA);
            ii) xsampa: Extended Speech Assessment Methods Phonetic Alphabe (X-SAMPA);
            iii) htk: Hidden Markov Model (HTK) dictionary friendly version (== X-SAMPA without stress and syllable marks) 
            iv) aeiouado: Aeiouado internal format.
        @param space (boolean): whether or not to include space between transcription symbols (valid only for X-SAMPA)
        @param div (boolean): checks if word is in dic and return it, instead of transcribing it online (to be implemented)

        Output:
        trans (string): the word transcription in Aeiouado phone convention.
        '''
```  

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