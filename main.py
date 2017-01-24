import os # path.exists() and system()

class MyList(list):

	def __init__(self, path = '0'):
		if path == '0':
			super(MyList, self).__init__()
		else:
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
		else:
			while end - start > 1:
				if word < self[mid]:
					end = mid - 1
					mid = (mid - start) // 2 + start
				elif word > self[mid]:
					start = mid + 1
					mid = (end - mid) // 2 + mid
				else:
					return True

			if word < self[start]:
				return False
			elif self[start] < word < self[end]:
				return False
			elif self[start] <= self[end] < word:
				return False
			else:
				return True

os.system("clear")

vocabulary = MyList("vocabulary.txt")

choice = int(input("Add words - 1\n" \
				   "Get words - 2\n" \
				   "Get number of words in the vocabulary - 3\n"))

# refilling vocabulary
if choice == 1:
	path = str(input("Write file path and name: "))

	# adding words
	with open(path) as file:
		for word in file:
			vocabulary.add(word.strip())

	# output in file
	with open("vocabulary.txt", 'w') as out:
		for word in vocabulary:
			out.write(word + '\n')

	os.system("clear")
# working with unknown words
elif choice == 2:
	path = str(input("Write file path and name: "))
	output_path = str(input("Write file-output path and name: "))

	unique_words = MyList()

	total_words_amount = 0

	# read and getting unique words
	with open(path) as file:
		for line in file:
			for word in line.split():
				if not word.isalpha():
					correct_word = ''

					for symbol in word:
						if symbol == '\'':
							break

						if symbol.isalpha():
							correct_word += symbol

					word = correct_word

				if (word.istitle() or word.isupper()) and len(word) > 1:
					word = word.lower()

				if len(word) != 0:
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
