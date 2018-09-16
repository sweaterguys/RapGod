# preprocess.py

# a collection of helper functions to prep rap lyrics
# first, from words to parts of speech then from parts of speech to vectors
# and a library of words for each part of speech
import nltk, csv, json, random
# nltk.download("punkt")

# posIndex = {'WDT': 32, 'NNS': 13, 'WP$': 34, 'VB': 26, 'VBD': 27, 'PRP': 18, 'JJR': 8, 'VBZ': 31, 'VBG': 28, 'NN': 12, 'DT': 3, 'WP': 33, 'UH': 25, 'VBP': 30, 'RB': 20, 'JJS': 9, 'RBR': 21, 'VBN': 29, 'LS': 10, 'CC': 1, 'TO': 24, 'RBS': 22, 'PDT': 16, 'MD': 11, 'PRP$': 19, 'WRB': 35, 'JJ': 7, 'EX': 4, 'IN': 6, 'POS': 17, 'NNPS': 15, 'CD': 2, 'FW': 5, 'RP': 23, 'NNP': 14}
posIndexBackward = {1: 'CC', 2: 'CD', 3: 'DT', 4: 'EX', 5: 'FW', 6: 'IN', 7: 'JJ', 8: 'JJR', 9: 'JJS', 10: 'LS', 11: 'MD', 12: 'NN', 13: 'NNS', 14: 'NNP', 15: 'NNPS', 16: 'PDT', 17: 'POS', 18: 'PRP', 19: 'PRP$', 20: 'RB', 21: 'RBR', 22: 'RBS', 23: 'RP', 24: 'TO', 25: 'UH', 26: 'VB', 27: 'VBD', 28: 'VBG', 29: 'VBN', 30: 'VBP', 31: 'VBZ', 32: 'WDT', 33: 'WP', 34: 'WP$', 35: 'WRB'}
posExamples = {'FW': {}, 'VBP': {}, 'CC': {}, 'WRB': {}, 'IN': {}, 'MD': {}, 'JJR': {}, 'LS': {}, 'NN': {}, 'NNP': {}, 'NNPS': {}, 'VB': {}, 'PDT': {}, 'VBG': {}, 'PRP': {}, 'RBR': {}, 'VBZ': {}, 'PRP$': {}, 'WDT': {}, 'TO': {}, 'CD': {}, 'JJ': {}, 'VBN': {}, 'RB': {}, 'POS': {}, 'VBD': {}, 'WP': {}, 'UH': {}, 'RP': {}, 'RBS': {}, 'WP$': {}, 'JJS': {}, 'NNS': {}, 'EX': {}, 'DT': {}}


def raps2pos(bars):

	with open("pos.csv", "w") as g:
		writer = csv.writer(g)

		for line in bars:
			tokens = nltk.word_tokenize(line)
			tags = nltk.pos_tag(tokens)
			pos = [tag[1] for tag in tags if "''" not in tag[1]]

			if len(pos) == 8:
				writer.writerow(pos)


def raps2index(bars):

	with open("posIndex.csv", "w") as h:
		writer = csv.writer(h)

		for line in bars:
			tokens = nltk.word_tokenize(line)
			tags = nltk.pos_tag(tokens)
			pos = [tag[1] for tag in tags if "''" not in tag[1]]

			if "(" in pos or ")" in pos:
				continue

			pos = [posIndex[p] for p in pos]
			if len(pos) == 8:
				writer.writerow(pos)


def vocab(bars):

	for line in bars:
		tokens = nltk.word_tokenize(line)
		tags = nltk.pos_tag(tokens)

		for tag in tags:
			if "''" not in tag[1]:
				pos = tag[1]

				if "(" in pos or ")" in pos:
					continue

				if tag[0] in posExamples[pos]:
					posExamples[pos][tag[0]] += 1
				else:
					posExamples[pos][tag[0]] = 1

	for key in posExamples.keys():
		total = sum(posExamples[key].values())

		for word in posExamples[key].keys():
			posExamples[key][word] /= total

	json.dump(posExamples, open("vocab.json", "w"), sort_keys=True, indent=2)

# takes an integer and returns a random word for the POS at that index
def pos2random(index):

	# get vocab extracted from raps.txt
	with open("vocab.json", "r") as f:
		vocab = json.load(f)
		# posIndex = list(vocab.keys())

	# pick a random word from the options for that POS
	if index < 1 or index > 35:
		return ""
	pos = posIndexBackward[index]
	pos = vocab[pos]

	options = list(pos.keys())
	word = random.choice(options)

	return word

def main(rap_file):

	with open(rap_file, "r") as f:
		bars = f.read()
		bars = bars.lower()
		bars = bars.translate({ord(c): None for c in "!@#$().-,"})
		bars = bars.split("\n")

	# print("Converting rap lines to part-of-speech tags")
	# raps2pos(bars)
	# print("Vectorizing lines of part-of-speech tags")
	# raps2index(bars)
	# print("Building vocabulary from rap lyrics")
	# vocab(bars)
	print(pos2random(16))


if __name__ == "__main__":
	main("lyrics/raps.txt")
