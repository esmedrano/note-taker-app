import os
import shutil 


class Node:
	def __init__(self):
		self.node_color = (0, 0, 255) 
		self.nodes = []


	def save_node_to_folder(self, node_file_name):
		# Set folder name
		folder = "node_markdown_files"
	    # Create folder
		os.makedirs(folder, exist_ok=True)
		# Add node to folder
		file_path = os.path.join(folder, node_file_name)
		shutil.move(node_file_name, file_path)


	def create_node(self):
		# Define the default file name
		file_name_holder = "title.md"

		# Define the node.md folder
		folder = "node_markdown_files"

		# Create the node.md folder
		os.makedirs(folder, exist_ok=True)

		# Set initial file name and construct the full path
		file_name = file_name_holder
		file_path = os.path.join(folder, file_name)

		# Check if the file exists in the folder, and if it does, rename it with an index
		index = 1
		while os.path.exists(file_path):
		    # Rename the file if the previous value for file_name exists
		    file_name = f"{file_name_holder[:-3]}{index}.md"  # Remove ".md" and append index
		    
		    # Redefine the path if the previous value for file_path exists
		    file_path = os.path.join(folder, file_name)
		    
		    # Index for the copied file name 
		    index += 1

		# Create and write to the file in the specified folder
		with open(file_path, 'w', encoding='utf-8') as file:
		    file.write("test")

		# Append the new file path to nodes 
		self.nodes.append(file_name)


###############################################################################################


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