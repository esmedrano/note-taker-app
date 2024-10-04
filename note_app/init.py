import pygame as pg
import pygame_gui as pgg

pg.init()

window_x = 500
window_y = 500
window = pg.display.set_mode((window_x, window_y), pg.RESIZABLE)

# UI manager for pygame_gui library 
manager = pgg.UIManager((window_x, window_y), theme_path="ui_theme.json") 
# Time between each loop required by pygame_gui library 
clock = pg.time.Clock()
time_delta = 0
def tick_clock():
	global time_delta
	time_delta = clock.tick(60)/1000.0


# Update window size variables when window is resized
def update_screen_size(width, height):
    global window_x, window_y
    window_x, window_y = width, height