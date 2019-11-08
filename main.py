from os import system
from os.path import exists
import re
import requests
import pysrt
import click

from mylist import MyList
from config import translate_key

english_dictionary = MyList()
english_dictionary.read_words('Data/less_words.txt')


def translate_words(*words):
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
		if word in ['lying', 'dying', 'tying']:
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
vocabulary.read_words('Data/vocabulary.txt')


@click.group()
@click.version_option()
def cli():
	"""words — extract words from English text

	This is a program that extracts all the English words that you don't know
	from file you give. All the known words are stored in vocabulary.txt.
	Currently supports .srt files only.

	\b
	Extract words:
		words get sub.srt words.txt

	\b
	Extract words and translate them:
		words get sub.srt words.txt --translate

	\b
	Add words to your vocabulary:
		words vocab extend file-with-words.txt

	\b
	Get know your vocabulary:
		words vocab size
	"""
	

@cli.group()
def vocab():
	"""Manges your vocabulary."""


@cli.command('get')
@click.argument('input', type=click.Path(exists=True, readable=True,
										allow_dash=False))
@click.argument('output', type=click.Path(exists=True, readable=True,
										allow_dash=False))
@click.option('--translate', is_flag=True,
			  help='Translate all extracted words.')	
def get_words(input, output, translate):
	"""Extracts words and, if needed, translates them."""

	unique_words = MyList()
	total_words_amount = 0

	# reading and getting unique words
	words = []

	file = pysrt.open(input)

	for sub in file:
		words += re.findall(r"\b[a-zA-Z]+(?:'\w+)?\b", sub.text)

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

	if translate:
		unknown_words = zip(unknown_words, translate_words(*unknown_words))
		unknown_words = MyList(map(lambda words: ' - '.join(words), unknown_words))

	# output in file
	with open(output, 'w') as out:
		for word in unknown_words:
			out.write(word + '\n')

	# output to screen
	unique_words_amount = unique_words.size()
	unknown_words_amount = unknown_words.size()
	unknown_words_percent = (unknown_words_amount * 100) / unique_words_amount

	print('Total words:\t{}'.format(total_words_amount))
	print('Unique words:\t{}'.format(unique_words_amount))
	print('Unknown words:\t{}/{:.2f}%'.format(unknown_words_amount, unknown_words_percent))


@vocab.command('extend')
@click.argument('file', type=click.Path(exists=True, readable=True,
										allow_dash=False))
def add_words_to_vocab(file):
	"""Add words to your vocabulary."""
	
	with open(file) as file:
		for word in file:
			vocabulary.add(word.strip())

	with open('Data/vocabulary.txt', 'w') as out:
		for word in vocabulary:
			out.write(word + '\n')

	print('All words has been added to your vocabulary.')


@vocab.command('size')
def get_vocab_size():
	"""Shows how much words you have in your vocabulary."""
	print('You have {} {} in your vocabulary'.format(vocabulary.size(), 
		'word' if vocabulary.size() == 1 else 'words'))
