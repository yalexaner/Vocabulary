import os

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

vocabulary = read_vocabulary()

# choice
choice = int(input("Add words - 1\n" \
				   "Get words - 2\n" \
				   "Get number of words in the vocabulary - 3\n"))

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
elif choice == 2:
	path = str(input("Write file path and name: "))
	output_path = str(input("Write file-output path and name: "))
	words = []

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
					word_was_added, index = word_in(word, words)
					word_in_vocabulary, nothing = word_in(word, vocabulary)

					if not word_was_added and not word_in_vocabulary:
						words.insert(index, word)

	# output in file
	with open(output_path, 'w') as out:
		for word in words:
			out.write(word + '\n')
else:
	print("Your vocabulary has {} words".format(vocabulary_amount()))
