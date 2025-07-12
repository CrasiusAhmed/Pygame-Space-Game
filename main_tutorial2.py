# TUTORIAL 2: Adding Enemies and Basic Collision
# YouTube Tutorial: Space Game Part 2 - Falling Asteroids

import pygame
import sys
import random

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60
PLAYER_SPEED = 7
ENEMY_SPEED = 3
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game Tutorial 2 - Falling Asteroids")
clock = pygame.time.Clock()

# --- Game Objects ---
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, 
                         SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
enemies = []  # List to store enemy asteroids

# --- Game Functions ---
def spawn_enemy():
    """Create a new enemy at the top of the screen"""
    x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_rect = pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemies.append(enemy_rect)

def update_enemies():
    """Move enemies down and remove them when they go off-screen"""
    for enemy in enemies[:]:  # Use slice copy to safely modify list
        enemy.y += ENEMY_SPEED
        if enemy.top > SCREEN_HEIGHT:
            enemies.remove(enemy)

def check_collision():
    """Check if player collides with any enemy"""
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            return True
    return False

def draw_everything():
    """Draw all game objects"""
    # Clear screen
    screen.fill(BLACK)
    
    # Draw player
    pygame.draw.rect(screen, BLUE, player_rect)
    
    # Draw enemies
    for enemy in enemies:
        pygame.draw.rect(screen, GRAY, enemy)
    
    # Draw instructions
    font = pygame.font.Font(None, 28)
    text1 = font.render("LEFT/RIGHT arrows to move", True, WHITE)
    text2 = font.render("Avoid the gray asteroids!", True, WHITE)
    screen.blit(text1, (10, 10))
    screen.blit(text2, (10, 40))
    
    # Update display
    pygame.display.flip()

# --- Main Game Loop ---
def game_loop():
    """Tutorial 2: Player movement with falling enemies"""
    running = True
    enemy_spawn_timer = 0
    
    while running:
        # --- 1. HANDLE EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # --- 2. UPDATE GAME STATE ---
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED
        
        # Spawn enemies periodically
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60:  # Spawn every 60 frames (1 second at 60 FPS)
            spawn_enemy()
            enemy_spawn_timer = 0
        
        # Update enemy positions
        update_enemies()
        
        # Check for collisions
        if check_collision():
            print("COLLISION! Game Over!")
            running = False
        
        # --- 3. DRAW EVERYTHING ---
        draw_everything()
        
        # --- 4. CONTROL FRAME RATE ---
        clock.tick(FPS)
    
    # Show game over message
    font = pygame.font.Font(None, 74)
    game_over_text = font.render("GAME OVER!", True, RED)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    
    # Wait a moment before closing
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    print("Tutorial 2: Falling Asteroids")
    print("Controls: LEFT/RIGHT arrow keys to move")
    print("Objective: Avoid the falling gray asteroids!")
    game_loop()
