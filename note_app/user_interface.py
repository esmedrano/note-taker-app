# Contains: tab container bar, sidebar, 
import os
import pygame as pg
import config


class Elements:
	def __init__(self):
		self.header_color = ((100,)*3)
		self.sidebar_color = ((100,)*3)
		self.button_color = ((100,)*3)

		# Pygame shapes as ui elements 
		self.header_rect_h = 35  # Specific dimensions vars are created for easy changes later
		self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)
		self.sidebar_w = 200
		self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)
		
		# Button initialization
		self.button_h = 20
		self.button_rects = []

		# File names
		self.file_names = []


	# Header for displaying tabs 
	def draw_header(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.header_rect = pg.Rect(0, 0, config.window_x, self.header_rect_h)

		# header bar background  
		pg.draw.rect(config.window, self.header_color, self.header_rect)

		# Font 
		font = pg.font.Font(None, 24)
		text_color = ((200,)*3)
		
		# Button text
		file_text = font.render("file", True, text_color)
		config.window.blit(file_text, (10, 10))


	def draw_sidebar(self):
		# Rebuild header rect here bc __init__ doesn't catch window_x resize
		self.sidebar_rect = pg.Rect(0, self.header_rect[3], self.sidebar_w, config.window_y)

		# sidebar background  
		pg.draw.rect(config.window, self.sidebar_color, self.sidebar_rect)


	def draw_sidebar_buttons(self):
		font = pg.font.Font(None, 24)
		text_color = ((200,)*3)
		
		# Only proceed if the "node markdown files" folder exists 
		folder = config.node_md_folder
		if os.path.exists(folder) and os.path.isdir(folder):

			# Collect node file names from folder every time main loop iterates
			self.file_names = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

			# Draw buttons on sidebar display where each new button is below the last 
			button_count = 0
			for title in self.file_names:
				# Y possition of each button is offset from the height of the previous buttons (button_h * i) 
				# and the height of the header bar
				button_y = self.button_h * button_count + self.header_rect[3]

				# Save the button rectangles for later
				new_button_rect = pg.Rect(0, button_y, self.sidebar_rect[2], self.button_h)
				self.button_rects.append([title, new_button_rect])

				# Draw the button and the text 
				pg.draw.rect(config.window, self.button_color, new_button_rect)
				config.window.blit(font.render(title, True, text_color), (10, button_y + 3))

				# Increment the button count 
				button_count += 1


	def get_pressed_buttons(self, ui, redraw_display):
		mouse_cursor = pg.mouse.get_pos()
		mouse_buttons = pg.mouse.get_pressed()

		for button in self.button_rects:
			if button[1].collidepoint(mouse_cursor):
				# ui.button_color = ((200,)*3)
				# redraw_display.draw(ui)

				if mouse_buttons[0]:
					print(button[0])

			if button[1].collidepoint(mouse_cursor):
				if mouse_buttons[2]:
					right_click_popup()


	def right_click_popup(self):
		popup_rect = pg.Rect(config.window_x / 2, config.window_y / 2, 100, 50)
		pg.draw.rect(config.window, (200, 200 ,200), popup_rect)


	def shade_hovered_button(self):
		pass
