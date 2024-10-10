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
		# Draw app 
		self.ui.draw_header()
		self.ui.draw_sidebar()
		self.ui.draw_workspace()
		self.ui.draw_sidebar_buttons()   

		pg.draw.circle(config.window, (0, 0, 255), (300, 200), self.radius)

		if self.is_overclocking:
			overclock.overclock()

		pg.display.update()
		self.display_redraws += 1
		print("\nScreen redraws: ", self.display_redraws)
