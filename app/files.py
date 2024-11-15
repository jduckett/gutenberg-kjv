import logging
import os

##########################################################################################
def read_list_file(file_spec):

	buffer = []

	if os.path.exists(file_spec):
	
		try:

			logging.info(f"Reading file: {file_spec}")

			with open(file_spec, "r") as f:

				buffer = f.read().splitlines()

		except Exception as err:

			print(err)

	return buffer

##########################################################################################
def write_list_file(file_spec, items, attr="w"):

	try:

		logging.info(f"Writing file: {file_spec}")

		with open(file_spec, attr) as f:

			for item in items:

				f.write(f"{item}\n")

	except Exception as err:

			print(err)

