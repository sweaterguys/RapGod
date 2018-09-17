# rapgod.py

# trains an LSTM on 1x8 vectors corresponding to rap lines from raps.txt
import numpy
import matplotlib.pyplot as plot
from random import choice
from pronouncing import rhymes as rhyme
from preprocess import pos2random
from keras.layers import LSTM, Dense, Embedding
from keras.models import Sequential, load_model
from keras import backend as K


# to improve the model with your latest insights, simply set train_mode=True and tweak hyperparameters
def ai(batch_size=5, epochs=20, train_mode=False):

	def train(batch_size, epochs):

		# the neural network architecture: one LSTM layer then two Dense layers
		model = Sequential()
		model.add(LSTM(128, input_shape=(4, 1), return_sequences=False))
		model.add(Dense(32))
		model.add(Dense(4))

		# build the model
		model.compile(loss="mse", optimizer="adam", metrics=["accuracy"])
		print(model.summary())

		# training data from part-of-speech sequences in rap lyrics
		bars = numpy.genfromtxt("posIndex.csv", delimiter=",", dtype=int)

		# break rap lines up into beginning and last word
		first = bars[:, :4]
		first = first.reshape((first.shape[0], first.shape[1], 1))

		last = bars[:, -4:]
		last = last.reshape((last.shape[0], last.shape[1]))

		# train and save the model then remove it from memory to prevent slowdown
		print("Training will take about {} minutes.".format(int(first.shape[1] / .6)))
		history = model.fit(first, last,
						  batch_size=batch_size,
						  epochs=epochs,
						  verbose=1,
						  validation_split=0.2)
		model.save("model.h5")
		K.clear_session()

		# visualize training data
		plot.plot(history.history["acc"])
		plot.plot(history.history["val_acc"])
		plot.title("RapGod Model Accuracy")
		plot.legend(["Train", "Test"])
		plot.show()

		return history


	def generate():

		# load the neural network and initialize it with a random sentence
		model = load_model("model.h5")
		start = numpy.random.randint(1, 36, size=(4))
		line = []

		# recursive function to generate n lines of rap
		def bar(model, seed, count=16, depth=0):

			if depth == count:
				return

			predict = model.predict(seed.reshape((1, 4, 1)))
			pred = predict.tolist()[0]
			start = numpy.append(seed[2:], pred[:2])

			if depth > 0:
				for i in pred:
					line.append(pos2random(int(round(i))).lower())

			return bar(model, start, count, depth + 1)


		bar(model, start)

		for i in range(len(line)):
			if (i + 1) % 8 == 0:
				rhymes = rhyme(line[i])
				if rhymes:
					swap = choice(rhymes)
					if swap in line[i - 6] or line[i - 6] in swap:
						swap = choice(rhymes)
					line.insert(i - 6, swap)
					line.insert(i + 2, "\n")

		line = " ".join(line)
		print(line)

		return line


	if train_mode:
		train(batch_size, epochs)
	generate()


if __name__ == "__main__":
	ai(epochs=100, train_mode=False)
