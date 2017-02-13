import os # path.exists() and system()

class MyList(list):
	def read_words(self, path):
		if os.path.exists(path):
			with open(path) as file:
				for word in file:
					self.append(word.strip())

	def size(self):
		return len(self)

	def add(self, word):
		word_in = False
		index = 0

		# check is word in
		start = 0
		end = len(self) - 1
		mid = end // 2

		if end == -1:
			word_in = False
			index = -1
		else:
			while end - start > 1:
				if word < self[mid]:
					end = mid - 1
					mid = (mid - start) // 2 + start
				elif word > self[mid]:
					start = mid + 1
					mid = (end - mid) // 2 + mid
				else:
					word_in = True
					index = -1
					break

			if not word_in:
				if word < self[start]:
					word_in = False
					index = start
				elif self[start] < word < self[end]:
					word_in = False
					index = end
				elif self[start] <= self[end] < word:
					word_in = False
					index = end + 1
				else:
					word_in = True
					index = -1

		# adding word
		if not word_in:
			self.insert(index, word)

	def word_in(self, word):
		start = 0
		end = len(self) - 1
		mid = end // 2

		if end == -1:
			return False

		while end - start > 1:
			if word < self[mid]:
				end = mid - 1
				mid = (mid - start) // 2 + start
			elif word > self[mid]:
				start = mid + 1
				mid = (end - mid) // 2 + mid
			else:
				return True

		if word == self[start]:
			return True
		elif word == self[end]:
			return True
		else:
			return False

def delete_ending_ed(word):
	global english_dictionary

	if len(english_dictionary) == 0:
		english_dictionary.read_words("Data/English Words.txt")
		# english_dictionary.read_words("Data/less_words.txt")

	if len(word) < 4:
		return word

	if word[-3] == 'i':
		return word[:-3] + 'y'
	elif word[-3] == word[-4]:
		return word[:-3]
	elif word[-3:-1] == 'ee':
		return word[:-1]

	word = word[:-2]

	if not english_dictionary.word_in(word):
		return word + 'e'
	else:
		return word

def delete_ending_ing(word):
	global english_dictionary

	if len(english_dictionary) == 0:
		english_dictionary.read_words("Data/English Words.txt")
		# english_dictionary.read_words("Data/less_words.txt")

	if word[-5] == word[-4]:
		word = word[:-3]

		if not english_dictionary.word_in(word):
			return word[:-1]
		else:
			return word

	# exceptions
	if word == "lying":
		return "lie"
	elif word == "dying":
		return "die"
	elif word == "tying":
		return "tie"

	word = word[:-3] + 'e'

	if not english_dictionary.word_in(word):
		return word[:-1]
	else:
		return word

def delete_ending_s(word):
	global english_dictionary

	if len(english_dictionary) == 0:
		english_dictionary.read_words("Data/English Words.txt")
		# english_dictionary.read_words("Data/less_words.txt")

os.system("clear")

vocabulary = MyList()
vocabulary.read_words("Data/vocabulary.txt")

choice = int(input("Add words in vocabulary - 1\n" \
				   "Get unknown words - 2\n" \
				   "Get number of words in the vocabulary - 3\n"))

# refilling vocabulary
if choice == 1:
	path = str(input("Write file path and name: "))

	# adding words
	with open(path) as file:
		for word in file:
			vocabulary.add(word.strip())

	# output in file
	with open("Data/vocabulary.txt", 'w') as out:
		for word in vocabulary:
			out.write(word + '\n')

	os.system("clear")
# working with unknown words
elif choice == 2:
	path = str(input("Write file path and name: "))
	output_path = str(input("Write file-output path and name: "))

	unique_words = MyList()
	english_dictionary = MyList()

	total_words_amount = 0

	# read and getting unique words
	with open(path) as file:
		for line in file:
			for word in line.split():
				if not word.isalpha():
					correct_word = ''

					for i, symbol in enumerate(word):
						if symbol == '\'':
							if i != 0 and word[i - 1] == 'n':
								if word == "won't":
									correct_word = 'will'
								elif word == "shan't":
									correct_word = 'shall'
								elif word == "can't":
									correct_word = 'can'
								else:
									correct_word = correct_word[:-1]
							break

						if symbol.isalpha():
							correct_word += symbol

					word = correct_word

				if (word.istitle() or word.isupper()) and len(word) > 1:
					word = word.lower()

				if len(word) != 0:
					if word[-2:] == 'ed':
						word = delete_ending_ed(word)
					elif word[-1] == 's':
						# word = delete_ending_s(word)
						pass
					elif word[-3:] == 'ing':
						word = delete_ending_ing(word)

					total_words_amount += 1

					unique_words.add(word)

	# getting unknown words
	unknown_words = MyList()

	for word in unique_words:
		if not vocabulary.word_in(word):
			unknown_words.add(word)

	# output in file
	with open(output_path, 'w') as out:
		for word in unknown_words:
			out.write(word + '\n')

	# output to screen
	unique_words_amount = unique_words.size()
	unknown_words_amount = unknown_words.size()
	unknown_words_procent = (unknown_words_amount * 100) / unique_words_amount

	os.system("clear")

	print("Total words:\t{}".format(total_words_amount))
	print("Unique words:\t{}".format(unique_words_amount))
	print("Unknown words:\t{}/{:.2f}%".format(unknown_words_amount, unknown_words_procent))
else:
	os.system("clear")
	print("Your vocabulary is {} words".format(vocabulary.size()))
