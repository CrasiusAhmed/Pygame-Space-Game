# TUTORIAL 3: Adding Shooting and Bullet Collision
# YouTube Tutorial: Space Game Part 3 - Shoot the Asteroids!

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
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
PLAYER_SPEED = 7
ENEMY_SPEED = 3
BULLET_SPEED = 10
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 100, 255)
RED = (255, 0, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game Tutorial 3 - Shooting System")
clock = pygame.time.Clock()

# --- Game Objects ---
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, 
                         SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
enemies = []
bullets = []
score = 0

# --- Game Functions ---
def spawn_enemy():
    """Create a new enemy at the top of the screen"""
    x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_rect = pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemies.append(enemy_rect)

def shoot_bullet():
    """Create a new bullet from player position"""
    bullet_x = player_rect.centerx - BULLET_WIDTH // 2
    bullet_y = player_rect.top
    bullet_rect = pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet_rect)

def update_enemies():
    """Move enemies down and remove them when they go off-screen"""
    for enemy in enemies[:]:
        enemy.y += ENEMY_SPEED
        if enemy.top > SCREEN_HEIGHT:
            enemies.remove(enemy)

def update_bullets():
    """Move bullets up and remove them when they go off-screen"""
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

def check_bullet_enemy_collision():
    """Check if any bullet hits any enemy"""
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                return  # Exit after first collision to avoid errors

def check_player_enemy_collision():
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
    
    # Draw bullets
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
    
    # Draw score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Draw instructions
    small_font = pygame.font.Font(None, 24)
    text1 = small_font.render("LEFT/RIGHT arrows to move", True, WHITE)
    text2 = small_font.render("SPACEBAR to shoot", True, WHITE)
    text3 = small_font.render("Shoot the asteroids for points!", True, WHITE)
    screen.blit(text1, (10, 50))
    screen.blit(text2, (10, 75))
    screen.blit(text3, (10, 100))
    
    # Update display
    pygame.display.flip()

# --- Main Game Loop ---
def game_loop():
    """Tutorial 3: Player movement, shooting, and collision detection"""
    global score
    running = True
    enemy_spawn_timer = 0
    
    while running:
        # --- 1. HANDLE EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet()
        
        # --- 2. UPDATE GAME STATE ---
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED
        
        # Spawn enemies periodically
        enemy_spawn_timer += 1
        if enemy_spawn_timer >= 60:  # Spawn every 60 frames
            spawn_enemy()
            enemy_spawn_timer = 0
        
        # Update positions
        update_enemies()
        update_bullets()
        
        # Check collisions
        check_bullet_enemy_collision()
        if check_player_enemy_collision():
            print(f"GAME OVER! Final Score: {score}")
            running = False
        
        # --- 3. DRAW EVERYTHING ---
        draw_everything()
        
        # --- 4. CONTROL FRAME RATE ---
        clock.tick(FPS)
    
    # Show game over screen
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 48)
    
    game_over_text = font.render("GAME OVER!", True, RED)
    final_score_text = small_font.render(f"Final Score: {score}", True, WHITE)
    
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 - 50))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 + 20))
    pygame.display.flip()
    
    # Wait before closing
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    print("Tutorial 3: Shooting System")
    print("Controls:")
    print("  LEFT/RIGHT arrows - Move")
    print("  SPACEBAR - Shoot")
    print("Objective: Shoot asteroids to score points!")
    game_loop()
