
# This script trains an Long-Short-Term-Memory model to generate rap lyrics
# from a dataset of rap lyrics. 
# THIS TRAINING ALGORITHM IS SO QUICK COMPARED TO ANYTHING ELSE
# This is the right way to do it

# As of 6am Thursday, 21 June this works!

from __future__ import print_function
import numpy as np
import random, sys, os, codecs, collections, requests
from keras.models import Sequential
from keras.callbacks import History 
from keras.layers import Dense, Activation
from keras.layers import LSTM
from keras.optimizers import Adam, RMSprop
from six.moves import cPickle
from keras import callbacks
from keras.callbacks import ModelCheckpoint

from keras.callbacks import Callback

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
            	requests.post('http://127.0.0.1:5000/publish/step/', data=data)
            except:
            	print("fuck")
            self.metric_cache.clear()

def train():
	directory = 'data/' # directory to store models.
	filepath = os.path.join(directory, "Model.h5")

	###########################################################################
	#  S O L I D  G O L D  H E R E 
	###########################################################################
	rnn_size = 128 # size of RNN
	batch_size = 30 # minibatch size
	seq_length = 15 # sequence length
	num_epochs = 20 # number of epochs
	learning_rate = 0.002 # learning rate
	sequences_step = 3 # step to create sequences
	###########################################################################

	# Load input text.
	input_file = os.path.join(directory, 'lyrics.txt')
	vocab_file = os.path.join(directory, 'vocab.pkl')

	with codecs.open(input_file, 'r', encoding = None) as f:
	    data = f.read()

	# Prepare input text.
	x_text = data.split()
	word_counts = collections.Counter(x_text)
	vocabulary_inv = [x[0] for x in word_counts.most_common()]
	vocabulary_inv = list(sorted(vocabulary_inv))
	vocab = {x: i for i, x in enumerate(vocabulary_inv)}
	words = [x[0] for x in word_counts.most_common()]
	vocab_size = len(words)

	with open(os.path.join(vocab_file), 'wb') as f:
	    cPickle.dump((words, vocab, vocabulary_inv), f)

	sequences = []
	next_words = []
	for i in range(0, len(x_text) - seq_length, sequences_step):
	    sequences.append(x_text[i: i + seq_length])
	    next_words.append(x_text[i + seq_length])


	# Vectorize words.
	X = np.zeros((len(sequences), seq_length, vocab_size), dtype = np.bool)
	y = np.zeros((len(sequences), vocab_size), dtype = np.bool)
	for i, sentence in enumerate(sequences):
	    for t, word in enumerate(sentence):
	        X[i, t, vocab[word]] = 1
	    y[i, vocab[next_words[i]]] = 1


	# Build the model.
	model = Sequential()
	model.add(LSTM(rnn_size, input_shape = (seq_length, vocab_size)))
	model.add(Dense(vocab_size))
	model.add(Activation('softmax'))
	optimizer = RMSprop(lr = learning_rate)
	model.compile(loss = 'categorical_crossentropy', optimizer = optimizer, metrics = ['accuracy'])
	call1 = ModelCheckpoint(filepath, monitor='loss', verbose=0, save_best_only=True, mode='min')
	call2 = callbacks.RemoteMonitor(root='http://127.0.0.1:5000', field='epic', path='/publish/epoch/')
	call3 = NBatchLogger(display=1)
	callbacks_list = [call1, call2, call3]
	# Fit the model.
	model.fit(X, y, batch_size = batch_size, epochs = num_epochs, validation_split = 0.3, verbose = 1, callbacks=callbacks_list)
train()

