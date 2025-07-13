# TUTORIAL 5: Complete Game with Game Over Screen and Restart
# YouTube Tutorial: Space Game Part 5 - Final Complete Game!

import pygame
import sys
import random
import os

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
pygame.display.set_caption("Space Game Tutorial 5 - Complete Game")
clock = pygame.time.Clock()

# --- Try to Load Images (Optional Enhancement) ---
IMG_DIR = "img"
player_img = None
enemy_img = None

try:
    if os.path.exists(os.path.join(IMG_DIR, "spaceship.png")):
        player_img = pygame.image.load(os.path.join(IMG_DIR, "spaceship.png")).convert_alpha()
        player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    
    if os.path.exists(os.path.join(IMG_DIR, "asteroid.png")):
        enemy_img = pygame.image.load(os.path.join(IMG_DIR, "asteroid.png")).convert_alpha()
        enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
except pygame.error:
    print("Images not found, using colored rectangles instead")

# --- Game Variables ---
high_score = 0

# --- Game Functions ---
def create_stars():
    """Create the star field background"""
    stars = []
    for _ in range(150):
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        stars.append([x, y])
    return stars

def update_stars(stars):
    """Move stars down to create scrolling space effect"""
    for star in stars:
        star[1] += 1
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randint(0, SCREEN_WIDTH)

def spawn_enemy(enemies):
    """Create a new enemy at the top of the screen"""
    x = random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH)
    enemy_rect = pygame.Rect(x, -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
    enemies.append(enemy_rect)

def shoot_bullet(player_rect, bullets):
    """Create a new bullet from player position"""
    bullet_x = player_rect.centerx - BULLET_WIDTH // 2
    bullet_y = player_rect.top
    bullet_rect = pygame.Rect(bullet_x, bullet_y, BULLET_WIDTH, BULLET_HEIGHT)
    bullets.append(bullet_rect)

def update_enemies(enemies):
    """Move enemies down and remove them when they go off-screen"""
    for enemy in enemies[:]:
        enemy.y += ENEMY_SPEED
        if enemy.top > SCREEN_HEIGHT:
            enemies.remove(enemy)

def update_bullets(bullets):
    """Move bullets up and remove them when they go off-screen"""
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

def check_bullet_enemy_collision(bullets, enemies):
    """Check if any bullet hits any enemy and return score increase"""
    score_increase = 0
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                bullets.remove(bullet)
                enemies.remove(enemy)
                score_increase += 1
                break
    return score_increase

def check_player_enemy_collision(player_rect, enemies):
    """Check if player collides with any enemy"""
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            return True
    return False

def draw_game(screen, player_rect, enemies, bullets, stars, score, high_score):
    """Draw all game objects"""
    # Clear screen
    screen.fill(BLACK)
    
    # Draw star field
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, star, 1)
    
    # Draw player (image or rectangle)
    if player_img:
        screen.blit(player_img, player_rect)
    else:
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, WHITE, player_rect, 2)
    
    # Draw enemies (images or rectangles)
    for enemy in enemies:
        if enemy_img:
            screen.blit(enemy_img, enemy)
        else:
            pygame.draw.rect(screen, GRAY, enemy)
            pygame.draw.rect(screen, RED, enemy, 2)
    
    # Draw bullets with glow effect
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
        glow_rect = pygame.Rect(bullet.x - 1, bullet.y - 1, 
                               bullet.width + 2, bullet.height + 2)
        pygame.draw.rect(screen, WHITE, glow_rect, 1)
    
    # Draw UI
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 28)
    
    # Score display
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = small_font.render(f"High Score: {high_score}", True, YELLOW)
    
    score_bg = pygame.Rect(10, 10, max(score_text.get_width(), high_score_text.get_width()) + 20, 80)
    pygame.draw.rect(screen, (0, 0, 0, 128), score_bg)
    pygame.draw.rect(screen, WHITE, score_bg, 2)
    
    screen.blit(score_text, (20, 15))
    screen.blit(high_score_text, (20, 50))
    
    # Game stats
    stats_y = 110
    enemies_text = small_font.render(f"Asteroids: {len(enemies)}", True, GREEN)
    bullets_text = small_font.render(f"Bullets: {len(bullets)}", True, YELLOW)
    screen.blit(enemies_text, (10, stats_y))
    screen.blit(bullets_text, (10, stats_y + 25))
    
    # Instructions
    instructions = [
        "LEFT/RIGHT - Move",
        "SPACEBAR - Shoot",
        "Survive as long as possible!"
    ]
    
    for i, instruction in enumerate(instructions):
        text = small_font.render(instruction, True, WHITE)
        screen.blit(text, (SCREEN_WIDTH - text.get_width() - 10, 10 + i * 25))
    
    pygame.display.flip()

def show_game_over_screen(screen, stars, score, high_score):
    """Display game over screen with restart option"""
    waiting = True
    
    while waiting:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Restart game
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        
        # Draw game over screen
        screen.fill(BLACK)
        
        # Animate stars in background
        update_stars(stars)
        for star in stars:
            pygame.draw.circle(screen, STAR_COLOR, star, 1)
        
        # Game over text
        title_font = pygame.font.Font(None, 100)
        subtitle_font = pygame.font.Font(None, 60)
        instruction_font = pygame.font.Font(None, 40)
        
        game_over_text = title_font.render("GAME OVER", True, RED)
        final_score_text = subtitle_font.render(f"Final Score: {score}", True, WHITE)
        
        # High score message
        if score > high_score:
            high_score_msg = subtitle_font.render("NEW HIGH SCORE!", True, YELLOW)
            screen.blit(high_score_msg, (SCREEN_WIDTH // 2 - high_score_msg.get_width() // 2, 
                                        SCREEN_HEIGHT // 2 - 150))
        else:
            high_score_text = subtitle_font.render(f"High Score: {high_score}", True, YELLOW)
            screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, 
                                         SCREEN_HEIGHT // 2 - 150))
        
        # Main text
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                                    SCREEN_HEIGHT // 2 - 80))
        screen.blit(final_score_text, (SCREEN_WIDTH // 2 - final_score_text.get_width() // 2, 
                                      SCREEN_HEIGHT // 2))
        
        # Instructions
        restart_text = instruction_font.render("Press 'R' to Restart", True, GREEN)
        quit_text = instruction_font.render("Press 'Q' or ESC to Quit", True, WHITE)
        
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                                  SCREEN_HEIGHT // 2 + 80))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, 
                               SCREEN_HEIGHT // 2 + 120))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    return False

def game_loop():
    """Main game loop"""
    global high_score
    
    # Initialize game objects
    player_rect = pygame.Rect(SCREEN_WIDTH // 2 - PLAYER_WIDTH // 2, 
                             SCREEN_HEIGHT - PLAYER_HEIGHT - 10, 
                             PLAYER_WIDTH, PLAYER_HEIGHT)
    enemies = []
    bullets = []
    stars = create_stars()
    score = 0
    enemy_spawn_timer = 0
    
    running = True
    
    while running:
        # --- 1. HANDLE EVENTS ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return False  # Don't restart
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot_bullet(player_rect, bullets)
        
        # --- 2. UPDATE GAME STATE ---
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED
        
        # Update visual effects
        update_stars(stars)
        
        # Spawn enemies with increasing difficulty
        enemy_spawn_timer += 1
        spawn_rate = max(20, 60 - score // 3)  # Gets faster as score increases
        if enemy_spawn_timer >= spawn_rate:
            spawn_enemy(enemies)
            enemy_spawn_timer = 0
        
        # Update game objects
        update_enemies(enemies)
        update_bullets(bullets)
        
        # Check collisions
        score += check_bullet_enemy_collision(bullets, enemies)
        
        if check_player_enemy_collision(player_rect, enemies):
            # Update high score
            if score > high_score:
                high_score = score
            
            print(f"GAME OVER! Final Score: {score}")
            running = False
        
        # --- 3. DRAW EVERYTHING ---
        draw_game(screen, player_rect, enemies, bullets, stars, score, high_score)
        
        # --- 4. CONTROL FRAME RATE ---
        clock.tick(FPS)
    
    # Show game over screen and check for restart
    return show_game_over_screen(screen, stars, score, high_score)

# --- Main Program ---
def main():
    """Main program with restart functionality"""
    print("Tutorial 5: Complete Space Game")
    print("Features:")
    print("  - Full game with restart functionality")
    print("  - High score tracking")
    print("  - Enhanced game over screen")
    print("  - Optional image support")
    print("  - Increasing difficulty")
    print("\nControls:")
    print("  LEFT/RIGHT arrows - Move")
    print("  SPACEBAR - Shoot")
    print("  R - Restart (on game over)")
    print("  Q/ESC - Quit (on game over)")
    
    # Main game loop with restart capability
    while True:
        restart = game_loop()
        if not restart:
            break
    
    pygame.quit()
    sys.exit()

# --- Start the Game ---
if __name__ == "__main__":
    main()
