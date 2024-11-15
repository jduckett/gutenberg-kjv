import glob
import os
import shutil

def total_lpad(value):

	total = 0

	for char in value:

		if char == " ":

			total += 1

		else:

			break

	return total

class Directory:

	# name = the directory name. it can be a simple name, period or tilda
	#        names that begin with a period or tilda are expanded into a full directory path
	#        the .name attribute is used by to_string() when building the full path
	#        as a string.
	#        NOTE: you should not use a period or tilda for calls to sub_directory()
	#        use a simple name only
	def __init__(self, name, schema=""):

		if name.endswith("/"):
			name = name[:-1]

		# i added support for expansion of certain directories.
		# the root node should be the only on 
		if name.startswith("."):
			name = os.path.abspath(name)

		elif name.startswith("~"):
			name = os.path.expanduser(name)

		self.children = []
		self.name = name
		self.parent = None

		self.build_schema(schema)

	def __str__(self):
		return self.to_string()

	def __repr__(self):
		return self.to_string()

	def to_string(self):

		# supposedly this is faster code (list comprehension)
		# this was a standard for loop appending to a list.
		names = (node.name for node in self.get_node_chain())

		return os.path.sep.join(names)

	def ensure_tree(self):

		self.ensure()

		for child in self.children:
			child.ensure_tree()

		return None


	def ensure(self):

		path = self.to_string()

		if not os.path.exists(path):
			os.makedirs(path, exist_ok=True)

	def get(self, name):

		for child in self.children:

			if child.name == name:

				return child

		return None

	# finds the root node of the tree based on the current node
	def get_node_chain(self):

		# creates a list of Directory objects adding self to it.
		nodes = [self]

		# loop until the root node is found. every node has a parent except
		# the root node. therefore, we loop until we find a node with a null parent.
		# we are always evaluating the first node in the list.
		# inside the loop we take the parent of the first node in the list
		# and insert the parent in front of it shifting all nodes over one.
		while nodes[0].parent:

			nodes.insert(0, nodes[0].parent)

		return nodes

	def get_root(self):

		if self.parent:

			return self.parent.get_root()

		else:

			return self

	def join(self, value):
		return os.path.join(self.to_string(), value)

	def print_tree(self, indent=0):

		print(f"{'    ' * (indent - 1)}{self.name}")

		for child in sorted(self.children, key=lambda child: child.name):
			child.print_tree(indent + 1)

	def sub_directory(self, name):

		dir = Directory(name)

		dir.parent = self

		for char in "-.":
			name = name.replace(char, "_")

		setattr(self, name, dir)

		self.children.append(dir)

		return dir

	def sync_file_system(self):

		self.ensure_tree()

		root_node = self.get_root()
		path_root = root_node.to_string()

		for root, dirs, files in os.walk(path_root):

			for dir in dirs:

				path_target = os.path.join(root, dir)

				# print("===========================>")
				# print(path_root)
				# print(path_target)

				path_target = path_target.replace(path_root, "")

				if path_target.startswith("/"):

					# remove the first character of the target path
					# if it begins with a "/"
					path_target = path_target[1:]

				# print(path_target)

				current_node = root_node

				for name in path_target.split("/"):

					if not current_node.get(name):

						current_node = current_node.sub_directory(name)

					else:

						current_node = current_node.get(name)




	# level01-01
	#     level02-01
	#         level03-01
	#         level03-02
	#             level04-01
	#             level04-02
	#             level04-03
	#                 level05-01
	#             level04-04
	#             level04-05
	#         level03-03
	#     level02-02
	#     level02-03
	#         level03-01
	#         level03-02
	#     level02-04
	# level01-02
	# level01-03
	# level01-04

	def build_schema(self, schema):

		if schema:

			lines = []

			# split the lines based on carriage return
			# process each line and store a dict with total number of leading spaces and a stripped name
			for line in schema.splitlines():

				line_stripped = line.strip()

				# allow lines to be commented out
				if line_stripped and not line_stripped.startswith("#"):

					lines.append({"spaces": total_lpad(line), "name": line_stripped})

			# at this point we have a list of dict representing each line in the schema
			# which is in tree form.
			# loop through each line
			# if the spaces are zero, then, it belongs to the root node
			# otherwise, loop backwards starting at the previous line in the list
			# and look for the first line (node) where the spaces are less than
			# the current line (node). that would be the parent node.

			for main_index in range(len(lines)):

				# print("------------------------------------")
				# print(f"{main_index}  {lines[main_index]['spaces']} {lines[main_index]['name']}")

				if lines[main_index]["spaces"] == 0:

					lines[main_index]["dir"] = self.sub_directory(lines[main_index]["name"])

				else:

					# print("         searching backwards")

					for index_going_backwards in range(main_index - 1, -1, -1):

						# print(f"               {main_index} {index_going_backwards} => {lines[index_going_backwards]['spaces']} {lines[index_going_backwards]['name']}  vs {lines[main_index]['spaces']} {lines[index_going_backwards]['name']}")


						if lines[index_going_backwards]["spaces"] < lines[main_index]["spaces"]:

							# print(f"                       found: {lines[index_going_backwards]['name']} parent to -> {lines[main_index]['name']}")

							lines[main_index]["dir"] = lines[index_going_backwards]["dir"].sub_directory(lines[main_index]["name"])

							break





