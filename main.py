import os # path.exists() and system()

def read_vocabulary():
	vocabulary = []

	if os.path.exists("vocabulary.txt"):
		with open("vocabulary.txt") as read:
			for word in read:
				vocabulary.append(word.strip())

	return vocabulary

def word_in(word, lst):
	start = 0
	end = len(lst) - 1
	mid = end // 2

	if end == -1:
		return (False, -1)
	
	while end - start > 1:
		if word < lst[mid]:
			end = mid - 1
			mid = (mid - start) // 2 + start
		elif word > lst[mid]:
			start = mid + 1
			mid = (end - mid) // 2 + mid
		else:
			return (True, -1)

	if word < lst[start]:
		return (False, start)
	elif lst[start] < word < lst[end]:
		return (False, end)
	elif lst[start] <= lst[end] < word:
		return (False, end + 1)
	else:
		return (True, -1)

def vocabulary_amount():
	global vocabulary

	amount = 0

	for i in vocabulary:
		amount += 1

	return amount

os.system("clear")

vocabulary = read_vocabulary()

# choice
choice = int(input("Add words - 1\n" \
				   "Get words - 2\n" \
				   "Get number of words in the vocabulary - 3\n"))

# refilling vocabulary
if choice == 1:
	path = str(input("Write file path and name: "))

	# adding words
	with open(path) as read:
		for word in read:
			word_in_vocabulary, index = word_in(word.strip(), vocabulary)

			if not word_in_vocabulary:
				vocabulary.insert(index, word.strip())

	# output in file
	with open("vocabulary.txt", 'w') as out:
		for word in vocabulary:
			out.write(word + '\n')

	os.system("clear")
# working with unknown words
elif choice == 2:
	path = str(input("Write file path and name: "))
	output_path = str(input("Write file-output path and name: "))

	unique_words = []

	total_words_amount = 0
	unique_words_amount = 0
	unknown_words_amount = 0
	unknown_words_procent = 0

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
					word_was_added, index = word_in(word, unique_words)

					total_words_amount += 1

					if not word_was_added:
						unique_words.insert(index, word)

						unique_words_amount += 1

	# getting unknown words
	unknown_words = []

	for word in unique_words:
		word_in_vocabulary, index = word_in(word, vocabulary)

		if not word_in_vocabulary:
			unknown_words.append(word)

			unknown_words_amount += 1

	# output in file
	with open(output_path, 'w') as out:
		for word in unknown_words:
			out.write(word + '\n')

	# output to screen
	unknown_words_procent = (unknown_words_amount * 100) / unique_words_amount

	os.system("clear")

	print("Total words:\t{}".format(total_words_amount))
	print("Unique words:\t{}".format(unique_words_amount))
	print("Unknown words:\t{}/{:.2f}%".format(unknown_words_amount, unknown_words_procent))
else:
	os.system("clear")
	print("Your vocabulary is {} words".format(vocabulary_amount()))
