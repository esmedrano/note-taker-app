# Contains: tab container bar, sidebar, 

import pygame as pg
import pygame_gui as pgg
import init


class Elements:
	def __init__(self):
		self.manager = init.manager
		self.header_bg = (100, 100, 100)
		self.initial_window_y = init.window_y

		# pygame_gui elements
		self.pygame_gui_sidebar = None


	# Header for displaying tabs 
	def header(self):
		# Build header rect here bc __init__ doesn't catch window_x resize
		header_rect = pg.Rect(0, 0, init.window_x, 35)

		# header bar background  
		pg.draw.rect(init.window, self.header_bg, header_rect)

		# Font 
		font = pg.font.Font(None, 24)
		text_color = (125, 125, 125)
		
		# Button text
		file_text = font.render("file", True, text_color)
		init.window.blit(file_text, (10, 10, 10, 10))


	def sidebar(self):
		# Build header rect here bc __init__ doesn't catch window_x resize
		header_rect = pg.Rect(0, 0, init.window_x, 35)

		# sidebar background  
		pg.draw.rect(init.window, self.header_bg, (0, header_rect[3], 100, init.window_y))
		

	# Tab functionality
	def tab(self):
		# Select, move, and slpit tabs
		pass


	# Holder for UI state variables  
	def get_ui_state(self):
		on_graph = true
		on_node = false
		toggle_file_display = true

		ui_state = [on_graph, on_node, toggle_file_display]

		return ui_state


	def ui_buttons(self):
		pass


	### POTENTIAL PYGAME_GUI BUGS ###
	def build_pygame_gui_elements(self):
		# Build header rect here bc __init__ doesn't catch window_x resize
		header_rect = pg.Rect(0, 0, init.window_x, 35)
		# Update self.sidebar with the UI function so that sidebar is accessable in the resize function 
		self.sidebar = pgg.elements.UIPanel(
			relative_rect=pg.Rect(0, header_rect[3], 100, 100), 
			manager=self.manager
			)
		#self.sidebar.set_dimensions((100, init.window_y))
		# self.sidebar.set_dimensions((100, 10))
		# self.sidebar.set_dimensions((100, 50))
		# sidebar_scroller = pgg.elements.ui_scrolling_container.UIScrollingContainer(
		# 	relative_rect=pg.Rect(50, 50, 50, 100), 
		# 	manager=self.manager,  
		# 	container=sidebar 
		# 	)


	# Side bar for displaying file structure
	def resize_pygame_gui_sidebar(self):
		sidebar_y = init.window_y - 50
		print(init.window_y, sidebar_y)
		self.sidebar.set_dimensions((100, sidebar_y))
		# self.sidebar.set_position((10, 80))
		# if init.window_y < self.initial_window_y:
		# 	 self.sidebar.set_dimensions((100, init.window_y))
		# 	 #self.sidebar.rebuild()
		# 	 self.initial_window_y = init.window_y 
		# 	 print('i')
		# elif init.window_y > self.initial_window_y:
		# 	 self.sidebar.set_dimensions((100, init.window_y))
		# 	 #self.sidebar.rebuild()
		# 	 self.initial_window_y = init.window_y 
		# 	 print('i')
