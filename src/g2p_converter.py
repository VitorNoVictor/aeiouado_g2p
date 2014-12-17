# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from extract_features import ExtractFeatures
import argparse
from sklearn.externals import joblib
import re

class AeiouadoG2P(object):

    def __init__(self, g2p_dir, nlpnet_model_dir=''):

        self.clf_delaf = joblib.load('%s/g2p_clf_delaf.pkl' % g2p_dir)
        self.vectorizer_delaf = joblib.load('%s/vectorizer_delaf.pkl' % g2p_dir)
        self.lab_encoder_delaf = joblib.load('%s/lab_encoder_delaf.pkl' % g2p_dir)

        self.clf_simple = joblib.load('%s/g2p_clf_simple.pkl' % g2p_dir)
        self.vectorizer_simple = joblib.load('%s/vectorizer_simple.pkl' % g2p_dir)
        self.lab_encoder_simple = joblib.load('%s/lab_encoder_simple.pkl' % g2p_dir)
        
        self.dic = []
        self.feat_extractor = ExtractFeatures(nlpnet_model_dir)
        

    def _conv_simple(self, word):
        '''
        Return the transcription of a word (simple format) in Aeiouado's phone convention.
        '''

        word = word.strip()        
        trans = []

        for ch_feats in self.feat_extractor.getWordFeaturesSimple(word):
            
            num_feats = self.vectorizer_simple.transform(ch_feats)
        
            predicted_class_num = self.clf_simple.predict(num_feats)[0]
            predicted_class = self.lab_encoder_simple.inverse_transform(predicted_class_num)
        
            trans.append(predicted_class)
                   
        return ''.join(trans)


    def _conv_delaf(self, word, pos, gender, tense, person, number):
        '''
        Return the transcription of a word (Delaf format) in Aeiouado's phone convention.
        '''

        word = word.strip()        
        trans = []

        for ch_feats in self.feat_extractor.getWordFeaturesDelafEntry(word, pos, gender, tense, person, number):
            
            num_feats = self.vectorizer_simple.transform(ch_feats)
        
            predicted_class_num = self.clf_simple.predict(num_feats)[0]
            predicted_class = self.lab_encoder_simple.inverse_transform(predicted_class_num)
        
            trans.append(predicted_class)
                   
        return ''.join(trans)
    

    def _conv2ipa(self, trans):
        trans = trans.replace('P', 'p')
        trans = trans.replace('B', 'b')
        trans = trans.replace('T', 't')
        trans = trans.replace('D', 'd')
        trans = trans.replace('K', 'k')
        trans = trans.replace('G', 'g')
        trans = trans.replace('7', 'tʃ')
        trans = trans.replace('8', 'dʒ')
        trans = trans.replace('M', 'm')
        trans = trans.replace('N', 'n')
        trans = trans.replace('Ñ', 'ɲ')
        trans = trans.replace('F', 'f')
        trans = trans.replace('V', 'v')
        trans = trans.replace('S', 's')
        trans = trans.replace('Z', 'z')
        trans = trans.replace('X', 'ʃ')
        trans = trans.replace('J', 'ʒ')
        trans = trans.replace('L', 'l')
        trans = trans.replace('Ĺ', 'ʎ')
        trans = trans.replace('Ŕ', 'ɾ')
        trans = trans.replace('H', 'x')
        trans = trans.replace('R', 'ɣ')
        trans = trans.replace('-Q', 'k-s')
        trans = trans.replace('Q', 'ks')
        trans = trans.replace('W', 'w')
        trans = trans.replace('Y', 'y')
        trans = trans.replace('Ŵ', 'ʊ̃')
        trans = trans.replace('Ỹ', 'ỹ')
        trans = trans.replace('Á', 'a')
        trans = trans.replace('6', 'ə')
        trans = trans.replace('É', 'ɛ')
        trans = trans.replace('Ê', 'e')
        trans = trans.replace('Í', 'i')
        trans = trans.replace('I', 'ɪ')
        trans = trans.replace('Ó', 'ɔ')
        trans = trans.replace('Ô', 'o')
        trans = trans.replace('Ú', 'u')
        trans = trans.replace('U', 'ʊ')
        trans = trans.replace('Ã', 'ã')
        trans = trans.replace('Ẽ', 'ẽ')
        trans = trans.replace('Ĩ', 'ĩ')
        trans = trans.replace('Õ', 'õ')
        trans = trans.replace('Ũ', 'ũ')
        trans = trans.replace('@', "'")
        trans = trans.replace("-'", "'")
        return trans
    

    def _ipa2sampa(self, trans):
        trans = re.sub('p', ' p ', trans)
        trans = re.sub('b', ' b ', trans)
        trans = re.sub(r't([^ʃ])', r' t \1 ', trans)
        trans = re.sub(r'd([^ʒ])', r' d \1 ', trans)
        trans = re.sub('k', ' k ', trans)
        trans = re.sub('g', ' g ', trans)
        trans = re.sub('tʃ', ' tS ', trans)
        trans = re.sub('dʒ', ' dZ ', trans)
        trans = re.sub('ʃ', ' S ', trans)
        trans = re.sub('ʒ', ' Z ', trans)
        trans = re.sub('m', ' m ', trans)
        trans = re.sub('n', ' n ', trans)
        trans = re.sub('f', ' f ', trans)
        trans = re.sub('v', ' v ', trans)
        trans = re.sub('s', ' s ', trans)
        trans = re.sub('z', ' z ', trans)
        trans = re.sub(r'([^t])ʃ', r' \1 S ', trans)
        trans = re.sub(r'([^d])ʒ', r' \1 Z ', trans)
        trans = re.sub('Ñ', ' J ', trans)
        trans = re.sub('ɲ', ' J ', trans)
        trans = re.sub('L', ' l ', trans)
        trans = re.sub('ʎ', ' L ', trans)
        trans = re.sub('ɾ', ' 4 ', trans)
        trans = re.sub('x', ' x ', trans)
        trans = re.sub('ɣ', ' G ', trans)
        trans = re.sub('ks', ' k s ', trans)
        trans = re.sub('w', ' w ', trans)
        trans = re.sub('y', ' j ', trans)
        trans = re.sub('ʊ̃', ' w~ ', trans)
        trans = re.sub('ỹ', ' j~ ', trans)
        trans = re.sub('a', ' a ', trans)
        trans = re.sub('@', '', trans)
        trans = re.sub('ə', ' @ ', trans)
        trans = re.sub('ɛ', ' E ', trans)
        trans = re.sub('e', ' e ', trans)
        trans = re.sub('i', ' i ', trans)
        trans = re.sub('ɪ', ' I ', trans)
        trans = re.sub('ɔ', ' O ', trans)
        trans = re.sub('o', ' o ', trans)
        trans = re.sub('u', ' u ', trans)
        trans = re.sub('ʊ', ' U ', trans)
        trans = re.sub('\-', ' . ', trans)
        trans = re.sub("'", ' " ', trans)
        
        trans = re.sub(r'ã', r' a~ ', trans)
        trans = re.sub(r'ẽ', r' e~ ', trans)
        trans = re.sub(r'ĩ', r' i~ ', trans)
        trans = re.sub(r'õ', r' o~ ', trans)
        trans = re.sub(r'ũ', r' u~ ', trans)

        trans = re.sub(r' ~', r'~', trans)
    
        trans = re.sub(r'[ ]{2,}', r' ', trans.strip())
        return trans

    def _sampa2htk(self, trans):
        trans = trans.replace('.', '')
        trans = trans.replace('"', '')
    
        trans = re.sub(r'[ ]{2,}', r' ', trans.strip())
        return trans



    def transcribe_word_simple(self, word, c = 'ipa', space = False, dic = True):
    
        word = word.lower()
        
        if dic:
            if word in self.dic:
                trans = self.dic[word][0]
            else:
                trans = self._conv_simple(word)
        else:
            trans = self._conv_simple(word)
        
        if c == 'ipa':
            return self._conv2ipa(trans)
        elif c == 'xsampa':
            if space == True:
                return self._ipa2sampa(self._conv2ipa(trans))
            else:
                spacedXsampa = self._ipa2sampa(self._conv2ipa(trans))
                return ''.join(spacedXsampa.split())
        elif c == 'htk':
            return self._sampa2htk(self._ipa2sampa(self._conv2ipa(trans)))
        elif c == 'aeiouado':
            return trans
        else:
            return self._conv2ipa(trans)


    def transcribe_word_delaf(self, word, pos, gender, tense, person, number, c = 'ipa', space = False, dic = True):
    
        word = word.lower()
        
        if dic:
            if word in self.dic:
                trans = self.dic[word][0]
            else:
                trans = self._conv_delaf(word)
        else:
            trans = self._conv_delaf(word)
        
        if c == 'ipa':
            return self._conv2ipa(trans)
        elif c == 'xsampa':
            if space == True:
                return self._ipa2sampa(self._conv2ipa(trans))
            else:
                spacedXsampa = self._ipa2sampa(self._conv2ipa(trans))
                return ''.join(spacedXsampa.split())
        elif c == 'aeiouado':
            return trans
        else:
            return self._conv2ipa(trans)


