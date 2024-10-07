import pygame as pg
import config
import overclock


class Draw:
    def __init__(self):
        self.is_overclocking = False
        self.screen_redraws = -1
        self.radius = 10


    # Draw the basic UI 
    def draw(self, ui):
        global screen_redraws 
        # Set background colors
        config.window.fill(config.bg_color)

        # Build non pygame_gui elements 
        ui.draw_header()
        ui.draw_sidebar()
        ui.draw_sidebar_buttons()   

        pg.draw.circle(config.window, (0, 0, 255), (300, 200), self.radius)

        if self.is_overclocking:
            overclock.overclock()

        pg.display.update()
        self.screen_redraws += 1
        print("Screen redraws: ", self.screen_redraws)
