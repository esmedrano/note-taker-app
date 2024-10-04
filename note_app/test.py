import pygame as pg
import pygame_gui as pgg

pg.init()

window_x = 500
window_y = 500
window = pg.display.set_mode((window_x, window_y), pg.RESIZABLE)

manager = pgg.UIManager((window_x, window_y))

# Create the initial UIPanel
sidebar = pgg.elements.UIPanel(
    relative_rect=pg.Rect(0, 35, 100, window_y - 35),  # Setting initial height
    manager=manager
)

clock = pg.time.Clock()
initial_window_y = window_y

# Main loop
running = True
while running:
    time_delta = clock.tick(60) / 1000.0
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.VIDEORESIZE:
            window_x, window_y = event.w, event.h
            
            # Resize the UIPanel
            sidebar.set_dimensions((100, window_y - 35))
            sidebar.rebuild()

    manager.update(time_delta)
    
    # Clear the window and draw everything
    window.fill((0, 0, 0))
    manager.draw_ui(window)
    pg.display.update()
