import pygame
import sys
import time
import math

# Define global constants and variables
WIDTH, HEIGHT = 1000, 1000
BLACK = (0, 0, 0)
RED = (255, 0, 0)
FOLLOWER_UPDATE_INTERVAL = .1  # seconds
GREY = (192, 192, 192)

# Global variables
follower_pos = None  # Position of the follower node
target_pos = None  # Target position for the follower
last_update_time = time.time()  # Last time the follower was updated

# Global variables
path = []  # List to store the path
follower_index = 0  # Index of the current point in the path that the follower is at

def init_game():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Advanced Drawing App")
    background_image = pygame.image.load('interface/test.jpg')
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    drawing_surface = pygame.Surface((WIDTH, HEIGHT))
    drawing_surface.set_colorkey(BLACK)
    drawing_surface.set_alpha(128)
    return screen, background_image, drawing_surface

def update_follower():
    global follower_index
    if follower_index < len(path) - 1:
        current_pos = path[follower_index]
        next_pos = path[follower_index + 1]
        dx = next_pos[0] - current_pos[0]
        dy = next_pos[1] - current_pos[1]
        angle = math.atan2(dy, dx)  # Angle in radians
        angle_degrees = math.degrees(angle)  # Convert to degrees
        print(f"Follower at: {current_pos} aiming for {next_pos} at angle {angle_degrees:.2f} degrees")
        follower_index += 1
    elif follower_index == len(path) - 1:
        print(f"Follower at: {path[follower_index]} has reached the end of the path")

def handle_events(drawing_surface):
    global drawing, last_pos, path
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            last_pos = event.pos
            drawing = True
            path.append(last_pos)  # Start a new path
        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
        elif event.type == pygame.MOUSEMOTION and drawing:
            current_pos = event.pos
            if last_pos:
                pygame.draw.line(drawing_surface, GREY, last_pos, current_pos, 5)
                path.append(current_pos)  # Add point to the path
            last_pos = current_pos

def main():
    global last_update_time, drawing, last_pos
    screen, background_image, drawing_surface = init_game()
    drawing = False
    last_pos = None

    running = True
    while running:
        current_time = time.time()
        screen.blit(background_image, (0, 0))
        screen.blit(drawing_surface, (0, 0))
        handle_events(drawing_surface)

        # Update follower's position every second
        if current_time - last_update_time >= FOLLOWER_UPDATE_INTERVAL:
            last_update_time = current_time
            update_follower()

        # Draw the follower node at the current index in the path
        if path and follower_index < len(path):
            pygame.draw.circle(screen, RED, path[follower_index], 10)

        pygame.display.flip()

if __name__ == "__main__":
    main()
