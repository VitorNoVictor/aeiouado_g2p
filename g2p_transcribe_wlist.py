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
    print 'v) HTK: %s' % spaced_xsampa_trans.encode('utf-8')
    print '#' * 60

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script to test the speller over a text.')
    parser.add_argument('g2p_model_dir', help='G2P model dir')
    parser.add_argument('nlpnet_model_dir', help='nlpnet POS model dir')
    parser.add_argument('dic_file', help='dictionary with exceptions')
    parser.add_argument('conv', help='phone convention: "ipa", "xsampa", "htk" or "aeiouado"')
    parser.add_argument('wlist_input', help='word list to transcribe')
    parser.add_argument('wlist_output', help='file to save the trascribed word list')
    args = parser.parse_args()

    g2p = AeiouadoG2P(args.g2p_model_dir, args.nlpnet_model_dir, args.dic_file)
    
    word_trans = []
    with open(args.wlist_input) as word_list:
        for line in word_list:
            word = line.decode('utf-8').strip()
            trans = g2p.transcribe_word_simple(word, c = args.conv)
            word_trans.append((word, trans))

    with open(args.wlist_output, 'w') as output_file:
        for word, trans in word_trans:
            output_file.write('%s  %s\n'.encode('utf-8') % (word.encode('utf-8'), trans.encode('utf-8')))