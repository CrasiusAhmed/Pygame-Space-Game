# TUTORIAL 1: Basic Pygame Window and Player Movement
# YouTube Tutorial: Space Game Part 1 - Getting Started with Pygame

import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
PLAYER_SPEED = 7
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game Tutorial 1 - Player Movement")
clock = pygame.time.Clock()

# --- Player Setup ---
# Create a simple rectangle for our player (we'll use images later)
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, 
                         SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)

# --- Main Game Loop ---
def game_loop():
    """Tutorial 1: Basic game loop with player movement"""
    running = True
    
    while running:
        # --- 1. HANDLE EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # --- 2. UPDATE GAME STATE ---
        # Get currently pressed keys
        keys = pygame.key.get_pressed()
        
        # Move player left and right (with boundary checking)
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED
        
        # --- 3. DRAW EVERYTHING ---
        # Fill screen with black background
        screen.fill(BLACK)
        
        # Draw player as a blue rectangle
        pygame.draw.rect(screen, BLUE, player_rect)
        
        # Add some text instructions
        font = pygame.font.Font(None, 36)
        text = font.render("Use LEFT and RIGHT arrows to move!", True, WHITE)
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 50))
        
        # Update the display
        pygame.display.flip()
        
        # --- 4. CONTROL FRAME RATE ---
        clock.tick(FPS)
    
    # Quit pygame
    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    print("Tutorial 1: Basic Player Movement")
    print("Controls: LEFT/RIGHT arrow keys to move")
    print("Close window to exit")
    game_loop()
