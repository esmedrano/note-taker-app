# Contains: tab container bar, sidebar, 
import os
import pygame as pg
import config 
from nodes import Node


# This is a singleton class meaning only one instance exists
# Every time a new instance is declared it just accesses the first one
# Also, only the first instance declaration initializes the variables
# When a second instance declaration is called to access the first instance, 
# it does not reinitialize the variables and instead keeps the current value,
# allowing the values to be passed to other files 
class Elements:
	# Stores the single instance of the Elements class
	_instance = None  


	# Run when a new instance is created to ensure only one instance exists
	def __new__(cls):
		# If an instance has not been created
		if cls._instance is None:  
			# Create new instance
		    cls._instance = super(Elements, cls).__new__(cls)
		# Return cls._instance as new instance 
		return cls._instance


	def __init__(self):
		# Only initialize one time. If one variable is initialized so are all the others 
		if not hasattr(self, 'header_rect_h'):  
			# Class instances 
			self.node = Node()

			# Pygame shapes as ui elements
			self.header_rect_h = 35
			self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)
			self.sidebar_w = 200
			self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)
			self.workspace_rect = pg.Rect(self.sidebar_w, self.header_rect_h, config.window_x, config.window_y)

			# File button initialization
			self.file_button_h = 20
			self.file_button_rects = []
			self.file_button_hover_states = {}

			# Sidebar redraws
			self.sidebar_redraws = 0

			# Popup buttons
			self.collide = False
			self.popup_button_rects = []
			self.popup_button_hover_states = {}
			self.popup_buttons = []
			self.rt_click_pos = None
			self.popup_button_h = 30
			self.popup_w = 200
			self.popup_h = None
			self.popup_button_w = self.popup_w
			self.popup_redraws = 0
			

	# Header for displaying tabs 
	def draw_header(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)

		# Header bar background  
		pg.draw.rect(config.window, config.header_c, self.header_rect)

		# Font 
		font = pg.font.Font(None, 24)
		
		# Button text
		file_text = font.render("file", True, config.header_text_c)
		config.window.blit(file_text, (10, 10))


	def draw_sidebar(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)

		# sidebar background  
		pg.draw.rect(config.window, config.sidebar_c, self.sidebar_rect)


	def draw_workspace(self):
		# Rebuild workspace rect here bc __init__ doesn't catch window_x resize
		self.workspace_rect = pg.Rect(self.sidebar_w, self.header_rect_h, config.window_x, config.window_y)

		# Draw workspace
		pg.draw.rect(config.window, config.workspace_c, self.workspace_rect)


	def draw_sidebar_buttons(self):
		font = pg.font.Font(None, 24)
		self.file_button_rects.clear()

		# Only proceed if the "node markdown files" folder exists 
		folder = config.node_md_folder
		if os.path.exists(folder) and os.path.isdir(folder):

			# Collect node file names from folder every time main loop iterates
			self.node_file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

			# Draw buttons on sidebar display where each new button is below the last 
			button_count = 0
			for file_name in self.node_file_names:
				# Y possition of each button is offset from the height of the previous buttons (button_h * i) 
				# and the height of the header bar
				file_button_y = self.file_button_h * button_count + self.header_rect[3]

				# Save the button rectangles for later
				new_button_rect = pg.Rect(0, file_button_y, self.sidebar_rect[2], self.file_button_h)
				
				# This list is cleard and rebuilt the sidebar is drawn 
				self.file_button_rects.append([file_name, new_button_rect])

				if file_name not in self.file_button_hover_states:
					self.file_button_hover_states[file_name] = False
				
				# If the mouse cursor is hovered over the current button in the for loop, draw it with different the hover color
				if self.file_button_hover_states[file_name] == True:
					pg.draw.rect(config.window, config.button_hover_c, new_button_rect)
				# Or draw the button with the normal color 
				else:   
					pg.draw.rect(config.window, config.button_c, new_button_rect)

				config.window.blit(font.render(file_name, True, config.sidebar_text_c), (10, file_button_y + 3))

				# Increment the button count 
				button_count += 1
				
		self.sidebar_redraws += 1


	# Shade any group of buttons by passing: 
	# - the function that draws them 
	# - mouse position 
	# - button rectanges ["button name", pg.Rect()]
	# - hover states {"button name", True} 
	def shade_hovered_buttons(self, redraw_function, mouse_pos, button_rects, hover_states):
		for button in button_rects:
					
			button_name = button[0]
			button_rect = button[1]
	
			if button_rect.collidepoint(mouse_pos):
				self.collide = True
				hover_states[button_name] = True
				redraw_function()
				pg.display.update()
			else:
				hover_states[button_name] = False

		if all(not value for value in hover_states.values()) and self.collide:			
			redraw_function()
			pg.display.update()
			self.collide = False


	# Draw the button names created in the popup loop
	def draw_popup_buttons(self):
		font = pg.font.Font(None, 18)
		self.popup_button_rects.clear()

		button_count = 0
		for button in self.popup_buttons:
			# Y possition of each button is offset from the height of the previous buttons (button_h * i) 
			# and the height of the header bar
			button_y = self.rt_click_pos[1] + self.popup_button_h * button_count

			# Save the button rectangles for later
			new_button_rect = pg.Rect(self.rt_click_pos[0], button_y, self.popup_button_w, self.popup_button_h)
			
			# This list is cleard and rebuilt the sidebar is drawn 
			self.popup_button_rects.append([button, new_button_rect])

			if button not in self.popup_button_hover_states:
				# Add a new dictionary item
				self.popup_button_hover_states[button] = False
			
			# If the mouse cursor is hovered over the current button in the for loop, draw it with different the hover color
			if self.popup_button_hover_states[button] == True:
				pg.draw.rect(config.window, config.popup_hover_c, new_button_rect)
			# Or draw the button with the normal color 
			else:   
				pg.draw.rect(config.window, config.popup_c, new_button_rect)

			config.window.blit(font.render(button, True, config.popup_text_c), (self.rt_click_pos[0] + 30, button_y + 7))

			# Increment the button count 
			button_count += 1

	
	# Create the button names for new popup instances
	def popup_loop(self, clock, type, rt_click_pos, draw, ui, element_clicked):
		# Create a miniture game loop to draw the popup over the screen 
		# This avoids having create a bunch of do not update conditions for whatever it draws over 
		# For example, if the popup draws over the file buttons, the file buttons will imidatly draw back over the popup
		# They are triggered by the mouse being in the sidebar 
		# Could also be useful to avoid having to redraw a large graph window when using a node popup 
		self.rt_click_pos = rt_click_pos

		in_popup = True
		while in_popup:
			# Slow down the while loop to limit cpu usage
			clock.tick(60)

			for event in pg.event.get():
				if event.type == pg.QUIT:
					quit()

			# Mouse states
			mouse_pos = pg.mouse.get_pos()
			mouse_clicks = pg.mouse.get_pressed()

			# Build popup buttons based on popup type 
			if type == "file button":
				self.popup_buttons = ["delete file", "test button 1", "test button 2"]
				self.draw_popup_buttons()

				# The popup rect is used to detect mouse clicks that occur inside the popup, but can be replaced by iterating the popup button rects for collisions  
				self.popup_h = len(self.popup_buttons) * self.popup_button_h

				# Detect popup button clicks for each button
				for popup_button in self.popup_button_rects:

					# Each button has a list of characteristics
					popup_button_name = popup_button[0]
					popup_button_rect = popup_button[1]

					if popup_button_rect.collidepoint(mouse_pos) and mouse_clicks[0]:
						if popup_button_name == "delete file":
							# Delete file
							self.node.delete_node(element_clicked)

							# The button hover state is used to click the button
							# If the file is deleted the button must be removed from the hover states list 
							# That way the correct button can be selected next time one is deleted  
							self.file_button_hover_states.pop(element_clicked)
							draw.draw_app()
							return

			if type == "empty workspace":
				self.popup_buttons = ["new file", "open file"]
				self.draw_popup_buttons()
				self.popup_h = len(self.popup_buttons) * self.popup_button_h

			ui.shade_hovered_buttons(self.draw_popup_buttons, mouse_pos, self.popup_button_rects, self.popup_button_hover_states)

			# Exit the loop to the main loop if right mouse button pressed down 
			if mouse_clicks[2]:
				# Redraw the screen to erase the popup from wherever it is at 
				draw.draw_app()
				in_popup = False

			# Create the popup rectangle
			popup_rect = pg.Rect(rt_click_pos[0], rt_click_pos[1], self.popup_w, self.popup_h)

			# Exit loop to the main app loop if right click detected outside of the popup 
			if not popup_rect.collidepoint(mouse_pos) and mouse_clicks[0]:
				# Redraw the screen to erase the popup from wherever it is at 
				draw.draw_app()
				in_popup = False

			self.popup_redraws += 1
