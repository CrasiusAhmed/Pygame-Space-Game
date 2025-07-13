# TUTORIAL 4: Adding Visual Effects and Polish
# YouTube Tutorial: Space Game Part 4 - Stars Background and Visual Polish

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
STAR_COLOR = (200, 200, 200)
GREEN = (0, 255, 0)

# --- Initialize Pygame ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Game Tutorial 4 - Visual Effects")
clock = pygame.time.Clock()

# --- Game Objects ---
player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, 
                         SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
                         PLAYER_WIDTH, PLAYER_HEIGHT)
enemies = []
bullets = []
score = 0

# --- Visual Effects ---
# Create animated star field background
stars = []
for _ in range(150):
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    stars.append([x, y])

# --- Game Functions ---
def update_stars():
    """Move stars down to create scrolling space effect"""
    for star in stars:
        star[1] += 1  # Move star down
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

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
                return

def check_player_enemy_collision():
    """Check if player collides with any enemy"""
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            return True
    return False

def draw_everything():
    """Draw all game objects with visual effects"""
    # Clear screen with space black
    screen.fill(BLACK)
    
    # Draw animated star field
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, star, 1)
    
    # Draw player with a slight glow effect
    pygame.draw.rect(screen, BLUE, player_rect)
    # Add a border for better visibility
    pygame.draw.rect(screen, WHITE, player_rect, 2)
    
    # Draw enemies with better styling
    for enemy in enemies:
        pygame.draw.rect(screen, GRAY, enemy)
        pygame.draw.rect(screen, RED, enemy, 2)  # Red border
    
    # Draw bullets with glow effect
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
        # Add a subtle glow around bullets
        glow_rect = pygame.Rect(bullet.x - 1, bullet.y - 1, 
                               bullet.width + 2, bullet.height + 2)
        pygame.draw.rect(screen, WHITE, glow_rect, 1)
    
    # Draw enhanced UI
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 28)
    
    # Score with background
    score_text = font.render(f"Score: {score}", True, WHITE)
    score_bg = pygame.Rect(10, 10, score_text.get_width() + 20, score_text.get_height() + 10)
    pygame.draw.rect(screen, (0, 0, 0, 128), score_bg)  # Semi-transparent background
    pygame.draw.rect(screen, WHITE, score_bg, 2)
    screen.blit(score_text, (20, 15))
    
    # Game stats
    stats_y = 80
    enemies_text = small_font.render(f"Asteroids: {len(enemies)}", True, GREEN)
    bullets_text = small_font.render(f"Bullets: {len(bullets)}", True, YELLOW)
    screen.blit(enemies_text, (10, stats_y))
    screen.blit(bullets_text, (10, stats_y + 25))
    
    # Instructions with better formatting
    instructions = [
        "LEFT/RIGHT arrows - Move",
        "SPACEBAR - Shoot",
        "Destroy asteroids for points!"
    ]
    
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10 + i * 25))
    
    # Update display
    pygame.display.flip()

# --- Main Game Loop ---
def game_loop():
    """Tutorial 4: Enhanced visuals and polish"""
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
        
        # Update visual effects
        update_stars()
        
        # Spawn enemies with increasing difficulty
        enemy_spawn_timer += 1
        spawn_rate = max(30, 60 - score // 5)  # Faster spawning as score increases
        if enemy_spawn_timer >= spawn_rate:
            spawn_enemy()
            enemy_spawn_timer = 0
        
        # Update game objects
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
    
    # Enhanced game over screen
    screen.fill(BLACK)
    
    # Continue drawing stars for background effect
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, star, 1)
    
    # Game over text with effects
    title_font = pygame.font.Font(None, 100)
    subtitle_font = pygame.font.Font(None, 60)
    
    game_over_text = title_font.render("GAME OVER", True, RED)
    final_score_text = subtitle_font.render(f"Final Score: {score}", True, WHITE)
    
    # Add text shadows for better visibility
    shadow_offset = 3
    game_over_shadow = title_font.render("GAME OVER", True, (100, 0, 0))
    score_shadow = subtitle_font.render(f"Final Score: {score}", True, GRAY)
    
    # Draw shadows first
    screen.blit(game_over_shadow, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2 + shadow_offset, 
                                  SCREEN_HEIGHT // 2 - 80 + shadow_offset))
    screen.blit(score_shadow, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2 + shadow_offset, 
                              SCREEN_HEIGHT // 2 + shadow_offset))
    
    # Draw main text
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                SCREEN_HEIGHT // 2 - 80))
    screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2))
    
    pygame.display.flip()
    
    # Wait before closing
    pygame.time.wait(4000)
    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    print("Tutorial 4: Visual Effects and Polish")
    print("New Features:")
    print("  - Animated star field background")
    print("  - Enhanced UI with game stats")
    print("  - Visual effects and borders")
    print("  - Increasing difficulty")
    print("\nControls:")
    print("  LEFT/RIGHT arrows - Move")
    print("  SPACEBAR - Shoot")
    game_loop()
