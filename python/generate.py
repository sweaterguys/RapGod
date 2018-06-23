
# Generate text.

from __future__ import print_function
from keras.models import load_model
import numpy as np
import os, collections, re, pronouncing, random
from six.moves import cPickle

directory = "python/data/"
def generator():

    batch_size = 15 # minibatch size
    seq_length = 15 # sequence length
    bars = 16 # number of lines to generate

    # Find a rhyme for one word.
    def quickRhyme(word):
        word = re.sub('[^A-Za-z]', '', word)
        try:
            words = pronouncing.rhymes(word.lower()) # A list of rhymes
            rhyme = words[random.randint(0,len(words)-1)] # A random choice from this list
            if rhyme in word: # To ensure the rhymes aren't too similar
                return words[random.randint(0,len(words)-1)]
            elif word in rhyme:
                return words[random.randint(0,len(words)-1)]
            else:
                return rhyme
        except:
            try:
                words = pronouncing.rhymes(word[-2:].lower())
                return words[random.randint(0,len(words)-1)]
            except:
                return word


    def sample(preds, temperature = 1.0): # helper function to sample an index from a probability array.
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)


    # Load vocabulary.
    with open(os.path.join(directory, 'vocab.pkl'), 'rb') as f:
            words, vocab, vocabulary_inv = cPickle.load(f)
    vocab_size = len(words)

    # Initiate sentences.
    sentence = []
    for i in range(seq_length):
        sentence.append('a')

    # Generate the text.
    model = load_model(os.path.join(directory, 'model.h5'))
    paragraph = ['seed']
    verse = ''
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
            # Calculate next word.
            preds = model.predict(x, verbose = 0)[0]
            next_index = sample(preds, 1)
            next_word = vocabulary_inv[next_index]
            if next_word in sentence[j - 3:]: # To prevent too much repetition
                next_word = quickRhyme(next_word)
            if next_word in ['nigga', 'niggas']:
                next_word = 'playa'
            if (i - 1) % 2 == 0 and j == 7:
                next_word = quickRhyme(paragraph[i][-1])
            sentence.append(next_word)
            bar += ' ' + next_word
        paragraph.append(sentence)
        verse += '\n\n' + bar


    return verse

