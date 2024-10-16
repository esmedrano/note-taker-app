import os
import pygame as pg
import config
import user_interface


class Node:
	def __init__(self):
		self.ui = user_interface.Elements()

		self.node_titles = []
		self.folder = config.node_md_folder

		# Node states 
		self.is_open = False
		self.node_title = None
		self.is_drawn = False
		self.text_entry_active = False
		self.cursor_active = False


		### TEXT INITIALIZATION ### 

		# Text
		self.text = ""
		self.text_drawn = False

		# Workspace font
		self.font_size = 24
		self.title_font_size = 50 
		self.font_c = ((10,)*3)
		self.title_font = pg.font.Font(None, self.title_font_size)
		self.body_font = pg.font.Font(None, self.font_size)

		# Initial line position and width dimension. Height is different for the title and the body 
		self.line_surface_x = ui.workspace_rect[0] + self.margin_x 
		self.line_surface_y = ui.workspace_rect[1] + self.margin_y 
		self.line_surface_w = config.window_x - self.margin_x * 2
		self.line_surface_h = 0

		# Prebuilt title surface
		self.pg.Surface((self.line_rect_w, self.line_rect_h))

		# Workspace margins
		self.margin_x = 40
		self.margin_y = 50

		# Initial position of character surface in the line surface
		self.char_x = 0
		self.char_y = 0 

		# Initial renderer position where the first chararcter will be displayed in the line surface 
		self.renderer_x = 0
		self.renderer_y = 0

		# Initial cursor index
		self.text_cursor_index = 0
		self.text_cursor_line = 0

		# Storage for character and line surfaces and rects 
		# Each inner character list is a line. The first one is the title and the second the first line
		self.char_surfaces = [[], []]
		self.char_rects    = [[], []]

		self.line_surfaces = []  
		self.line_rects    = []
		
		# Line surface holder for buffering a copy of the line without the flashing cursor ?
		self.line_buffer = None


	def create_node(self):
		# Define the default file name
		file_name_holder = config.node_title

		# Create the node.md folder
		os.makedirs(self.folder, exist_ok=True)

		# Set initial file name and construct the full path
		file_name = file_name_holder
		file_path = os.path.join(self.folder, file_name)

		# Check if the file exists in the folder, and if it does, rename it with an index
		index = 1
		while os.path.exists(file_path):
		    # Rename the file if the previous value for file_name exists
		    file_name = f"{file_name_holder[:-3]}{index}.md"  # Remove ".md" and append index
		    
		    # Redefine the path if the previous value for file_path exists
		    file_path = os.path.join(self.folder, file_name)
		    
		    # Index for the copied file name 
		    index += 1

		# Create and write to the file in the specified folder
		with open(file_path, 'w', encoding='utf-8') as file:
		    file.write("test")


	# Initialize the opened node
	def open(self, node_title):
		# Get node title
		self.node_title = node_title

		# Reset renderer position
		self.renderer_x = 0
		self.renderer_y = 0

		# Clear text from render queue
		self.char_rects.clear()
		self.char_surfaces.clear()
		self.line_rects.clear()
		self.line_surfaces.clear()
		
		# Set True for use in main loop 
		self.is_open = True

		# Allow user to start typing immediatly 
		self.text_entry_active = True

		print("node opened")

	
	# Text will need to be rendered with .md tags in real time
	def draw_text(self):

		# During the first iteration and upon screen scrolling, draw entire displayed area of the doc  
		if not self.text_drawn:

			# Create a surface and a rectangle for every character in the title and append it to the title line 
			for char in self.node_title:
				# Get the surface
				char_surface = self.title_font.render(char, True)  # true for anti-aliasing 
				#self.char_surfaces[0].append(char_surface)
				
				# Get the rect 
				char_rect = char_surface.get_rect()
				self.char_rects[0].append(char_rect)

				# Create one line surface to append the title character surfaces to
				if len(self.line_surfaces) == 0:
					# Get the surface
					self.line_surface_h = char_rect[3]
					title_surface = pg.Surface(self.line_surface_x, self.line_surface_y, self.line_surface_w, self.line_surface_h)
					self.line_surfaces.append(title_surface)

					# Get the rect
					title_surface_rect = title_surface.get_rect()
					self.line_rects.append(title_surface_rect)

					# Increment the line_surface starting position for the next line
					self.line_surface_y += self.line_surface_h

				self.line_surfaces[0].append(char_surface)

			# Create a surface and a rect for every character in the body text and append it to the approrpriate line 
			line_number = 1
			for char in self.text:
				# Get the surface
				char_surface = self.body_font.render(char, True)
				# self.char_surfaces[line_number].append(char_surface)

				# Get the rect and set the position for later when they are displayed to the line surface      
				char_rect = char_surface.get_rect()
				char_rect[0] = self.char_x
				char_rect[1] = self.line_surface_y 
				self.char_rects[line_number].append(char_rect)

				# Create the first line surface and rect for the body text if only the title line has been created 
				if len(self.line_surfaces) == 1:
					# The height of the line surface can now be set to the height of the character rect that uses the body font  
					self.line_surface_h = char_rect[3]

					# Get the surface 
					body_surface = pg.Surface(self.line_surface_x, self.line_surface_y, self.line_surface_w, self.line_surface_h)
					self.line_surfaces.append(body_surface)

					# Get the rect
					body_surface_rect = body_surface.get_rect()
					self.line_rects.append(body_surface_rect)

					# Increment the line_surface starting position for the next line
					self.line_surface_y += self.line_surface_h

				# Only append the char surface if it fits on the current line
				if self.char_x < self.line_rect_w:
					self.line_surfaces[line_number].append(char_surface)
					self.char_x += char_rect[2]
				# Or create a new line surface and append it there 
				else: 
					# Get the surface
					body_surface = pg.Surface(self.line_surface_x, self.line_surface_y, self.line_surface_w, self.line_surface_h)
					self.line_surfaces.append(body_surface)

					# Get the rect
					body_surface_rect = body_surface.get_rect()
					self.line_rects.append(body_surface_rect)
					
					# Increment the line number and reset the char_x position for the new line 
					line_number += 1
					self.char_x = 0
					
					# Append to the new line 
					self.line_surfaces[line_number].append(char_surface)
			
			# Display the line surfaces to the workspace
			for surface in self.line_surfaces:
						
				self.text_drawn = True

		# If a line is marked as changed, redraw it with the appropriate text 


		# Reset the text holder for each line 


	def text_entry(self, mouse_pos, mouse_buttons_pressed):
		pass


	def save(self):
		path = os.path.join(config.node_md_folder, self.node_title)
		with open(path, 'w') as file:
			file.write(self.text)
			file.flush()


	def delete(self, node_name):
		path = os.path.join(config.node_md_folder, node_name)
		if os.path.exists(path):
			os.remove(path)