# Contains: tab container bar, sidebar, 
import os
import pygame as pg
import config 


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
		if not hasattr(self, 'header_h'):  
			# Pygame shapes as ui elements
			self.header_h = 35
			self.header_rect = pg.Rect(0, 0, config.window_x, self.header_h)
			self.sidebar_w = 200
			self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)
			self.workspace_rect = pg.Rect(self.sidebar_w, self.header_h, config.window_x, config.window_y)

			# Sidebar file buttons initialization
			self.file_button_h = 20

			self.node_file_names = []
			self.file_button_rects = []
			self.files_rect = pg.Rect(0, 0, 0, 0)

			self.file_button_hover_states = {}			
			self.file_button_select_states = {}
			self.selected_button = None

			# Popup initialization
			self.popup_active = False
			self.in_popup = False

			self.mouse_pos = None
			self.rt_click_pos = None
			self.collide = False

			self.popup_button_rects = []
			self.popup_button_hover_states = {}
			self.popup_buttons = []

			self.popup_button_h = 30
			self.popup_w = 200
			self.popup_h = None

			self.popup_button_w = self.popup_w
			self.popup_rect = pg.Rect(0, 0, 0, 0)
			self.popup_redraws = 0

			# Draw counters
			self.header_draws = 0
			self.workspace_draws = 0
			self.sidebar_draws = 0
			self.sidebar_button_draws = 0
			self.popup_draws = 0
			self.popup_button_draws = 0
			self.buttons_shaded = 0
			

	# Header for displaying tabs 
	def draw_header(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.header_rect = pg.Rect(0, 0, config.window_x, self.header_h)

		# Header bar background  
		pg.draw.rect(config.window, config.header_c, self.header_rect)

		# Font 
		font = pg.font.Font(None, 24)
		
		# Button text
		file_text = font.render("file", True, config.header_text_c)
		config.window.blit(file_text, (10, 10))

		self.header_draws += 1
		print("Header draws: ", self.header_draws)


	def draw_workspace(self):
		# Rebuild workspace rect here bc __init__ doesn't catch window_x resize
		self.workspace_rect = pg.Rect(self.sidebar_w, self.header_h, config.window_x - self.sidebar_w, config.window_y - self.header_h)

		# Draw workspace
		pg.draw.rect(config.window, config.workspace_c, self.workspace_rect)

		self.workspace_draws += 1
		print("Workspace draws: ", self.workspace_draws)


	def draw_sidebar(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)

		# sidebar background  
		pg.draw.rect(config.window, config.sidebar_c, self.sidebar_rect) 

		self.sidebar_draws += 1
		print("Sidebar_redraws: ", self.sidebar_draws)


	def draw_sidebar_buttons(self):
		font = pg.font.Font(None, 24)

		self.file_button_rects.clear()

		# Only proceed if the "node markdown files" folder exists 
		folder = config.node_md_folder
		if os.path.exists(folder) and os.path.isdir(folder):

			# Collect node file names from folder every time this function is called 
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

				# Create the hover and select states lists
				if file_name not in self.file_button_hover_states:
					self.file_button_hover_states[file_name] = False
				if file_name not in self.file_button_select_states:
					self.file_button_select_states[file_name] = False
				
				# If the mouse cursor is hovered or selected, draw with the appropriate color 
				if self.file_button_hover_states[file_name] and not self.file_button_select_states[file_name]:
					pg.draw.rect(config.window, config.button_hover_c, new_button_rect)
				elif self.file_button_select_states[file_name]:
					pg.draw.rect(config.window, config.button_select_c, new_button_rect)
				# Or draw the button with the normal color 
				else:   
					pg.draw.rect(config.window, config.button_c, new_button_rect)

				config.window.blit(font.render(file_name, True, config.sidebar_text_c), (10, file_button_y + 3))

				# Increment the button count 
				button_count += 1

			# Create a rectangle the same size as all the file buttons 
			if len(self.node_file_names) != 0:
				files_rect_x = self.file_button_rects[0][1][0] 
				files_rect_y = self.file_button_rects[0][1][1]
				files_rect_w = self.file_button_rects[0][1][2]
				files_rect_h = self.file_button_rects[0][1][3] * button_count

				self.files_rect = pg.Rect(files_rect_x, files_rect_y, files_rect_w, files_rect_h)

		self.sidebar_button_draws += 1
		print("Sidebar button draws: ", self.sidebar_button_draws)


	def draw_popup(self):
		# Build popup buttons based on popup type 
		if self.popup_type == "file button":
			self.popup_buttons = ["delete file", "test button 1", "test button 2"]
		if self.popup_type == "empty workspace":
			self.popup_buttons = ["new file", "open file"]

		# Draw the buttons and create the button rect and button hover state lists or the appropriate popup type
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
			
			# If the mouse cursor is hovered over the current button in the for loop, draw it with the hover color
			if self.popup_button_hover_states[button] == True:
				pg.draw.rect(config.window, config.popup_hover_c, new_button_rect)
			# Or draw the button with the normal color 
			else:   
				pg.draw.rect(config.window, config.popup_c, new_button_rect)

			config.window.blit(font.render(button, True, config.popup_text_c), (self.rt_click_pos[0] + 30, button_y + 7))

			# Increment the button count 
			button_count += 1

		# Popup_h is used to build the popup rect containng all popup buttons 
		self.popup_h = len(self.popup_buttons) * self.popup_button_h
		
		# Create the popup rectangle
		self.popup_rect = pg.Rect(self.rt_click_pos[0], self.rt_click_pos[1], self.popup_w, self.popup_h)

		self.popup_draws += 1
		print("Popup draws: ", self.popup_draws)


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
			
			# If the mouse cursor is hovered over the current button in the for loop, draw it with the hover color
			if self.popup_button_hover_states[button] == True:
				pg.draw.rect(config.window, config.popup_hover_c, new_button_rect)
			# Or draw the button with the normal color 
			else:   
				pg.draw.rect(config.window, config.popup_c, new_button_rect)

			config.window.blit(font.render(button, True, config.popup_text_c), (self.rt_click_pos[0] + 30, button_y + 7))

			# Increment the button count 
			button_count += 1

		self.popup_button_draws += 1
		print("Popup button draws: ", self.popup_button_draws)


	# Shade any group of buttons by passing: 
	# - the function that draws them 
	# - mouse position 
	# - button rectanges ["button name", pg.Rect()]
	# - hover states {"button name", True} 
	def shade_hovered_buttons(self, draw_button_function, mouse_pos, button_rects, button_hover_states):
		for button in button_rects:
					
			button_name = button[0]
			button_rect = button[1]
	
			if button_rect.collidepoint(mouse_pos):
				button_hover_states[button_name] = True
				draw_button_function()
			else:
				button_hover_states[button_name] = False

		self.buttons_shaded += 1
		print("Shaded buttons: ", self.buttons_shaded)