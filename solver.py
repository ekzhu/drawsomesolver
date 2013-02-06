import re

def check_word(letter_count, word):
	for letter in set(word):
		if not letter_count.has_key(letter) or word.count(letter) > letter_count[letter]:
			return False
	return True

def findwords(letters, length):
	letters = letters.lower()
	letters_set = set(letters)
	letter_count = dict((letter, letters.count(letter)) for letter in letters_set)
	alphabet = ''.join(letters_set)
	possible_solution = re.compile('[' + alphabet + ']{'+ str(length) +'}$', re.I)
	words = set(word.lower()
	            for word in open('words').read().splitlines()
	            if possible_solution.match(word) and check_word(letter_count, word))
	return sorted(list(words))

if __name__ == "__main__":
	print findwords("keepup", 4)