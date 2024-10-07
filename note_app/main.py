# Dependencies
import pygame as pg
import os
import json
import random as rand

# Application code modules 
import config
import user_interface
import nodes
import draw_display
import shortcuts

clock = pg.time.Clock()

pg.init()

# # Draw the basic UI 
# def redraw(ui, radius, is_overclocking):
# 	global screen_redraws 
# 	# Set background colors
# 	config.window.fill(bg_color)

# 	# Build non pygame_gui elements 
# 	ui.draw_header()
# 	ui.draw_sidebar()
# 	ui.draw_sidebar_buttons()	

# 	pg.draw.circle(config.window, (0, 0, 255), (300, 200), radius)

# 	if is_overclocking:
# 		overclock.overclock()

# 	pg.display.update()
# 	screen_redraws += 1
# 	print("Screen redraws: ", screen_redraws)


def main():
	### CODE FROM OTHER FILES ###
	# Class instances
	ui = user_interface.Elements()
	node = nodes.Node()
	redraw_display = draw_display.Draw()

	shortcuts_list = shortcuts.get_shortcuts()
	### CODE FROM OTHER FILES ###

	space_bar_pressed = False
	space_count = 0
	is_overclocking = False

	radius = 10

	is_running = True
	while is_running:
		# Draw everything needed to use application one time 
		# Then enter the inner while loop to parse for user input
		
		redraw_display.draw(ui)
		
		# Used to check if nodes folder has been deleted
		node_folder_exists = False

		# Use inner while loop to parse for user input and only exit to redraw
		parsing = True
		while parsing: 
			# IMPORTANT: This keeps the code from straining the cpu 
			time = clock.tick(60)

			# Get mouse cursor position 
			mouse_cursor = pg.mouse.get_pos()

			# Parse node files for deletions 
			folder = config.node_md_folder
			if os.path.exists(folder) and os.path.isdir(folder):
				node_folder_exists = True
				# Collect node file names from folder every time inner loop iterates
				file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

				# Check if the current file_names matches the ui.file_names created in the first ui.draw_sidebar_buttons()
				for title in ui.file_names:
					# Redraw the screen if the file_names needs to be updated 
					if title not in file_names:
						ui.draw_sidebar_buttons() 
						# Exit inner loop to redraw screen
						parsing = False

			# If the node folder doesn't exist but it used to 
			else:
				# This is true if the node folder used to exist in the above if statement 
				if node_folder_exists == True:
					# Redraw screen yet again... but only once
					ui.draw_sidebar_buttons() 
					# Exit inner loop to redraw screen
					parsing = False

					# Set to false to avoid redrawing the screen every iteration because the folder doesn't exist 
					node_folder_exists = False

			# If this is true the screen will need to be redrawn every iteration of the inner loop. Observe CPU usage 
			if redraw_display.is_overclocking:
				# Exit inner loop to redraw screen
				parsing = False

			# Check if buttons are pressed
			ui.get_pressed_buttons(ui, redraw_display)
			



################################################################ EVENT HANDLING ################################################################
			for event in pg.event.get():
				if event.type == pg.QUIT:
					is_running = False
					# Exit inner loop to redraw screen
					parsing = False
				
				# Update the window size variables when window is resized
				if event.type == pg.VIDEORESIZE:
					config.update_screen_size(event.w, event.h)
					# Exit inner loop to redraw screen
					parsing = False

				# Key press events
				if event.type == pg.KEYDOWN:
					keys = pg.key.get_pressed()	

					# Toggle overclock() if spacebar is pressed
					if keys[pg.K_SPACE]:
						space_count += 1
						if space_count % 2 != 0:
							redraw_display.is_overclocking = True
						else:
							redraw_display.is_overclocking = False
							# Exit inner loop to redraw screen. Erases the last draw of the overclock function 
							parsing = False

					# Decrease circle radius by pressing m
					if keys[pg.K_m]: 
						redraw_display.radius -= 3
						# Exit inner loop to redraw screen
						parsing = False

					# Increase circle radius by pressing m
					if keys[pg.K_p]: 
						redraw_display.radius += 3
						# Exit inner loop to redraw screen
						parsing = False

					# Check for keyboard shortcut key strokes 
					# shortcuts_list = [ [[][][]], [["shortcut name"], [l_ctrl + n], [r_ctrl + n]], ...  ]
					# If I put this into a function in another file I'll have to import all the functions that the shortcuts call into that same file 
					for shortcut in shortcuts_list:
						if shortcut[0] == "create new node":  
							for key_combo in shortcut[1:]:
								if all(keys[getattr(pg, key)] for key in key_combo):
									node.create_node()
									# Exit inner loop to redraw screen
									parsing = False
						
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
