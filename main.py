from os import system
from os.path import exists
import re
import requests
import pysrt

from mylist import MyList
from config import translate_key


def translate(*words):
	data = {
		'host': 'translate.yandex.net/api/v1.5/tr.json/translate',
		'key': translate_key,
		'lang': 'en-ru'
	}

	url = 'https://{host}?key={key}&lang={lang}&text='.format(**data) + '&text='.join(words)

	res = requests.get(url).json()

	for word in res['text']:
		yield word


def delete_ending_ed(word):
	try:
		if word.endswith('eed'):
			return word[:-1]

		if word.endswith('ied'):
			return word[:-3] + 'y'

		if word[-4] == word[-3]:
			return word[:-3] if english_dictionary.word_in(word[:-3]) else word[:-2]

		if english_dictionary.word_in(word[:-1]):
			return word[:-1]

		return word[:-2] if english_dictionary.word_in(word[:-2]) else word
	except IndexError:
		return word


def delete_ending_ing(word):
	if len(word) < 5:
		return word

	try:
		# exceptions
		if word in ["lying", "dying", "tying"]:
			return word[0] + 'ie'

		if word[-5] == word[-4]:
			return word[:-4] if english_dictionary.word_in(word[:-4]) else word[:-3]

		if word.endswith('ying'):
			return word[:-3]

		if english_dictionary.word_in(word[:-3] + 'e'):
			return word[:-3] + 'e'

		return word[:-3] if english_dictionary.word_in(word[:-3]) else word
	except IndexError:
		return word


def delete_ending_s(word):
	if word.endswith('ss') or len(word) < 3:
		return word

	# word ends with -es
	if word.endswith('ves'):
		return word[:-3] + 'f' if english_dictionary.word_in(word[:-3] + 'f') else word[:-3] + 'fe'

	if word.endswith('ies'):
		return word[:-3] + 'y'

	if word.endswith(('oes', 'shes', 'ches', 'xes', 'sses', 'tches')):
		return word[:-2]

	# word ends with -s
	return word[:-1] if english_dictionary.word_in(word[:-1]) else word


vocabulary = MyList()
vocabulary.read_words("Data/vocabulary.txt")

system("clear")

while True:
	try:
		choice = int(input("Add words in vocabulary - 1\n"
		                   "Get unknown words - 2\n"
		                   "Get number of words in the vocabulary - 3\n"
		                   '> '))
	except ValueError:
		system("clear")

		print("Wrong symbol(s)! Try again.", end='\n\n')
	else:
		if 0 < choice < 4:
			break
		else:
			system("clear")

			print("Wrong number! Try again.", end='\n\n')

# refilling vocabulary
if choice == 1:
	system("clear")

	path = str(input("Write file path: "))

	while not exists(path):
		system("clear")
		path = str(input("The file does not exist!\nTry another path: "))

	# adding words
	with open(path) as file:
		for word in file:
			vocabulary.add(word.strip())

	# output in file
	with open("Data/vocabulary.txt", 'w') as out:
		for word in vocabulary:
			out.write(word + '\n')

	# output on screen
	print("\nAdding words in your vocabulary has Done.")
# working with unknown words
elif choice == 2:
	system("clear")

	withTranslation = True if input('Translate words? [y/n]\n> ') == 'y' else False

	system("clear")

	path = input("Write file path (.srt only): ")
	output_path = input("Write file-output path: ")	

	english_dictionary = MyList()
	english_dictionary.read_words("Data/less_words.txt")

	unique_words = MyList()
	total_words_amount = 0

	# reading and getting unique words
	words = []

	# with open(path) as file:
	file = pysrt.open(path)

	for sub in file:
		words += re.findall(r"\b[a-zA-Z]+(?:'\w+)?\b", sub.text)
	# words = re.findall(r"\b\w+'?\w*\b", file.read())

	for word in words:
		# short reductions
		if word.endswith("n't"):
			# exceptions
			if word == "won't":
				word = 'will'
			elif word == "shan't":
				word = 'shall'
			elif word == "can't":
				word = 'can'
			# other words
			else:
				word = word[:-3]
		elif word.endswith(("'s", "'d", "'m", "'ve", "'ll", "'re")):
			word, *_ = word.split('\'')

		if (word.istitle() or word.isupper()) and word != 'I':
			word = word.lower()

		if len(word) != 0:
			if word.endswith('ed'):
				word = delete_ending_ed(word)
			elif word.endswith('s'):
				word = delete_ending_s(word)
			elif word.endswith('ing'):
				word = delete_ending_ing(word)

		if english_dictionary.word_in(word):
			total_words_amount += 1
			unique_words.add(word)

	unknown_words = MyList(filter(lambda word: not vocabulary.word_in(word), unique_words))

	if withTranslation:
		unknown_words = zip(unknown_words, translate(*unknown_words))
		unknown_words = MyList(map(lambda words: ' - '.join(words), unknown_words))

	# output in file
	with open(output_path, 'w') as out:
		for word in unknown_words:
			out.write(word + '\n')

	# output to screen
	unique_words_amount = unique_words.size()
	unknown_words_amount = unknown_words.size()
	unknown_words_percent = (unknown_words_amount * 100) / unique_words_amount

	system("clear")

	print("Total words:\t{}".format(total_words_amount))
	print("Unique words:\t{}".format(unique_words_amount))
	print("Unknown words:\t{}/{:.2f}%".format(unknown_words_amount, unknown_words_percent))
else:
	system("clear")
	print("Your vocabulary is {} words".format(vocabulary.size()))
