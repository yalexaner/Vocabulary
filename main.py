import os # path.exists() and system()
import re

class MyList(list):
	def read_words(self, path):
		if os.path.exists(path):
			with open(path) as file:
				for word in file:
					self.append(word.strip())

	def size(self):
		return len(self)

	def add(self, word):
		index, word_in = self.word_in(word, withIndex=True)

		if not word_in:
			self.insert(index, word)

	def word_in(self, word, withIndex=False):
		start = 0
		end = len(self) - 1
		mid = end // 2

		if end == -1:
			return (0, False) if withIndex else False

		while end - start > 1:
			if word < self[mid]:
				end = mid - 1
				mid = (mid - start) // 2 + start
			elif word > self[mid]:
				start = mid + 1
				mid = (end - mid) // 2 + mid
			else:
				return (-1, True) if withIndex else True

		if word < self[start]:
			return (start, False) if withIndex else False

		if self[start] < word < self[end]:
			return (end, False) if withIndex else False

		if self[start] <= self[end] < word:
			return (end + 1, False) if withIndex else False

		return (-1, True) if withIndex else True

def delete_ending_ed(word):
	global english_dictionary

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
	global english_dictionary

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
	global english_dictionary

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

os.system("clear")

while True:
	try:
		choice = int(input("Add words in vocabulary - 1\n"\
						   "Get unknown words - 2\n"\
						   "Get number of words in the vocabulary - 3\n"\
						   '> '))
	except ValueError:
		os.system("clear")

		print("Wrong symbol(s)! Try again.", end='\n\n')
	else:
		if 0 < choice < 4:
			break
		else:
			os.system("clear")

			print("Wrong number! Try again.", end='\n\n')

# refilling vocabulary
if choice == 1:
	os.system("clear")

	path = str(input("Write file path and name: "))

	while not os.path.exists(path):
		os.system("clear")
		path = str(input("The file does not exist!\nTry again: "))

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
	os.system("clear")

	path = input("Write file path and name: ")
	output_path = input("Write file-output path and name: ")

	english_dictionary = MyList()
	# english_dictionary.read_words("Data/English Words.txt")
	english_dictionary.read_words("Data/less_words.txt")

	unique_words = MyList()
	total_words_amount = 0

	# read and getting unique words
	with open(path) as file:
		words = re.findall(r"\w+'?\w+", file.read())

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
				word = word.split('\'')[0]

			if (word.istitle() or word.isupper()) and word != 'I':
				word = word.lower()

			if len(word) != 0:
				if word.endswith('ed'):
					# word += ' - ' + delete_ending_ed(word)
					word = delete_ending_ed(word)
				elif word.endswith('s'):
					# word += ' - ' + delete_ending_s(word)
					word = delete_ending_s(word)
				elif word.endswith('ing'):
					# word += ' - ' + delete_ending_ing(word)
					word = delete_ending_ing(word)

			if english_dictionary.word_in(word):
				total_words_amount += 1
				unique_words.add(word)

	unknown_words = MyList(list(filter(lambda word: not vocabulary.word_in(word), unique_words)))

	# output in file
	with open(output_path, 'w') as out:
		for word in unknown_words:
			out.write(word + '\n')

	# output to screen
	unique_words_amount = unique_words.size()
	unknown_words_amount = unknown_words.size()
	unknown_words_percent = (unknown_words_amount * 100) / unique_words_amount

	os.system("clear")

	print("Total words:\t{}".format(total_words_amount))
	print("Unique words:\t{}".format(unique_words_amount))
	print("Unknown words:\t{}/{:.2f}%".format(unknown_words_amount, unknown_words_percent))
else:
	os.system("clear")
	print("Your vocabulary is {} words".format(vocabulary.size()))
