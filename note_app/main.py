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
	node_folder_exists = False

	redrawn = False

	drawn = False
	is_running = True
	while is_running:
		# Only redraw the screen when nessecary 
		if not drawn:
			draw.draw_app()
			drawn = True

		# IMPORTANT: This keeps the code from straining the cpu 
		time = clock.tick(60)

		# Get mouse cursor position 
		mouse_cursor_pos = pg.mouse.get_pos()

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
					# Redraw screen with if not drawn if statement
					drawn = False

		# If the node folder doesn't exist but it used to then redraw the screen with no files
		else:
			# This is true if the node folder used to exist in the above if statement 
			if node_folder_exists == True:
				# Redraw screen with if not drawn if statement
				drawn = False
				# Set to false to keep this parse exit closed 
				node_folder_exists = False

		# If this is true the screen will need to be redrawn every iteration of the inner loop. Observe CPU usage 
		if draw.is_overclocking:
			# Redraw screen with if not drawn if statement
			drawn = False

		# Check if buttons are pressed
		# io.get_pressed_buttons()
		collide = False
		for file_button in ui.file_button_rects:
					
			file_button_rect = file_button[1]
	
			if file_button_rect.collidepoint(mouse_cursor_pos):
				file_button[2] = 1
				collide = True
				redrawn = False
			else:
				file_button[2] = 0

		# Collide will only be true for this iteration unless the button stays hovered 
		if collide:
			draw.draw_app()
			pg.display.update()

		# Redraw one last time to take off button highlight 
		if not collide and not redrawn:
			draw.draw_app()
			pg.display.update()
			redrawn = True


################################################################ EVENT HANDLING ################################################################
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False
				# Redraw screen with if not drawn if statement
				drawn = False
				print("\n# of total redraws: ", draw.display_redraws, "\n# of sidebar file redraws: ", ui.sidebar_redraws)
				
			
			# Update the window dimension variables when window is resized
			if event.type == pg.VIDEORESIZE:
				config.window_x = event.w
				config.window_y = event.h
				
				# Redraw screen with if not drawn if statement
				drawn = False

			# Mouse button events
			if event.type == pg.MOUSEBUTTONUP:
				# Check for file_button hovering and clicks
				for file_button in ui.file_button_rects:
					
					file_button_rect = file_button[1]
					file_button_hovered = file_button[2]

					if file_button_rect.collidepoint(mouse_cursor_pos):
						file_button_hovered = 1
						#draw.draw_app()


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
