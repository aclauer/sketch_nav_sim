import pygame
import sys

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
black = (0, 0, 0)
white = (255, 255, 255)

# Variables for coordinate printing
movement_counter = 0
movement_print_threshold = 5

# Main loop
running = True
drawing = False  # State to track if the mouse is being held down
last_pos = None  # Last position of the mouse

# Blit the background image once
screen.blit(background_image, (0, 0))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            drawing = True
            last_pos = event.pos
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            movement_counter = 0  # Reset counter when stopping
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos
            if last_pos is not None:
                pygame.draw.line(drawing_surface, black, last_pos, current_pos, 5)
                movement_counter += 1
                if movement_counter >= movement_print_threshold:
                    print(f"Drawing at: x={current_pos[0]}, y={current_pos[1]}")  # Print current drawing position
                    movement_counter = 0  # Reset the counter after printing
            last_pos = current_pos

    # Blit the transparent drawing surface over the background
    screen.blit(drawing_surface, (0, 0))
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()