# -*- encoding: utf-8 -*-

from __future__ import unicode_literals
from sklearn.feature_extraction import DictVectorizer
import nlpnet
import sys
from delaf import Delaf
from regras.marcador_sil_tonica import posRelacaoTonica
from regras.regras import getTranscription,getAligned

class ExtractFeatures(object):


	def __init__(self, nlpnet_model_dir=''):
		
		if nlpnet_model_dir != '':
			nlpnet.set_data_dir(nlpnet_model_dir)
			self.tagger = nlpnet.POSTagger()


	def getWordFeaturesSimple(self, word, phone_window_size = 5):
		'''
		Return the word features as a Dict for a simple string.

		Note: this method was developed to train the G2P converter using a simple word as input.
		Training a classifier using these features will produce worse results.

		Input:
		@param word (string): input word

		Output:
		A generator with a dictionary containing all word features:
		e.g. for input amigo:
			{
			    u'phone_0': u'#',
			    u'phone_1': u'#'
			    u'phone_2': u'Á',
			    u'phone_3': u'-',
			    u'phone_4': u'@',
			    u'syll_distance_to_stress': -1,
			    u'pos': u'art',
			}
			{
			    u'phone_0': u'#',
			    u'phone_1': u'Á'
			    u'phone_2': u'-',
			    u'phone_3': u'@',
			    u'phone_4': u'M',
			    u'syll_distance_to_stress': 0,
			    u'pos': u'art',    
			}
			...
		'''

		word = word.lower().strip()

		if phone_window_size % 2 == 0: sys.exit('"phone_window_size" must be odd')

		# Obtain word POS using NLPNET tagger
		pos = self.tagger.tag(word)[0][0][1]

		# Obtain the partial transcription
		partial_trans = getTranscription(word)
		padded_partial_trans = '#'*(phone_window_size/2) + partial_trans + '#'*(phone_window_size/2)

		# Remove the left padding
		first_word_char_index = phone_window_size/2
		last_word_char_index = len(padded_partial_trans) - first_word_char_index

		# Iterate over each character and yield the features
		for i in range(first_word_char_index, last_word_char_index):

			# Define the featuers dict, which will be yielded
			features_dict = {}

			# Define the phone window
			# +1 because the right side is not inclusive
			phone_window = padded_partial_trans[i-(phone_window_size/2):i+(phone_window_size/2)+1] 
			for j, phone in enumerate(phone_window):
				features_dict['phone_' + str(j)] = phone

			# Calculate the position of the character to stress
			features_dict['syll_distance_to_stress'] = posRelacaoTonica(padded_partial_trans, i)

			features_dict['pos'] = pos

			yield features_dict


	def getWordFeaturesDelafEntry(self, word, pos, gender, tense, person, number, phone_window_size = 5):
		'''
		Return the word features as a Dict for a Delaf dictionary entry.

		Note: this method was developed to train the G2P converter using all information in the Delaf dictionary.
		This information must be provided while calling the method.

		Input:
		@param word (string): input word
		@param pos (string): word part-of-speech tag (according to DELAF)
		@param gender (string): grammatical gender ('m' or 'f') 
		@param tense (string): verbal tense (according to DELAF)
		@param person (string): grammatical person (1,2,3)
		@param number (string): grammatical number ('s' or 'p')
		@param phone_windows_size (int): The phone windo size, must be an odd number

		Output:
		A generator with a dictionary containing all word features:
		e.g. for input amigo:
			{
			    u'phone_0': u'#',
			    u'phone_1': u'#'
			    u'phone_2': u'Á',
			    u'phone_3': u'-',
			    u'phone_4': u'@',
			    u'syll_distance_to_stress': -1,
			    u'pos': u'art',
			    u'gender': u'm',
			    u'tense': u'',  
			    u'number': u's',
			    u'person': u'',      
			}
			{
			    u'phone_0': u'#',
			    u'phone_1': u'Á'
			    u'phone_2': u'-',
			    u'phone_3': u'@',
			    u'phone_4': u'M',
			    u'syll_distance_to_stress': 0,
			    u'pos': u'art',
			    u'gender': u'm',
			    u'tense': u'',
			    u'number': u's',
			    u'person': u'',    
			}
			...
		'''

		word = word.strip()

		if phone_window_size % 2 == 0: sys.exit('"phone_window_size" must be odd')

		# Obtain the partial transcription
		partial_trans = getTranscription(word)
		padded_partial_trans = '#'*(phone_window_size/2) + partial_trans + '#'*(phone_window_size/2)

		# Remove the left padding
		first_word_char_index = phone_window_size/2
		last_word_char_index = len(padded_partial_trans) - first_word_char_index

		# Iterate over each character and yield the features
		for i in range(first_word_char_index, last_word_char_index):

			# Define the featuers dict, which will be yielded
			features_dict = {}

			# Define the phone window
			# +1 because the right side is not inclusive
			phone_window = padded_partial_trans[i-(phone_window_size/2):i+(phone_window_size/2)+1] 
			for j, phone in enumerate(phone_window):
				features_dict['phone_' + str(j)] = phone

			# Calculate the position of the character to stress
			features_dict['syll_distance_to_stress'] =  posRelacaoTonica(padded_partial_trans, i)

			features_dict['pos']	= pos
			features_dict['gender'] = gender
			features_dict['tense'] = tense
			features_dict['person'] = person
			features_dict['number'] = number

			yield features_dict
			

			
if __name__ == '__main__':
	
	# pos, gender, tense, person, number
	e = ExtractFeatures(nlpnet_model_dir='etc/nlpnet-pos')
	word = 'amigo'
	''
	for feat in e.getWordFeaturesDelafEntry(word, 'art', 'm', '', '', 's', 3):
		print feat

	print
	for feat in e.getWordFeaturesDelafEntry(word, 'art', 'm', '', '', 's', 5):
		print feat

	print 
	print
	for feat in e.getWordFeaturesSimple(word):
		print feat
	
