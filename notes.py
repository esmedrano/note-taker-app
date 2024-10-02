import pygame as pg 
pg.init()

bg_color = (150, 150, 150)
header_bg = (100, 100, 100)

window_x = 500
window_y = 500
window = pg.display.set_mode((window_x, window_y), pg.RESIZABLE)


# Holder for UI state variables  
def get_ui_state():
	on_graph = true
	on_node = false
	toggle_file_display = true

	ui_state = [on_graph, on_node, toggle_file_display]

	return ui_state


# Update window size variables when window is resized
def update_screen_size(width, height):
    global window_x, window_y
    window_x, window_y = width, height


# Draw UI header bar
def ui_header():
	# header bar background  
	pg.draw.rect(window, header_bg, (0, 0, window_x, 35))

	# Font 
	font = pg.font.Font(None, 24)
	text_color = (125, 125, 125)
	
	# Button text
	file_text = font.render("file", True, text_color)
	window.blit(file_text, (10, 10, 10, 10))


# Create and draw a new node
def create_node():
	pass


# Draw node links
def link_node():
	pass


# Open a node text file
def select_node(nodes):
	pass


# Select a group of nodes
def box_select_nodes():
	box_origin = pg.mouse.get_pos()


# Lock nodesinplace on graph
def lock_nodes():
	pass


# Input text on a node 
def text_input():
	pass


while 1:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			pg.quit()
		
		# Update the window size variables when window is resized
		if event.type == pg.VIDEORESIZE:
			update_screen_size(event.w, event.h)

	# Set background color
	window.fill(bg_color)  
	
	# Draw UI header bar
	ui_header()   

	pg.display.update()

