import pygame as pg
import os
import json
import random as rand

# Import class from file
import config
from draw_display import Draw
from user_interface import Elements
from nodes import Node

# Import function files
import overclock
import shortcuts 

clock = pg.time.Clock()

pg.init()


def main():
	# Class instances
	draw = Draw()
	ui = Elements()
	
	node = Node()

	shortcuts_list = shortcuts.get_shortcuts()
	
	space_bar_pressed = False
	space_count = 0

	# If else gate variables 
	node_folder_exists = False

	drawn = False
	is_running = True
	while is_running:
		# IMPORTANT: This keeps the code from straining the cpu 
		clock.tick(60)

		# Only redraw the screen when nessecary 
		if not drawn:
			draw.draw_app()
			drawn = True

		# Get mouse cursor position 
		mouse_pos = pg.mouse.get_pos()

		# Parse node files for deletions 
		folder = config.node_md_folder
		# If the node folder exists get the file names
		if os.path.exists(folder) and os.path.isdir(folder):
			# The node folder exists for the current screen redraw
			node_folder_exists = True

			# Collect node file names from folder every time inner loop iterates
			file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

			# Check if the current file_names matches the ui.file_names created in the first screen draw
			for title in ui.node_file_names:
				# Redraw the screen if the file_names needs to be updated 
				if title not in file_names:
					# Redraw sidebar files
					ui.draw_sidebar()
					ui.draw_sidebar_buttons()
					pg.display.update()

		# If the node folder doesn't exist but it used to then redraw the screen with no files
		else:
			# This is true if the node folder used to exist in the above if statement 
			if node_folder_exists == True:
				# Redraw screen with if not drawn if statement
				ui.draw_sidebar()
				ui.draw_sidebar_buttons()
				pg.display.update()
				# Set to false to keep this parse exit closed 
				node_folder_exists = False

		# If this is true the screen will need to be redrawn every iteration of the while loop Observe CPU usage 
		if draw.is_overclocking:
			# Redraw screen with if not drawn if statement
			drawn = False

		ui.shade_hovered_buttons(ui.draw_sidebar_buttons, mouse_pos, ui.file_button_rects, ui.file_button_hover_states)


################################################################ EVENT HANDLING ################################################################
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False
				# Redraw screen with if not drawn if statement
				drawn = False
				print("\n# of full window redraws: ", draw.display_redraws)
				print("\n# of sidebar redraws: ", ui.sidebar_redraws)
				print("\n# of popup redraws: ", ui.popup_redraws)
				print("\n")
			
			# Update the window dimension variables when window is resized
			if event.type == pg.VIDEORESIZE:
				config.window_x = event.w
				config.window_y = event.h
				
				# Redraw screen with if not drawn if statement
				drawn = False

			# Mouse button events
			if event.type == pg.MOUSEBUTTONUP:
				# If in the sidebar rect
				if ui.sidebar_rect.collidepoint(mouse_pos):
					print("\nClick detected inside sidebar!")
					# Check for file_button clicks by iterating the button hover state list 
					# It is crucial that the popup loop is called upon releaseing the mouse button 
					# Pressing the mouse button while in the popup loop exits the loop and allows the release event to trigger a new popup loop 
					
					# Create a copy of the hover states because deletion from dictionaries being iterated is not allowed
					for button, state in ui.file_button_hover_states.copy().items():
						if state:
							# If a button is right clicked open the popup
							if event.button == 3:
								print("\nFile right clicked: ", button)
								popup_type = "file button"
								ui.popup_loop(clock, popup_type, mouse_pos, draw, ui, button)

				# If in the workspace rect 
				if ui.workspace_rect.collidepoint(mouse_pos):
					print("\nClick detected inside workspace!")
					if event.button == 3:
						popup_type = "empty workspace"
						ui.popup_loop(clock, popup_type, mouse_pos, draw, ui, None) 

			# Key press events
			if event.type == pg.KEYDOWN:
				keys = pg.key.get_pressed()	

				# Toggle overclock() if spacebar is pressed
				if keys[pg.K_SPACE]:
					space_count += 1
					if space_count % 2 != 0:
						draw.is_overclocking = True
					else:
						draw.is_overclocking = False
						# Redraw screen with if not drawn if statement 
						drawn = False

				# Decrease circle radius by pressing m
				if keys[pg.K_m]: 
					draw.radius -= 3
					# Redraw screen with if not drawn if statement
					drawn = False

				# Increase circle radius by pressing m
				if keys[pg.K_p]: 
					draw.radius += 3
					# Redraw screen with if not drawn if statement
					drawn = False

				# Check for keyboard shortcut key strokes 
				# shortcuts_list = [ [[][][]], [["shortcut name"], [l_ctrl + n], [r_ctrl + n]], ...  ]
				# If I put this into a function in another file I'll have to import all the functions that the shortcuts call into that same file 
				for shortcut in shortcuts_list:
					if shortcut[0] == "create new node":  
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								node.create_node()
								# Redraw sidebar
								ui.draw_sidebar_buttons()
								pg.display.update()
					
					if shortcut[0] == "shortcut two":
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("a")

					if shortcut[0] == "shortcut three":		 
						for key_combo in shortcut[1:]:							
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("z") 
		
		
if __name__ == "__main__":
	main()
	pg.quit()
