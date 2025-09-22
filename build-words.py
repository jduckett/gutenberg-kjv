#!/usr/bin/env python3

import glob
import json
import os

dir_base = os.getcwd()
dir_source = os.path.join(dir_base, "data", "json")
dir_target = os.path.join(dir_base, "data", "words")

alpha = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

words = []

for testament in ["ot", "nt"]:

	file_spec_target = os.path.join(dir_target, f"words-{testament}.txt", )
	words_testament = []

	for file_spec in glob.glob(os.path.join(dir_source, testament, "**/*.json"), recursive=True):

		with open(file_spec, "r") as f:
			book = json.load(f)

		for chapter in book:

			for verse in chapter:

				for word in verse.split(" "):

					word_clean = ""

					for char in word:

						if char in alpha:
							word_clean += char

					word_clean = word_clean.strip()

					if word_clean and not word_clean in words_testament:
						words_testament.append(word_clean)


	print(f"           total words in {testament}: {len(words_testament)}")

	with open(file_spec_target, "w") as f:

		for word in sorted(words_testament):

			f.write(f"{word}\n")

			if not word in words:

				words.append(word)



print(f"             total words all: {len(words)}")

file_spec_target = os.path.join(dir_target, f"words-all.txt", )

with open(file_spec_target, "w") as f:

	for word in sorted(words):

		f.write(f"{word}\n")

for index, word in enumerate(words):
	words[index] = word.lower()

words = list(set(words))

print(f"total words all (lower case): {len(words)}")

file_spec_target = os.path.join(dir_target, f"words-all-lower.txt", )

with open(file_spec_target, "w") as f:

	for word in sorted(words):

		f.write(f"{word}\n")

