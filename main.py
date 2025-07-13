import pygame
import os
import random
import sys

# --- Constants ---
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
PLAYER_WIDTH = 80
PLAYER_HEIGHT = 80
ENEMY_WIDTH = 60
ENEMY_HEIGHT = 60
PLAYER_SPEED = 7
ENEMY_SPEED = 3
BULLET_SPEED = 10
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
FPS = 60

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
STAR_COLOR = (200, 200, 200)

# --- Game Setup ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroid Dodger")
clock = pygame.time.Clock()

# --- Asset Loading ---
IMG_DIR = "img"
try:
    player_img = pygame.image.load(os.path.join(IMG_DIR, "spaceship.png")).convert_alpha()
    player_img = pygame.transform.scale(player_img, (PLAYER_WIDTH, PLAYER_HEIGHT))
    enemy_img = pygame.image.load(os.path.join(IMG_DIR, "asteroid.png")).convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (ENEMY_WIDTH, ENEMY_HEIGHT))
except pygame.error as e:
    print("Unable to load image (spaceship.png or asteroid.png).")
    print("Please make sure the images are in the correct folder.")
    print(e)
    sys.exit()

# --- Game Objects ---
player_rect = player_img.get_rect(centerx=SCREEN_WIDTH // 2, bottom=SCREEN_HEIGHT - 10)
enemies = []
bullets = []
score = 0
font = pygame.font.Font(None, 36)
stars = [[random.randrange(SCREEN_WIDTH), random.randrange(SCREEN_HEIGHT)] for _ in range(150)]

# --- LOGIC FUNCTIONS ---

def update_stars():
    """Moves the stars down and resets them if they go off-screen."""
    for star in stars:
        star[1] += 1
        if star[1] > SCREEN_HEIGHT:
            star[1] = 0
            star[0] = random.randrange(SCREEN_WIDTH)

def move_objects():
    """Moves enemies and bullets. Removes them if they go off-screen."""
    for enemy in enemies[:]:
        enemy.y += ENEMY_SPEED
        if enemy.top > SCREEN_HEIGHT:
            enemies.remove(enemy)
    for bullet in bullets[:]:
        bullet.y -= BULLET_SPEED
        if bullet.bottom < 0:
            bullets.remove(bullet)

def handle_collisions():
    """Checks for collisions and returns True if the game is over."""
    global score
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if bullet.colliderect(enemy):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 1
                break
    for enemy in enemies:
        if player_rect.colliderect(enemy):
            return True  # Game Over
    return False

# --- DRAWING FUNCTIONS ---

def draw_screen():
    """Draws all game elements onto the screen."""
    # Draw background and stars
    screen.fill(BLACK)
    for star in stars:
        pygame.draw.circle(screen, STAR_COLOR, star, 1)
    
    # Draw player, enemies, and bullets
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet in bullets:
        pygame.draw.rect(screen, YELLOW, bullet)
        
    # Draw score
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))
    
    # Update the display
    pygame.display.flip()

def show_game_over_screen():
    """Displays the game over message and waits for player input."""
    # This function is fine as is, no changes needed.
    screen.fill(BLACK)
    title_font = pygame.font.Font(None, 74)
    sub_font = pygame.font.Font(None, 48)
    title_text = title_font.render("GAME OVER", True, RED)
    score_text = sub_font.render(f"Final Score: {score}", True, WHITE)
    restart_text = sub_font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                waiting = False

# --- Main Game Loop ---
def game_loop():
    """The main function that runs the game."""
    global score, enemies, bullets
    score = 0
    enemies = []
    bullets = []
    player_rect.centerx = SCREEN_WIDTH // 2
    player_rect.bottom = SCREEN_HEIGHT - 10
    
    # Use a custom timer event for spawning enemies for better consistency
    SPAWN_ENEMY_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_ENEMY_EVENT, 600) # Spawn an enemy every 600ms

    running = True
    while running:
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                # Use break to exit the loop cleanly, pygame.quit() is handled outside
                break 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = pygame.Rect(player_rect.centerx - (BULLET_WIDTH // 2), player_rect.top, BULLET_WIDTH, BULLET_HEIGHT)
                    bullets.append(bullet_rect)
            if event.type == SPAWN_ENEMY_EVENT:
                enemy_rect = pygame.Rect(random.randint(0, SCREEN_WIDTH - ENEMY_WIDTH), -ENEMY_HEIGHT, ENEMY_WIDTH, ENEMY_HEIGHT)
                enemies.append(enemy_rect)
        
        if not running: continue

        # --- 1. UPDATE GAME STATE ---
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player_rect.right < SCREEN_WIDTH:
            player_rect.x += PLAYER_SPEED
        
        update_stars()
        move_objects()
        if handle_collisions():
            running = False # End game on player collision

        # --- 2. DRAW EVERYTHING ---
        draw_screen()

        # --- Frame Rate Control ---
        clock.tick(FPS)

# --- Game Start ---
while True:
    game_loop()
    show_game_over_screen()