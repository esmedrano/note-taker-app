import json

def get_shortcuts():
	with open('keyboard_shortcuts.json', 'r') as file:
			data = json.load(file)

	create_new_node = data.get("create new node")
	shortcuts = [create_new_node]
	return shortcuts
