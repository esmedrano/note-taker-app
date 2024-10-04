import init
import pygame as pg
import random as rand

pg.init()

def overclock():
	circle_radius = 5 
	circles = []
	x_pos = [*range(10, init.window_x, 10)]
	y_pos = [*range(10, init.window_y, 10)]
	for y in y_pos:
		for x in x_pos:
			circle_rect = pg.Rect(x - circle_radius, y - circle_radius, circle_radius * 2, circle_radius * 2)
			circles.append(circle_rect)

	i = 0
	for circle_rect in circles:
		circle_rect.x = rand.randrange(0, init.window_x - circle_radius * 2)
		circle_rect.y = rand.randrange(0, init.window_y - circle_radius * 2)
		pg.draw.circle(init.window, (0, 0, 0), circle_rect.center, circle_radius)
		pg.draw.line(init.window, (0, 0, 0), (circles[i][0], circles[i][1]), (circles[i - 1][0], circles[i - 1][1]))
		i += 1
		