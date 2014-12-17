# -*- encoding: utf-8 -*-

from src.g2p_converter import AeiouadoG2P
import argparse


def show_all_trans_simple(word, g2p_instance):

    aeiouado_trans = g2p_instance.transcribe_word_simple(word, c = 'aeiouado')
    ipa_trans = g2p_instance.transcribe_word_simple(word, c = 'ipa')
    xsampa_trans = g2p_instance.transcribe_word_simple(word, c = 'xsampa')
    spaced_xsampa_trans = g2p_instance.transcribe_word_simple(word, c = 'xsampa', space = True)
    htk_trans = g2p_instance.transcribe_word_simple(word, c = 'htk')

    print '#' * 60
    print '### Transcribing word "%s" in all conventions (simple method)' % word 
    print '#' * 60
    print 'i) Aeiouado convention: %s' % aeiouado_trans.encode('utf-8')
    print 'ii) IPA: %s' % ipa_trans.encode('utf-8')
    print 'iii) X-SAMPA: %s' % xsampa_trans.encode('utf-8')
    print 'iv) spaced X-SAMPA: %s' % spaced_xsampa_trans.encode('utf-8')
    print 'v) HTK: %s' % htk_trans.encode('utf-8')
    print '#' * 60


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to test the speller over a text.')
    parser.add_argument('g2p_model_dir', help='G2P model dir')
    parser.add_argument('nlpnet_model_dir', help='nlpnet POS model dir')
    args = parser.parse_args()

    g2p = AeiouadoG2P(args.g2p_model_dir, args.nlpnet_model_dir)
    
    show_all_trans_simple(u'testando', g2p)
    print
    show_all_trans_simple(u'constituição', g2p)
    print
    show_all_trans_simple(u'aliança', g2p)
    print
    show_all_trans_simple(u'inconstitucionalissimamente', g2p)