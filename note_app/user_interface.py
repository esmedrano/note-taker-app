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
		if not hasattr(self, 'header_rect_h'):  
			# Pygame shapes as ui elements
			self.header_rect_h = 35
			self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)
			self.sidebar_w = 200
			self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)

			# Button initialization
			self.file_button_h = 20
			self.file_button_rects = []

			# File names
			self.node_file_names = []

			# Redraws
			self.sidebar_redraws = 0
			

	# Header for displaying tabs 
	def draw_header(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)

		# header bar background  
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


	def draw_sidebar_buttons(self):
		font = pg.font.Font(None, 24)
		
		# Only proceed if the "node markdown files" folder exists 
		folder = config.node_md_folder
		if os.path.exists(folder) and os.path.isdir(folder):

			# Collect node file names from folder every time main loop iterates
			self.node_file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

			# Draw buttons on sidebar display where each new button is below the last 
			button_count = 0

			for title in self.node_file_names:
				# Y possition of each button is offset from the height of the previous buttons (button_h * i) 
				# and the height of the header bar
				file_button_y = self.file_button_h * button_count + self.header_rect[3]

				# Save the button rectangles for later
				new_button_rect = pg.Rect(0, file_button_y, self.sidebar_rect[2], self.file_button_h)
				
				if len(self.file_button_rects) < len(self.node_file_names):
					self.file_button_rects.append([title, new_button_rect, 0])

				# Draw the button  
				pg.draw.rect(config.window, config.button_c, new_button_rect)

				# If hovered draw with different color
				if self.file_button_rects[button_count][2] == 1:
					pg.draw.rect(config.window, config.button_hover_c, new_button_rect)

				config.window.blit(font.render(title, True, config.sidebar_text_c), (10, file_button_y + 3))

				# Increment the button count 
				button_count += 1
		self.sidebar_redraws += 1
		print("Sidebar redraws: ", self.sidebar_redraws)


	def right_click_popup(self):
		popup_rect = pg.Rect(config.window_x / 2, config.window_y / 2, 100, 50)
		pg.draw.rect(config.window, (200, 200 ,200), popup_rect)


	def shade_hovered_button(self):
		pass
