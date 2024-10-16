import pygame as pg
import os
import json
import random as rand

# Import class from file
import config
from user_interface import Elements
from nodes import Node

# Import function files
import overclock
import shortcuts 
import circle

pg.init()

clock = pg.time.Clock()


def main():
	# Class instances
	ui = Elements()
	node = Node()

	# Load shortcuts
	shortcuts_list = shortcuts.get_shortcuts()
	
	# Space bar overclock switch
	space_bar_pressed = False
	space_count = 0
	is_overclocking = False

	# If else gate variables 
	node_folder_exists = False
	files_rect_accessed = False

	#### TEMPS
	w_drawn = False		
	radius = 10

	drawn = False
	is_running = True
	while is_running:
		# IMPORTANT: This keeps the code from straining the cpu 
		clock.tick(60)

		# Draw the screen the first time
		if not drawn:
			ui.draw_header()
			ui.draw_sidebar()
			ui.draw_workspace()
			ui.draw_sidebar_buttons()   

			# Save a buffer to the buffer surface
			window_save_state = pg.Surface(config.window.get_size())
			window_save_state.blit(config.window, (0, 0))

			circle.draw(radius)

			drawn = True

		# Check if overclock() is toggled on 
		if is_overclocking:
			# REFRESH_SCREEN: both draw method and blit method are slow 
			config.window.blit(window_save_state, (0, 0))

			overclock.overclock()
			pg.display.update()

		# Get mouse cursor position 
		mouse_pos = pg.mouse.get_pos()
		mouse_buttons_pressed = pg.mouse.get_pressed()

		# Check node files for deletions 
		folder = config.node_md_folder
		if os.path.exists(folder) and os.path.isdir(folder):
			# If the node folder exists get the file names
			# The node folder exists for the current screen redraw
			node_folder_exists = True

			# Collect node file names from folder every time inner loop iterates
			fresh_file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

			# Check if the current file_names matches the ui.file_names created in the first screen draw
			for title in ui.node_file_names:
				# Redraw the screen if ui.file_names needs to be updated 
				if title not in fresh_file_names:
					# Redraw sidebar files
					ui.draw_sidebar()
					ui.draw_sidebar_buttons()
					pg.display.update()
		elif node_folder_exists:
			# If the node folder doesn't exist but it used to then redraw the screen with no files
			ui.draw_sidebar()
			ui.draw_sidebar_buttons()
			pg.display.update()
			# Lock the elif statement 
			node_folder_exists = False
		
		# Shade the hovered file button if the mouse is in the file buttons rect   				
		if ui.files_rect.collidepoint(mouse_pos) and not ui.popup_rect.collidepoint(mouse_pos):
			files_rect_accessed = True
			ui.shade_hovered_buttons(ui.draw_sidebar_buttons, mouse_pos, ui.file_button_rects, ui.file_button_hover_states)
		elif files_rect_accessed:
			# If mouse is not in the files rect but it was before, unshade the button that was shaded last when the mouse left the files rect
			ui.shade_hovered_buttons(ui.draw_sidebar_buttons, mouse_pos, ui.file_button_rects, ui.file_button_hover_states)
			ui.draw_sidebar_buttons()
			# Lock the elif statement 
			files_rect_accessed = False

		# Shade the hovered popup button if the mouse is in the popup rect
		if ui.popup_rect.collidepoint(mouse_pos):
			ui.shade_hovered_buttons(ui.draw_popup, mouse_pos, ui.popup_button_rects, ui.popup_button_hover_states)

		# Draw the popup
		if ui.popup_active:
			# Draw the file button popup at the right click posisition
			ui.draw_popup()
			pg.display.update()

		# Draw the node text to the workspace
		if not node.is_drawn and node.is_open:
			pass

		if node.text_entry_active:
			node.text_entry(mouse_pos, mouse_buttons_pressed)

################################################################ EVENT HANDLING ################################################################
		
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False

				print("\n# of header redraws: ", ui.header_draws)
				print("\n# of workspace redraws: ", ui.workspace_draws)
				print("\n# of sidebar redraws: ", ui.sidebar_draws)
				print("\n# of sidebar button redraws: ", ui.sidebar_button_draws)
				print("\n# of popup redraws: ", ui.popup_draws)
				print("\n# of popup button redraws: ", ui.popup_button_draws)
				print("\n# of shade_hovered_buttons() calls: ", ui.buttons_shaded) 
				print("\n")
			
			# Update the window dimension variables when window is resized
			if event.type == pg.VIDEORESIZE:
				config.window_x = event.w
				config.window_y = event.h
				
				# Save a buffer to the buffer surface
				window_save_state = pg.Surface(config.window.get_size())
				window_save_state.blit(config.window, (0, 0))

				# Redraw screen to adjust ui element dimensions
				drawn = False

			# Mouse button events
			if event.type == pg.MOUSEBUTTONUP:
				# If right click
				if event.button == 3:
					if ui.sidebar_rect.collidepoint(mouse_pos):
						# Check for file_button clicks by iterating the button hover state list and detecting the release of the right mouse button  
						# Create a copy of the hover states because deletion from dictionaries being iterated is not allowed
						for button, state in ui.file_button_hover_states.copy().items():
							# The button has been right clicked while hovered, so open the popup
							if state:
								# Save the buffer to the surface
								config.window_save_state.blit(config.window, (0, 0))
								
								button_with_popup = button
								ui.popup_type = "file button"
								ui.rt_click_pos = mouse_pos
								ui.popup_active = True

					# If in the workspace rect 
					if ui.workspace_rect.collidepoint(mouse_pos):
						ui.popup_type = "empty workspace"
						ui.rt_click_pos = mouse_pos
						ui.popup_active = True 

			if event.type == pg.MOUSEBUTTONDOWN:
				
				# If in ui.files_rect
				if ui.sidebar_rect.collidepoint(mouse_pos) and not ui.popup_active: 
					if event.button == 1:
						print("\nLeft click detected inside sidebar!") 
						# For all file buttons
						for button, state in ui.file_button_hover_states.items(): 
							# If the button is hovered
							if state:
								# Reset the color of any previously selected button
								ui.file_button_select_states[ui.selected_button] = False

								# Set the select state of the selected button to True
								ui.selected_button = button
								ui.file_button_select_states[ui.selected_button] = True

								# Redraw the sidebar to reflect change
								ui.draw_sidebar_buttons()

								# If file extension is .md
								if button[-3:] == ".md":
									# Open the node.md file
									# REFRESH_WORKSPACE
									node.open(button)
									ui.draw_workspace()
									node.draw_text()

				# If in workspace
				if ui.workspace_rect.collidepoint(mouse_pos) and not ui.popup_active:
					if event.button == 1:	
						print("\nLeft click detected inside workspace!")
						if node.is_open == True:

							if not w_drawn:
								for y in [*range(ui.header_h + node.margin_y, config.window_y, node.font_size)]:
									pg.draw.line(config.window, (0, 0, 0), (ui.sidebar_w, y), (config.window_x, y))
									#pg.draw.rect(config.window, (0, 0, 0), (ui.sidebar_w + node.node_margin, y - rect[3], rect[2], rect[3]))
									#config.window.blit(file_text, (ui.sidebar_w + node.margin_x, y - rect[3]))
									pg.display.update()
								w_drawn = True

				# If in popup
				if ui.popup_rect.collidepoint(mouse_pos):
					if event.button == 1:
						# Detect popup button clicks for each button
						for popup_button in ui.popup_button_rects:

							# Each button has a list of characteristics [name, rect]
							popup_button_name = popup_button[0]
							popup_button_rect = popup_button[1]

							# Detect if the mouse is clicked in the current popup button 
							if popup_button_rect.collidepoint(mouse_pos):
								print(popup_button_name, "clicked")
								if popup_button_name == "delete file":
									# If delete is selected, the popup can be exited and the rectangle reset
									ui.popup_active = False
									ui.popup_rect = pg.Rect(0, 0, 0, 0)

									node.delete(button_with_popup)

									# The button hover state is used to click the button
									# If the file is deleted the button hover state must be removed from the list 
									# That way the correct button is deleted next time  
									ui.file_button_hover_states.pop(button_with_popup)

									# REFRESH_SCREEN
									config.window.blit(config.window_save_state, (0, 0))
							
								# if popup_button_name == "test button 1":
								# 		# If delete is selected, the popup can be exited and the rectangle deleted
								# 		ui.popup_active = False
								# 		ui.popup_rect = pg.Rect(0, 0, 0, 0)

								# 		# REFRESH_SCREEN
								# 		#ui.draw_workspace()
								# 		node.is_drawn = False
								# 		ui.draw_sidebar()
								# 		ui.draw_sidebar_buttons()
								
								# if popup_button_name == "test button 2":
								# 		# If delete is selected, the popup can be exited and the rectangle deleted
								# 		ui.popup_active = False
								# 		ui.popup_rect = pg.Rect(0, 0, 0, 0)

								# 		# REFRESH_SCREEN
								# 		#ui.draw_workspace()
								# 		node.is_drawn = False
								# 		ui.draw_sidebar()
								# 		ui.draw_sidebar_buttons()

				# If mouse pressed outside of popup, refresh screen
				if not ui.popup_rect.collidepoint(mouse_pos) and ui.popup_active:
					if event.button == 1:
						ui.popup_active = False
						ui.popup_rect = pg.Rect(0, 0, 0, 0)
						
						# REFRESH_SCREEN
						ui.draw_workspace()
						node.is_drawn = False
						ui.draw_sidebar()
						ui.draw_sidebar_buttons()
								
			# Key press events
			if event.type == pg.KEYDOWN:
				keys = pg.key.get_pressed()	

				# Toggle overclock() if spacebar is pressed
				if keys[pg.K_SPACE]:
					space_count += 1
					if space_count % 2 != 0:
						is_overclocking = True
					else:
						is_overclocking = False
						# REFRESH_SCREEN
						config.window.blit(window_save_state, (0, 0))

				# If entering text
				if node.text_entry_active:
					if keys[pg.K_RETURN]:
						pass
						# Create new line

					elif keys[pg.K_BACKSPACE]:
						if node.text_cursor_index != 0:
							node.text = node.text[:node.text_cursor_index - 1] + node.text[node.text_cursor_index:]
							node.text_cursor_index -= 1
						elif node.text_cursor_line != 0:
							node.text_cursor_line -= 1 
						else:
							pass

					elif keys[pg.K_LEFT]:
						if node.text_cursor_index > 0:
							node.text_cursor_index -= 1
						elif node.text_cursor_line > 0:
							node.text_cursor_line -= 1
						else: 
							pass

					elif keys[pg.K_RIGHT]:
						node.text_cursor_index += 1

					elif keys[pg.K_DOWN]:
						node.text_cursor_line -= 1

					elif keys[pg.K_UP]:
						node.text_cursor_line += 1

					elif keys[pg.K_RCTRL] or keys[pg.K_LCTRL]:
						pass
						
					# Else detects any other keys including space 
					else:	
						node.text = node.text[:node.text_cursor_index] + event.unicode + node.text[node.text_cursor_index + 1:]
						node.text_cursor_index += 1

				print(node.text)
			
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

					if shortcut[0] == "save node":  
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								node.save()
					
					if shortcut[0] == "shortcut two":
						for key_combo in shortcut[1:]:
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("a")

					if shortcut[0] == "shortcut three":		 
						for key_combo in shortcut[1:]:							
							if all(keys[getattr(pg, key)] for key in key_combo):
								print("z") 
	
		pg.display.update()


if __name__ == "__main__":
	main()
	pg.quit()
