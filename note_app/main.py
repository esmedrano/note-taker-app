# Dependencies
import pygame as pg
import pygame_gui as pgg
import os
import json
import random as rand

# Application code modules 
import init
import user_interface
import graph
import note_app_nodes
import shortcut_functionality
import overclock
import test

pg.init()

bg_color = (150, 150, 150) 


def main():
	### CODE FROM OTHER FILES ###
	# UI class from user_interface.py
	ui = user_interface.Elements()
	node = note_app_nodes.Node()
	### CODE FROM OTHER FILES ###

	shortcuts_list = shortcut_functionality.get_shortcuts()
	
	space_bar_pressed = False
	space_count = 0
	is_overclocking = False

	is_running = True
	while is_running:
		# This keeps the code from straining the cpu 
		init.tick_clock()

		# Event handling
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False
			
			# Update the window size variables when window is resized
			if event.type == pg.VIDEORESIZE:
				init.update_screen_size(event.w, event.h)
			
			# Key press events
			if event.type == pg.KEYDOWN:
				keys = pg.key.get_pressed()	

				if keys[pg.K_SPACE]:
					space_count += 1
					if space_count % 2 != 0:
						is_overclocking = True
					else:
						is_overclocking = False

				# Check for keyboard shortcut key strokes 
				# shortcuts_list = [ [[][][]], [["shortcut name"], [l_ctrl + n], [r_ctrl + n]], ...  ]
				# If I put this into a function in another file I'll have to import all the functions that the shortcuts call into that same file 
				for shortcut in shortcuts_list:
					if shortcut[0] == "create new node":  
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								node.create_node()
								ui.populate_sidebar(node.node_titles)
					
					if shortcut[0] == "shortcut two":
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("a")

					if shortcut[0] == "shortcut three":		 
						for key_combo in shortcut[1:]:							
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("z")

			# Button logic
			# if event.type == pgg.UI_BUTTON_PRESSED:
			# 	if event.ui_element == hello_button:
			# 		print('Hello world')

			# UI events
			init.manager.process_events(event)

		# Set background colors
		init.window.fill(bg_color)

		# Build non pygame_gui elements 
		ui.draw_header()   
		ui.draw_sidebar()  # This can't be built anywhere else (event for loop, outside of while loop) for reasons that are beyond me  
		
		# Some UI elements require a timer
		init.manager.update(init.time_delta)
		# Draw UI elements 
		init.manager.draw_ui(init.window)

		# Function toggle section 
		if is_overclocking:
			overclock.overclock()

		# Update the screen
		pg.display.update()
		
		
if __name__ == "__main__":
	main()
	pg.quit()
