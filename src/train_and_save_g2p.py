# -*- encoding: utf-8 -*_

from extract_features_delaf import ExtractFeatures
from sklearn.feature_extraction import DictVectorizer
from sklearn import preprocessing
from delaf import DelafEntry
from numpy import array
from sklearn import tree, svm
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.cross_validation import StratifiedKFold
from sklearn.externals import joblib
from numpy import array
import os
import argparse


def extract_and_save_features_simple(delaf_trans_file, nlpnet_model_dir, dir_to_save_g2p):

	e = ExtractFeatures(nlpnet_model_dir)
	vectorizer = DictVectorizer(sparse=False)
	lab_encoder = preprocessing.LabelEncoder()
	
	train_samples = []
	train_labels = []

	# Open the delaf transcribed dictionary
	print 'Loading the delaf dictionary...'
	with open(delaf_trans_file) as delaf_file:
		for line in delaf_file:

			# Separate the entry and the transcription
			entry, trans = line.decode('utf-8').rsplit(';')

			entry = entry.strip()
			trans = trans.strip()

			# Create a DelafEntry object, in order to be able to retrieve the word and the gramm info
			delaf_entry = DelafEntry(entry)
			word = delaf_entry.getWord()

			# Get all word features and check whether the number of features is equal to the number of phonetic symbols
			word_feats = [f for f in e.getWordFeaturesSimple(word, phone_window_size = 5)]
			
			if len(word_feats) == len(trans):
				for i, feat in enumerate(word_feats):
					train_samples.append(feat)
					train_labels.append(trans[i])

	print 'Vectorizing the features...'
	print 'Number of samples: %s' % len(train_samples)
	
	train_samples = vectorizer.fit_transform(train_samples)
	train_labels = lab_encoder.fit_transform(train_labels)
	label_names = list(lab_encoder.classes_)

	joblib.dump(vectorizer, '%s/vectorizer_simple.pkl' % dir_to_save_g2p, compress=1)
	joblib.dump(lab_encoder, '%s/lab_encoder_simple.pkl' % dir_to_save_g2p, compress=1)

	train_and_eval_clf(train_samples, train_labels, label_names, '%s/g2p_clf_simple.pkl' % dir_to_save_g2p)


def extract_and_save_features_delaf_full(delaf_trans_file, nlpnet_model_dir, dir_to_save_g2p):

	e = ExtractFeatures(nlpnet_model_dir)
	vectorizer = DictVectorizer(sparse=False)
	lab_encoder = preprocessing.LabelEncoder()
	
	train_samples = []
	train_labels = []

	# Open the delaf transcribed dictionary
	print 'Loading the delaf dictionary...'
	with open(delaf_trans_file) as delaf_file:
		for line in delaf_file:

			# Separate the entry and the transcription
			entry, trans = line.decode('utf-8').rsplit(';')

			entry = entry.strip()
			trans = trans.strip()

			# Create a DelafEntry object, in order to be able to retrieve the word and the gramm info
			delaf_entry = DelafEntry(entry)
			word = delaf_entry.getWord()
			pos, number, gender, tense, person = delaf_entry.getAllGramInfo()

			# The values cannot be None, otherwise DictVectorizer raises an error
			if pos == None: pos = ''
			if number == None: number = ''
			if gender == None: gender = ''
			if tense == None: tense = ''
			if person == None: person = ''

			# Get all word features and check whether the number of features is equal to the number of phonetic symbols
			word_feats = [f for f in e.getWordFeaturesDelafEntry(word, pos, gender, tense, person, number, phone_window_size = 5)]
			
			
			if len(word_feats) == len(trans):
				for i, feat in enumerate(word_feats):
					train_samples.append(feat)
					train_labels.append(trans[i])

	print 'Vectorizing the features...'
	print 'Number of samples: %s' % len(train_samples)
	
	train_samples = vectorizer.fit_transform(train_samples)
	train_labels = lab_encoder.fit_transform(train_labels)
	label_names = list(lab_encoder.classes_)

	joblib.dump(vectorizer, '%s/vectorizer_delaf.pkl' % dir_to_save_g2p, compress=1)
	joblib.dump(vectorizer, '%s/lab_encoder_delaf.pkl' % dir_to_save_g2p, compress=1)

	print 'Training the classifier...'
	train_and_eval_clf(train_samples, train_labels, label_names, '%s/g2p_clf_delaf.pkl' % dir_to_save_g2p)


def train_and_eval_clf(trainingSamples, classLabels, labelNames, clf_pkl_file):
    '''
    Train and evaluate a Decision Tree classifier over the speller 
    features in 'speller_features_file', which was previously created by the
    script 'save_features_for_training.py'.
    '''

    # Divide the data into 5 stratified samples
    skf = StratifiedKFold(classLabels, n_folds=5)

    # Make the Decision TRee classifier
    clf = tree.DecisionTreeClassifier()
    #clf = svm.LinearSVC()
    
    # Loop through each fold, training the classifier and printing the results
    for train_index, test_index in skf:
    	
        data_train, data_test = trainingSamples[train_index], trainingSamples[test_index]
        classes_train, classes_test = classLabels[train_index], classLabels[test_index]
        
        clf = clf.fit(data_train, classes_train)
        pred = clf.predict(data_test)

        report =  classification_report(classes_test, pred, target_names=labelNames)
        cm = confusion_matrix(classes_test, pred)
        
        print report.encode('utf-8')
        break
    
    print 'Saving the classifier pickle (%s)...' % clf_pkl_file
    clf = clf.fit(trainingSamples, classLabels)
    joblib.dump(clf, clf_pkl_file, compress=1)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(description='Script to generate a feature file '\
                                     'to be read by the machine learning components.'\
                                     '\nUsage example: python src/save_features_for_training.py'\
                                     ' etc/bd_unitex_revisado.txt etc/nlpnet-pos/ feats/aeiouado pkl/aeiouado')
    parser.add_argument('input_delaf_file', help='Input Delaf transcribed corpus')
    parser.add_argument('nlpnet_model_dir', help='nlpnet POS model dir')
    parser.add_argument('dir_to_save_g2p', help='Dir to save G2P files')
    args = parser.parse_args()
    
    os.system('mkdir -p %s' % args.dir_to_save_g2p)

    extract_and_save_features_delaf_full(args.input_delaf_file, 
    	args.nlpnet_model_dir, 
    	args.dir_to_save_g2p)

    extract_and_save_features_simple(args.input_delaf_file, 
    	args.nlpnet_model_dir, 
    	args.dir_to_save_g2p)