#!/usr/bin/env python3

import app
import fnmatch
import json
import logging
import os
import traceback

titles = """
genesis=>The First Book of Moses: Called Genesis
exodus=>The Second Book of Moses: Called Exodus
leviticus=>The Third Book of Moses: Called Leviticus
numbers=>The Fourth Book of Moses: Called Numbers
deuteronomy=>The Fifth Book of Moses: Called Deuteronomy
joshua=>The Book of Joshua
judges=>The Book of Judges
ruth=>The Book of Ruth
1_samuel=>The First Book of Samuel
2_samuel=>The Second Book of Samuel
1_kings=>The First Book of the Kings
2_kings=>The Second Book of the Kings
1_chronicles=>The First Book of the Chronicles
2_chronicles=>The Second Book of the Chronicles
ezra=>Ezra
nehemiah=>The Book of Nehemiah
esther=>The Book of Esther
job=>The Book of Job
psalms=>The Book of Psalms
proverbs=>The Proverbs
ecclesiastes=>Ecclesiastes
songs=>The Song of Solomon
isaiah=>The Book of the Prophet Isaiah
jeremiah=>The Book of the Prophet Jeremiah
lamentations=>The Lamentations of Jeremiah
ezekiel=>The Book of the Prophet Ezekiel
daniel=>The Book of Daniel
hosea=>Hosea
joel=>Joel
amos=>Amos
obadiah=>Obadiah
jonah=>Jonah
micah=>Micah
nahum=>Nahum
habakkuk=>Habakkuk
zephaniah=>Zephaniah
haggai=>Haggai
zechariah=>Zechariah
malachi=>Malachi
matthew=>The Gospel According to Saint Matthew
mark=>The Gospel According to Saint Mark
luke=>The Gospel According to Saint Luke
john=>The Gospel According to Saint John
acts=>The Acts of the Apostles
romans=>The Epistle of Paul the Apostle to the Romans
1_corinthians=>The First Epistle of Paul the Apostle to the Corinthians
2_corinthians=>The Second Epistle of Paul the Apostle to the Corinthians
galatians=>The Epistle of Paul the Apostle to the Galatians
ephesians=>The Epistle of Paul the Apostle to the Ephesians
philippians=>The Epistle of Paul the Apostle to the Philippians
colossians=>The Epistle of Paul the Apostle to the Colossians
1_thessalonians=>The First Epistle of Paul the Apostle to the Thessalonians
2_thessalonians=>The Second Epistle of Paul the Apostle to the Thessalonians
1_timothy=>The First Epistle of Paul the Apostle to Timothy
2_timothy=>The Second Epistle of Paul the Apostle to Timothy
titus=>The Epistle of Paul the Apostle to Titus
philemon=>The Epistle of Paul the Apostle to Philemon
hebrews=>The Epistle of Paul the Apostle to the Hebrews
james=>The General Epistle of James
1_peter=>The First Epistle General of Peter
2_peter=>The Second General Epistle of Peter
1_john=>The First Epistle General of John
2_john=>The Second Epistle General of John
3_john=>The Third Epistle General of John
jude=>The General Epistle of Jude
revelation=>The Revelation of Saint John the Divine
"""

nt = [
	"matthew",
	"mark",
	"luke",
	"john",
	"acts",
	"romans",
	"1_corinthians",
	"2_corinthians",
	"galatians",
	"ephesians",
	"philippians",
	"colossians",
	"1_thessalonians",
	"2_thessalonians",
	"1_timothy",
	"2_timothy",
	"titus",
	"philemon",
	"hebrews",
	"james",
	"1_peter",
	"2_peter",
	"1_john",
	"2_john",
	"3_john",
	"jude",
	"revelation"
]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# source file
file_spec = app.dirs.data.join("10.txt.utf-8")

lines = app.read_list_file(file_spec)

content = []

total = 0
is_add_lines = False

# read all of the lines of the file.
# eliminate blank lines
# single line that contains ***
# single line that contains The New Testament of the King James Bible
for line in lines:

	if line:

		if "The First Book of Moses: Called Genesis" in line:

			total += 1

			if total >= 2:

				is_add_lines = True


		if "*** END OF THE PROJECT GUTENBERG EBOOK THE KING JAMES VERSION OF THE BIBLE ***" in line:

			is_add_lines = False


		if is_add_lines and not "***" in line and not "The New Testament of the King James Bible" in line:

			content.append(line)




# build a list of book_names / titles from the heredoc above.
keys = []

for title in titles.splitlines():

	if title:

		keys.append(title)


try:

	# loop through the book_names / titles
	# basically, scans the lines of the content.
	# looks for a line containing the current title.
	# when found, records the index of that line, then, continues
	# scanning for the title of the next book. when found, records
	# the index. (the book of revelation will never have a next_book_title)
	for index, key in enumerate(keys):

		book_name, title = key.split("=>")
		next_book_name, next_title = "", ""

		if index < len(keys) - 1:

			next_book_name, next_title = keys[index + 1].split("=>")


		index_begin = -1
		index_end = -1


		for index_line, line in enumerate(content):

			# if the index_begin has not been set yet
			if index_begin < 0:

				if line.strip() == title:

					index_begin = index_line

			# if the index_end has not been set yet
			elif index_end < 0:

				if line.strip() == next_title:

					index_end = index_line

					break


		# if the beginning index has been found
		if index_begin >= 0:

			book_content = []

			# if an index_end has been found, otherwise, include all content
			# to the end of content[]
			if index_end > 0:

				book_content = content[index_begin + 1:index_end]

			else:

				book_content = content[index_begin + 1:]

			dir_output = app.dirs.data.text.ot

			if book_name in nt:

				dir_output = app.dirs.data.text.nt


			file_spec = dir_output.join(f"{book_name}.txt")

			app.write_list_file(file_spec, book_content)


except Exception as err:

	traceback.print_exc()


try:

	dir_source = app.dirs.data.text

	# now that the source file has been broken into individual files containing
	# the content for each book. we need to clean them up a little bit.
	# simply due to the fact that the authors did not design the format of the source
	# file to be easily parsable, there are a few areas of garbage data.
	# for each bible book file
	# the file is read, the garbage is removed and it is reformatted to ensure
	# that the carriage return characters are removed and to ensure that the produced
	# text file has one verse per line in the file.
	for root, directories, files in os.walk(dir_source.to_string(), topdown = True):

		# process each file in the nt/ot directories
		for file_name in fnmatch.filter(files, "*.txt"):

			# build a full file spec
			file_spec = os.path.join(root, file_name)

			# read the contents of that file as lines
			lines = app.read_list_file(file_spec)

			# buffer to hold the full content of the file with the line breaks (carriage returns) removed.
			buffer = ""

			# loop through all the lines and glue them into one large string buffer.
			for line in lines:

				if line:

					# concantenate the line with a preceding space.
					buffer += f" {line}"


			# strip leading and trailing spaces
			buffer = buffer.strip()


			# garbage data may exist prior to the first verse, so, search for 1:1
			# and if the index is greater than zero some type of garbage must exist.
			# simply eliminate the garbage by reassigning buffer variable to include
			# all of the content from the index to the end.
			index = buffer.index("1:1")

			if index > 0:

				buffer = buffer[index:]


			# the approach is the break the entire content of the buffer into individual
			# tokens by splitting buffer based on a space " ".
			# then, loop through all of the tokens and identify the indexes of each token
			# that represents a chapter:verse marker. all of those indexes are added to a list
			# in order.
			token_indexes = []
			tokens = buffer.split(" ")

			for token_index, token in enumerate(tokens):

				# chapter:verse is formatted as 1:1
				# if the current token contains a ":", then, it might be a chapter:verse marker.
				if ":" in token:

					before, after = token.split(":")

					# if both strings on either side of the token are numbers, then,
					# we are considering it to be a chapter:verse marker.
					if before.isdigit() and after.isdigit():

						token_indexes.append(token_index)


			# buffer representing the lines of the file with one verse per line.
			new_contents = []

			# loop through the list of token_indexes.
			# content lines are reconstructed by grabbing the tokens between
			# token_indexes recorded in the code above.
			# each value in the token_indexes list is the index of a chapter:verse marker.
			# each token index is considered the beginning index, so, the ending index is
			# simply the next beginning index in the series.
			# the last index will not have an ending index. simply grab the rest of the content
			# in the tokens list.
			for token_index, index_begin in enumerate(token_indexes):

				# set the value to below zero
				# this is how i indentify the last one.
				index_end = -1

				# make sure this is not the last token_index in the token_indexes list.
				if token_index < len(token_indexes) - 1:

					# this gets the next token index in the list.
					index_end = token_indexes[token_index + 1]

				# if both values have been set, get the range.
				# otherwise, get from the index_begin to the end of tokens.
				if index_end > index_begin:

					line_tokens = tokens[index_begin:index_end]

				else:

					line_tokens = tokens[index_begin:]

				# now, reconstruct the line and add it to the new contents list.
				new_contents.append(" ".join(line_tokens))

			# rewrite the contents of the file.
			app.write_list_file(file_spec, new_contents)


			# now, generate JSON content
			file_spec_json = file_spec.replace(".txt", ".json")
			file_spec_json = file_spec_json.replace("text", "json")

			# read the contents of the file as lines
			lines = app.read_list_file(file_spec)

			# json_content is simply and array of arrays.
			# add an empty array representing contents of chapter one.
			json_content = [[]]
			chapter_number = 1

			for line in lines:

				# split the line via space " " character.
				tokens = line.split(" ")

				# the first token should ALWAYS BE a chapter:verse marker.
				# determine the chapter of the chapter:verse marker.
				chapter_str = tokens[0].split(":")[0]

				# reconstruct the line excluding the chapter:verse marker.
				new_line = " ".join(tokens[1:])

				# if chapter number of the current line matches chapter_number
				# simply add it to the current chapter array which is the last array of json_content
				# if chapter_number does not match, 
				if not (chapter_number == int(chapter_str)):

					chapter_number = int(chapter_str)
					json_content.append([])

				# append the reconstructed line to the end of the current chapter array which
				# is the last array in json_content
				json_content[-1].append(new_line)


			# write the target file as JSON content
			with open(file_spec_json, "w", encoding="utf-8") as f:

				f.write(json.dumps(json_content, indent=4, ensure_ascii=False))

except Exception as err:
	traceback.print_exc()

logging.info("complete")

