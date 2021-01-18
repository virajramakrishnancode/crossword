class Grid():

	def __init__(self, contained_words, remaining_words, dimension):

		self.contained_words = contained_words
		self.remaining_words = remaining_words
		self.dimension = dimension
		self.matrix = [["" for j in range(dimension)] for i in range(dimension)]

	def __str__(self):
		result_string = ""

		for row in self.matrix:
			for letter in row:

				if not letter:

					result_string += '.  '

				else:
					result_string += letter + "  "

			result_string += "\n"

		result_string += "Words contained: \n"

		for word in self.contained_words:
			result_string += word + "\n"

		return result_string


	def resize(self, increment):


		self.matrix = [[""]*self.dimension] + self.matrix + [[""]*self.dimension]

		for row in self.matrix:
			row.insert(0, "")
			row.append("")

		self.dimension += 2*increment



	# function finds the best place for the first word in remaining_words, and places it in the grid

	def find_word_place(self, word_dimension_creation):

		# inner function that calculates a score for placing a word (i.e. how compact it is)

		# the heuristic is the number of overlaps that occur for a given word
		# if no overlaps occur, score is 0 (can be made -1 but buggy)
		# if placing the word is impossible, makes the grid bigger in each direction
		# and then tries again

		def heuristic_calc(word, location, direction):

			row = location[0]
			col = location[1]

			potential = 0 if word_dimension_creation > len(word) - 1 else -1 # 0 if not anywhere in board so far, else -1

			if direction == "across":

				if col + len(word) > self.dimension:
					return -1

				for i in range(len(word)):
					letter = self.matrix[row][col + i]

					position = "middle"

					if row == 0:
						position = "top"

					if row == self.dimension - 1:
						position = "bottom"

					if col != 0 and i == 0 and self.matrix[row][col - 1]:
						return -1

					if col != self.dimension - len(word) and i == len(word) - 1 and self.matrix[row][col + i + 1]:
						return -1

					if letter and letter != word[i]:
						return -1

					elif letter and letter == word[i]:
						potential += 1

					elif position == "middle" and (self.matrix[row - 1][col + i] or self.matrix[row + 1][col + i]):
						return -1

					elif position == "top" and self.matrix[row + 1][col + i]:
						return -1

					elif position == "bottom" and self.matrix[row - 1][col + i]:
						return -1

				return potential


			else:
				if row + len(word) > self.dimension:
					return -1

				for i in range(len(word)):
					letter = self.matrix[row + i][col]

					position = "middle"

					if col == 0:
						position = "left"

					if col == self.dimension - 1:
						position = "right"

					if row != 0 and i == 0 and self.matrix[row - 1][col]:
						return -1

					if row != self.dimension - len(word) and i == len(word) - 1 and self.matrix[row + i + 1][col]:
						return -1

					if letter and letter != word[i]:
						return -1

					elif letter and letter == word[i]:
						potential += 1

					elif position == "middle" and (self.matrix[row + i][col - 1] or self.matrix[row + i][col + 1]):
						return -1

					elif position == "left" and self.matrix[row + i][col + 1]:
						return -1

					elif position == "right" and self.matrix[row + i][col - 1]:
						return -1


				return potential

		word = self.remaining_words[0]

		# try every spot and orientation, and find one that maxes heuristic

		max_location, max_direction, max_heuristic = None, None, -1

		for i in range(self.dimension):
			for j in range(self.dimension):
				for direction in ["across", "down"]:

					score = heuristic_calc(word, (i, j), direction)

					if score > max_heuristic:
						max_location, max_direction, max_heuristic = (i, j), direction, score

		# insert word in best place (if there even is a way to do so)

		if max_heuristic > -1:

			self.insert_word(max_location, max_direction)

		else:

			self.resize(1)

			self.find_word_place(word_dimension_creation + 1)


	# function that places a word in a place, removing it from remaining_words and placing it
	# in contained_words

	def insert_word(self, location, direction):

		word = self.remaining_words.pop(0)

		# put word in place

		row = location[0]
		col = location[1]

		if direction == "across":

			for i in range(len(word)):

				self.matrix[row][col + i] = word[i]

		else:

			for i in range(len(word)):

				self.matrix[row + i][col] = word[i]

		self.contained_words.append(word)






print("Hey, this is a thing that makes a crossword out of a set of words")
print("Enter the words below, when you are done, hit enter without typing anything")

word_array = []

is_done = False

while not is_done:
	new_word = input("Input your word here: ")

	if not new_word and word_array:
		is_done = True

	elif not new_word and not word_array:

		print("You don't have any words unfortunately")

	elif isinstance(new_word, str) and new_word.isalpha() and new_word.lower() not in word_array:
		word_array.append(new_word.lower())

	elif new_word.lower() in word_array:
		print("Already in list of words")

	else:
		print("Not a word, try again")


word_array.sort(reverse = True, key=len)

final_grid = Grid([], word_array, len(word_array[0]))

while final_grid.remaining_words:
	final_grid.find_word_place(0)

while all([element == "" for element in final_grid.matrix[-1]]):
	final_grid.matrix.pop()

while all(element == "" for element in [row[-1] for row in final_grid.matrix]):
	for across in final_grid.matrix:
		across.pop()

print(final_grid)







