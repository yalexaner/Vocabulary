from os.path import exists

'''
This file includes class 'MyList' expanding built-in type 'list' with some functions:
	* read_words(self, path) - this function reads text from given file(path);
	* size(self) - the same thing that len()
	* add(self, word) - adding not-added word(word)
	* word_in(self, word, withIndex=False) - checking given word in list.
		If word is in, returns True if withIndex=False and (-1, True) if withIndex=True.
		Else returns False if withIndex=False and (its index, False) if withIndex=True.
'''


class MyList(list):
	def read_words(self, path):
		if exists(path):
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
