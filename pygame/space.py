
import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Switch")

clock = pygame.time.Clock()
font = pygame.font.Font(None, 32)
big_font = pygame.font.Font(None, 58)

BG = (15, 18, 35)
WHITE = (240, 245, 255)
CYAN = (40, 220, 255)
PINK = (255, 65, 130)
YELLOW = (255, 220, 70)

player = pygame.Rect(100, HEIGHT - 90, 35, 35)

gravity = 0.65
velocity_y = 0
gravity_direction = 1

obstacles = []
spawn_timer = 0
score = 0
game_over = False
speed = 5


def reset_game():
    global player, velocity_y, gravity_direction
    global obstacles, spawn_timer, score, game_over, speed

    player = pygame.Rect(100, HEIGHT - 90, 35, 35)
    velocity_y = 0
    gravity_direction = 1
    obstacles = []
    spawn_timer = 0
    score = 0
    game_over = False
    speed = 5


while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not game_over:
                gravity_direction *= -1
                velocity_y = 0

            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:
        velocity_y += gravity * gravity_direction
        player.y += int(velocity_y)

        # Keep the player between the floor and ceiling
        if player.bottom >= HEIGHT - 25:
            player.bottom = HEIGHT - 25
            velocity_y = 0

        if player.top <= 25:
            player.top = 25
            velocity_y = 0

        # Spawn obstacles
        spawn_timer += 1

        if spawn_timer >= 65:
            obstacle_height = random.randint(45, 100)

            if random.choice([True, False]):
                obstacle = pygame.Rect(
                    WIDTH, HEIGHT - 25 - obstacle_height,
                    30, obstacle_height
                )
            else:
                obstacle = pygame.Rect(
                    WIDTH, 25, 30, obstacle_height
                )

            obstacles.append(obstacle)
            spawn_timer = 0

        # Move obstacles
        for obstacle in obstacles[:]:
            obstacle.x -= speed

            if obstacle.right < 0:
                obstacles.remove(obstacle)
                score += 1
                speed = 5 + score // 8

            elif player.colliderect(obstacle):
                game_over = True

    # Draw everything
    screen.fill(BG)

    pygame.draw.line(screen, CYAN, (0, 25), (WIDTH, 25), 3)
    pygame.draw.line(
        screen, CYAN,
        (0, HEIGHT - 25), (WIDTH, HEIGHT - 25), 3
    )

    pygame.draw.rect(screen, YELLOW, player, border_radius=8)

    for obstacle in obstacles:
        pygame.draw.rect(
            screen, PINK, obstacle, border_radius=5
        )

    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 15))

    gravity_text = "Gravity: FLOOR" if gravity_direction == 1 else "Gravity: CEILING"
    screen.blit(font.render(gravity_text, True, CYAN), (20, 48))

    if game_over:
        title = big_font.render("GAME OVER", True, PINK)
        screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

        message = font.render(
            f"Score: {score}   |   Press R to restart",
            True, WHITE
        )
        screen.blit(
            message,
            message.get_rect(center=(WIDTH // 2, 235))
        )

    pygame.display.flip()
