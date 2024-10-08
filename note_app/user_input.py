import pygame as pg
import config



# class User_Input:
# 	def __init__(self):
# 		# Call the singleton instance with the updated variables
# 		self.ui = Elements()  

# 		# Normal class instances 
# 		self.draw = Draw()

# 		self.hovered_buttons = []


# 	def get_pressed_buttons(self):  # ui, redraw_display
# 		mouse_cursor = pg.mouse.get_pos()
# 		mouse_buttons = pg.mouse.get_pressed()

# 		for button in self.ui.button_rects:
# 			# If the mouse cursor is in the button rectangle
# 			if button[1].collidepoint(mouse_cursor):
# 				self.hovered_buttons.append(button[0])
# 				# redraw the display 
# 				#self.draw.draw_app()

# 				if mouse_buttons[0]: 
# 					print(button[0])
# 			else:
# 				config.button_color = (0,0,0)
# 				print(0)

# 			if button[1].collidepoint(mouse_cursor):
# 				if mouse_buttons[2]:
# 					right_click_popup()
