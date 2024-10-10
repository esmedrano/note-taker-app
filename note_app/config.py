import pygame as pg


window_x = 900
window_y = 500
window = pg.display.set_mode((window_x, window_y), pg.RESIZABLE)

# Default node title
node_title = 'title.md'

# Default node markdown folder
node_md_folder  = 'node_markdow_files'

# Colors
header_c = ((100,)*3)
header_text_c = ((200,)*3)

sidebar_c = ((100,)*3)
sidebar_text_c = ((20,)*3)

workspace_c = ((150,)*3)

button_c = ((100,)*3)
button_hover_c = ((200,)*3)

popup_c = ((31,)*3)
popup_hover_c = ((54,)*3)
popup_text_c = ((200,)*3)
