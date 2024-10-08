import pygame as pg
import config
import user_interface
import overclock 


class Draw:
	def __init__(self):
		self.ui = user_interface.Elements()
		self.is_overclocking = False
		self.radius = 10
		self.display_redraws = 0


	def draw_app(self):
		# Set background colors
		config.window.fill(config.background_c)

		# Build non pygame_gui elements 
		self.ui.draw_header()
		self.ui.draw_sidebar()
		self.ui.draw_sidebar_buttons()   

		pg.draw.circle(config.window, (0, 0, 255), (300, 200), self.radius)

		if self.is_overclocking:
			overclock.overclock()

		pg.display.update()
		self.display_redraws += 1
		print("Screen redraws: ", self.display_redraws)

		# Used to check if nodes folder has been deleted
		node_folder_exists = False

		drawn = True
