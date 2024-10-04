
class Node:
	def __init__(self):
		self.node_color = (0, 0, 255) 


	def create_node():
		# Create a new .md file
		base_name = "title.md"
		file_name = "title.md"
		index = 1
		while os.path.exists(file_name):
			file_name = f"{base_name[:-3]}{index}.md"
			index += 1
		with open(file_name, 'w', encoding='utf-8') as file:
			file.write("""test""")


###############################################################################################

# Create and draw a new node
def create_node():
	# Create a new .md file
	base_name = "title.md"
	file_name = "title.md"
	index = 1
	while os.path.exists(file_name):
		file_name = f"{base_name[:-3]}{index}.md"
		index += 1
	with open(file_name, 'w', encoding='utf-8') as file:
		file.write("""test""")


def delete_node():
	try:
		os.remove()
	except FileNotFoundError:
		print("File not found")


# Update the node file path when title is changed 
def update_node_title():
	pass


# Input text on a node 
def edit_node(node):
	with open(node, 'w', encoding='utf-8') as file:
		file.writelines(""" """) 


def read_json():
	with open('nodes.json', 'r') as file:
		data = json.load(file)
	print(data)