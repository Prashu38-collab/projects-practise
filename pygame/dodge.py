import random
import sys

import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 50
ENEMY_SIZE = 50
PLAYER_SPEED = 7
ENEMY_SPEED_BASE = 5
FPS = 60

# Colors 
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge the Falling Blocks")
clock = pygame.time.Clock()

# Font for score
font = pygame.font.SysFont("comicsansms", 35)


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def main():
    # Player position (start at bottom center)
    player_x = SCREEN_WIDTH // 2 - PLAYER_SIZE // 2
    player_y = SCREEN_HEIGHT - PLAYER_SIZE - 10

    # Enemy list: each enemy is [x, y]
    enemies = []
    spawn_timer = 0
    score = 0
    game_over = False
    enemy_speed = ENEMY_SPEED_BASE

    while True:
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                # Restart game
                main()  
                return

        if not game_over:
            # Key presses for movement
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and player_x > 0:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - PLAYER_SIZE:
                player_x += PLAYER_SPEED

            # Spawn enemies
            spawn_timer += 1
            if spawn_timer >= 30:  # Spawn every ~0.5 seconds (at 60 FPS)
                enemy_x = random.randint(0, SCREEN_WIDTH - ENEMY_SIZE)
                enemies.append([enemy_x, -ENEMY_SIZE])
                spawn_timer = 0

            # Move enemies
            for enemy in enemies[:]:  
                enemy[1] += enemy_speed

                # Remove if off-screen
                if enemy[1] > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    score += 1
                    # Increase difficulty slightly every 10 points
                    if score % 10 == 0:
                        enemy_speed += 0.5

                # Collision detection (AABB)
                player_rect = pygame.Rect(
                    player_x, player_y, PLAYER_SIZE, PLAYER_SIZE)
                enemy_rect = pygame.Rect(
                    enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE)

                if player_rect.colliderect(enemy_rect):
                    game_over = True

        
        screen.fill(WHITE)

        # Draw player
        pygame.draw.rect(
            screen, BLUE, (player_x, player_y, PLAYER_SIZE, PLAYER_SIZE))

        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(
                screen, RED, (enemy[0], enemy[1], ENEMY_SIZE, ENEMY_SIZE))

        # Draw score
        draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)

        if game_over:
            # make  screen dark slightly
            s = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            s.set_alpha(128)
            s.fill(BLACK)
            screen.blit(s, (0, 0))

            draw_text("GAME OVER", font, RED, screen,
                      SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 - 50)
            draw_text(f"Final Score: {score}", font, WHITE,
                      screen, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2)
            draw_text("Press 'R' to Restart", font, WHITE, screen,
                      SCREEN_WIDTH//2 - 140, SCREEN_HEIGHT//2 + 50)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
