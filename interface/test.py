import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Advanced Drawing App")

# Load the background image
background_image = pygame.image.load('interface/test.jpg')  # Replace 'background.jpg' with your image file
background_image = pygame.transform.scale(background_image, (width, height))

# Create a transparent surface for drawing
drawing_surface = pygame.Surface((width, height))
drawing_surface.set_colorkey((0,0,0))  # Set black as transparent color; adjust if black is a drawing color
drawing_surface.set_alpha(128)

# Define colors
black = (0, 0, 90)
white = (255, 255, 255)
red = (255, 0, 0)

font = pygame.font.Font(None, 36)


# Variables for coordinate printing and time control
movement_counter = 0
movement_print_threshold = 5
last_draw_time = None  # Variable to store the last draw time
draw_interval = 10  # Interval in seconds

# Main loop
running = True
drawing = False  # State to track if the mouse is being held down
last_pos = None  # Last position of the mouse

# Blit the background image once


while running:
    current_time = time.time()
    screen.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            
            if last_draw_time is None or current_time - last_draw_time >= draw_interval:
                drawing = True
                last_pos = event.pos
                 # Update the last draw time
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            movement_counter = 0  # Reset counter when stopping
            last_draw_time = current_time 
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos
            if last_pos is not None:
                pygame.draw.line(drawing_surface, black, last_pos, current_pos, 5)
                movement_counter += 1
                if movement_counter >= movement_print_threshold:
                    print(f"Drawing at: x={current_pos[0]}, y={current_pos[1]}")
                    movement_counter = 0
            last_pos = current_pos

    # Update and blit the timer
    if last_draw_time is not None:
        time_left = max(0, draw_interval - (current_time - last_draw_time))
        timer_text = font.render(f"Time left: {int(time_left)}s", True, red)
        screen.blit(timer_text, (50, 50))

    screen.blit(drawing_surface, (0, 0))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()