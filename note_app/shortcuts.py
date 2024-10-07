import json


def get_shortcuts():
	with open('keyboard_shortcuts.json', 'r') as file:
			data = json.load(file)
	shortcuts = data['shortcuts']
	return shortcuts
