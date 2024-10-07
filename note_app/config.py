import pygame as pg

pg.init()

window_x = 900
window_y = 500
window = pg.display.set_mode((window_x, window_y), pg.RESIZABLE)

node_md_folder  = 'node markdown files'

bg_color = (150, 150, 150) 

# Update window size variables when window is resized
def update_screen_size(width, height):
    global window_x, window_y
    window_x, window_y = width, height