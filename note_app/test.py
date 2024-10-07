import pygame as pg
import sys

# Initialize Pygame
pg.init()

# Set up the display
width, height = 800, 600
window = pg.display.set_mode((width, height))
pg.display.set_caption("Space Bar Print Example")

bgc = (100, 100, 100)

# Main loop
running = True
while running:
    # Draw everything that the user needs to use app
    window.fill(bgc)
    pg.draw.circle(window, (255, 0, 0), (100, 100), 50)
    pg.display.update()
    
    # Parse user input
    parsing = True
    while parsing:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                parsing = False

            # Check for key down events
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:  # Check if space bar is pressed
                    print("Exit inner loop to update screen!")
                    
                    parsing = False

# Clean up and close Pygame
pg.quit()
sys.exit()
