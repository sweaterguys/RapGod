#RapGod.py
from __future__ import print_function
from flask import Flask, render_template, request, jsonify
import random, sys, os, re, pronouncing
from multiprocessing import Value
from keras.models import load_model
import numpy as np
from six.moves import cPickle
from flask_socketio import SocketIO, emit

global epoch, loss, step
counter = Value('i',0)

batch_size = 15
seq_length = 15
bars = 8
vocab = '../data/epoch.pkl'
neural_network = '../data/epoch.h5'

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

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

@app.route('/')
def init():
	return render_template("index.html")

@app.route('/generate/', methods=['GET'])
def generator():
	with counter.get_lock():
		counter.value += 1
	return generate(vocab)

@app.route('/stats/', methods=['GET'])
def stats():
	try:
		count=counter.value
		data = {'epoch':str(epoch), 'generated':str(count), "loss":str(loss), 'step':str(step)}
	except:
		data = {'epoch':"na", 'generated':"na", "loss":"na", "step":"na"}
	data = jsonify(data)
	return data

if __name__ == '__main__':
	app.run()
