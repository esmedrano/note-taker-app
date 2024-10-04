# Libraries
import pygame as pg
import pygame_gui as pgg
import os
import json
import random as rand

# Application code modules 
import init
import user_interface
import graph
import node

pg.init()

bg_color = (150, 150, 150) 
pg_c = getattr(pg, 'K_SPACE')

# Proof of concept
def overclock():
	circle_radius = 5 
	circles = []
	x_pos = [*range(10, window_x, 10)]
	y_pos = [*range(10, window_y, 10)]
	for y in y_pos:
		for x in x_pos:
			circle_rect = pg.Rect(x - circle_radius, y - circle_radius, circle_radius * 2, circle_radius * 2)
			circles.append(circle_rect)

	i = 0
	for circle_rect in circles:
		circle_rect.x = rand.randrange(0, window_x - circle_radius * 2)
		circle_rect.y = rand.randrange(0, window_y - circle_radius * 2)
		pg.draw.circle(window, (0, 0, 0), circle_rect.center, circle_radius)
		pg.draw.line(window, (0, 0, 0), (circles[i][0], circles[i][1]), (circles[i - 1][0], circles[i - 1][1]))
		i += 1


def main():
	# UI class from user_interface.py
	ui = user_interface.Elements()

	is_running = True
	while is_running:
		# This keeps the code from straining the cpu 
		init.tick_clock()

		# Event handling
		for event in pg.event.get():
			if event.type == pg.QUIT:
				is_running = False
			
			# Update the window size variables when window is resized
			if event.type == pg.VIDEORESIZE:
				init.update_screen_size(event.w, event.h)
			
			if event.type == pg.KEYDOWN:
				keys = pg.key.get_pressed()

				for shortcut in shortcuts:
					for key_combo in shortcut: 
						if all(keys[getattr(pg, key)] for key in key_combo):
							print('combo')

			# Button logic
			# if event.type == pgg.UI_BUTTON_PRESSED:
			# 	if event.ui_element == hello_button:
			# 		print('Hello world')

			# UI events
			init.manager.process_events(event)

		init.window.fill(bg_color)

		# Build non pygame_gui elements 
		ui.header()   
		ui.sidebar()  # This can't be built anywhere else (event for loop, outside of while loop) for reasons that are beyond me  
		
		# Some UI elements require a timer
		init.manager.update(init.time_delta)
		# Draw UI elements 
		init.manager.draw_ui(init.window)

		# Update the screen
		pg.display.update()

		with open('keyboard_shortcuts.json', 'r') as file:
			data = json.load(file)

		create_new_node = data.get("create new node")
		shortcuts = [create_new_node]
		
		
if __name__ == "__main__":
	main()
	pg.quit()
