
from __future__ import print_function
import numpy as np
import random, sys, os, pyttsx3, re, pronouncing, random
from keras.models import load_model
from six.moves import cPickle


###########################################################################
#  				      H     Y   P   E  R PARAMETERS 					  #
rnn_size = 512
batch_size = 15
seq_length = 15
num_epochs = 10
learning_rate = 0.002
sequences_step = 8
bars = 8
###########################################################################
corpus = 'MFDoom'
vocab = '{}_Vocab_{}_Epochs.pkl'.format(corpus, num_epochs)
neural_network = '{}_Model_{}_Epochs.h5'.format(corpus, num_epochs)
###########################################################################
def generator():
	def quickRhyme(word):
	    word = re.sub('[^A-Za-z]', '', word)
	    try:
	        rhymes = pronouncing.rhymes(word.lower())
	        ayn_rand = random.randint(0, len(rhymes) - 1)
	        rhyme = rhymes[ayn_rand]
	        if rhyme in word:
	            return rhymes[ayn_rand]
	        elif word in rhyme:
	            return rhymes[ayn_rand]
	        else:
	            return rhyme
	    except:
	        try:
	            rhymes = pronouncing.rhymes(word[-2:].lower())
	            return rhymes[ayn_rand]
	        except:
	            return word


	def sample(preds, temperature = 1.0):
	    preds = np.asarray(preds).astype('float64')
	    preds = np.log(preds) / temperature
	    exp_preds = np.exp(preds)
	    preds = exp_preds / np.sum(exp_preds)
	    probas = np.random.multinomial(1, preds, 1)
	    return np.argmax(probas)


	def generate(vocab):
		model = load_model(neural_network)
		with open(os.path.join(vocab), 'rb') as f:
			words, vocab, vocabulary_inv = cPickle.load(f)
		sentence = []
		verse = ''
		for i in range(seq_length):
		    sentence.append('a')
		paragraph = ['seed']
		vocab_size = len(words)
		for i in range(bars):
		    sentence = []
		    bar = ''
		    for j in range(8):
		        x = np.zeros((1, batch_size, vocab_size))
		        for t, word in enumerate(sentence):
		            try:
		                x[0, t, vocab[word.encode('ascii')]] = 1.
		            except:
		                continue
		        preds = model.predict(x, verbose = 0)[0]
		        next_index = sample(preds, 1)
		        next_word = vocabulary_inv[next_index]
		        if next_word in sentence[j - 3:]:
		            next_word = quickRhyme(next_word)
		        if (i - 1) % 2 == 0 and j == 7:
		            next_word = quickRhyme(paragraph[i][-1])
		        sentence.append(next_word)
		        bar += ' ' + next_word
		    paragraph.append(sentence)
		    verse += '\n\n' + bar
		return verse
	return generate(vocab)
