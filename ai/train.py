
from __future__ import print_function
import numpy as np
import random, sys, os, codecs, re, random, collections, requests
from keras.models import Sequential, load_model
from keras.callbacks import History 
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import Adam, RMSprop
from six.moves import cPickle
from keras import callbacks
from keras.callbacks import ModelCheckpoint

from keras.callbacks import Callback

url = "http://127.0.0.0:5000"
class NBatchLogger(Callback):
    def __init__(self, display):
        self.step = 0
        self.display = display
        self.metric_cache = {}
    def on_batch_end(self, batch, logs={}):
        self.step += 1
        for k in self.params['metrics']:
            if k in logs:
                self.metric_cache[k] = self.metric_cache.get(k, 0) + logs[k]
        if self.step % self.display == 0:
            metrics_log = ''
            for (k, v) in self.metric_cache.items():
                val = v / self.display
                if abs(val) > 1e-3:
                    metrics_log += ' - %s: %.4f' % (k, val)
                else:
                    metrics_log += ' - %s: %.4e' % (k, val)
            data = str('step: {}/{} ... {}'.format(self.step,self.params['steps'],metrics_log))
            try:
            	requests.post(url+"/publish/step/", data=data)
            except:
            	print("fuck")
            self.metric_cache.clear()

###########################################################################
#  				      H     Y   P   E  R PARAMETERS 					  #
rnn_size = 512
batch_size = 15
seq_length = 15
num_epochs = 20
learning_rate = 0.002
sequences_step = 3
###########################################################################
vocab = '../data/epoch.pkl'
neural_network = '../data/epoch.h5'
###########################################################################

def train(vocab):
	input_file = os.path.join('raps.txt')
	vocab_file = os.path.join(vocab)
	with codecs.open(input_file, 'r', encoding = None) as f:
	    data = f.read()
	x_text = data.split()
	word_counts = collections.Counter(x_text)
	vocabulary_inv = [x[0] for x in word_counts.most_common()]
	words = [x[0] for x in word_counts.most_common()]
	vocab_size = len(words)
	vocabulary_inv = list(sorted(vocabulary_inv))
	vocabs = {x: i for i, x in enumerate(vocabulary_inv)}

	with open(os.path.join(vocab_file), 'wb') as f:
	    cPickle.dump((words, vocabs, vocabulary_inv), f)

	sequences = []
	next_words = []
	for i in range(0, len(x_text) - seq_length, sequences_step):
	    sequences.append(x_text[i: i + seq_length])
	    next_words.append(x_text[i + seq_length])

	X = np.zeros((len(sequences), seq_length, vocab_size), dtype = np.bool)
	y = np.zeros((len(sequences), vocab_size), dtype = np.bool)
	for i, sentence in enumerate(sequences):
	    for t, word in enumerate(sentence):
	        X[i, t, vocabs[word]] = 1
	    y[i, vocabs[next_words[i]]] = 1

	model = Sequential()
	model.add(LSTM(rnn_size, input_shape = (seq_length, vocab_size)))
	model.add(Dense(vocab_size))
	model.add(Activation('softmax'))
	optimizer = RMSprop(lr = learning_rate)
	model.compile(loss = 'categorical_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
	call1 = ModelCheckpoint(neural_network, monitor='loss', verbose=1, save_best_only=True, mode='min')
	callbacks_list = [call1]
	model.fit(X, y, batch_size = batch_size, epochs = num_epochs, validation_split = 0.3, verbose = 1, callbacks=callbacks_list)

train(vocab)

