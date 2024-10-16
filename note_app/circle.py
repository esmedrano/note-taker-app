import pygame as pg
import config


def draw(radius):
	pg.draw.circle(config.window, (0, 0, 255), (300, 200), radius)
