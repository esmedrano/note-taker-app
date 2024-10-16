import pygame

pygame.init()

# Set up the window
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Pygame Text Editor")

# Font settings
font = pygame.font.Font(None, 36)

# Text-related variables
text = ""  # Store the inputted text
cursor_position = len(text)  # Track cursor position

# Set up the main loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen with white background
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Handle backspace
                if cursor_position > 0:
                    text = text[:cursor_position - 1] + text[cursor_position:]
                    cursor_position -= 1
            
            elif event.key == pygame.K_RETURN:
                # Handle enter (for multiline support, append a newline)
                text = text[:cursor_position] + "\n" + text[cursor_position:]
                cursor_position += 1
            
            elif event.key == pygame.K_LEFT:
                # Move cursor left
                if cursor_position > 0:
                    cursor_position -= 1

            elif event.key == pygame.K_RIGHT:
                # Move cursor right
                if cursor_position < len(text):
                    cursor_position += 1
            
            elif event.key == pygame.K_DELETE:
                # Handle delete
                if cursor_position < len(text):
                    text = text[:cursor_position] + text[cursor_position + 1:]
            
            else:
                # Add character to text at the cursor position
                text = text[:cursor_position] + event.unicode + text[cursor_position:]
                cursor_position += 1

    # Render the text
    rendered_text = font.render(text, True, (0, 0, 0))
    screen.blit(rendered_text, (10, 10))

    # Display the cursor (optional)
    if pygame.time.get_ticks() % 1000 < 500:  # Blinking effect
        cursor_rect = pygame.Rect(rendered_text.get_width() + 10, 10, 2, rendered_text.get_height())
        pygame.draw.rect(screen, (0, 0, 0), cursor_rect)

    pygame.display.flip()

pygame.quit()
