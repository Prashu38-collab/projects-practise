import math
import random

import pygame

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Click the Target")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (150, 20, 20)
GREEN = (50, 200, 100)

font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)

GAME_TIME = 30

target_x = 400
target_y = 300

target_radius = 40
target_speed = 2

score = 0

start_time = pygame.time.get_ticks()

game_over = False


def move_target():
    global target_x, target_y

    target_x = random.randint(target_radius, WIDTH - target_radius)
    target_y = random.randint(100 + target_radius, HEIGHT - target_radius)


def reset_game():
    global score
    global target_radius
    global target_speed
    global start_time
    global game_over

    score = 0
    target_radius = 40
    target_speed = 2
    start_time = pygame.time.get_ticks()
    game_over = False

    move_target()


running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouse_x, mouse_y = pygame.mouse.get_pos()

            distance = math.sqrt(
                (mouse_x - target_x) ** 2 +
                (mouse_y - target_y) ** 2
            )

            if distance <= target_radius:

                score += 1

                target_radius = max(10, target_radius - 2)

                target_speed += 0.3

                move_target()

        if event.type == pygame.KEYDOWN:  # noqa: SIM102

            if event.key == pygame.K_r and game_over:
                reset_game()

    if not game_over:

        elapsed_time = (pygame.time.get_ticks() - start_time) / 1000

        remaining_time = max(0, GAME_TIME - elapsed_time)

        if remaining_time <= 0:
            game_over = True

    screen.fill(WHITE)

    if not game_over:

        pygame.draw.circle(
            screen,
            RED,
            (target_x, target_y),
            target_radius
        )

        pygame.draw.circle(
            screen,
            DARK_RED,
            (target_x, target_y),
            max(3, target_radius // 5)
        )

        score_text = font.render(
            f"Score: {score}",
            True,
            BLACK
        )

        screen.blit(score_text, (20, 20))

        timer_text = font.render(
            f"Time: {math.ceil(remaining_time)}",
            True,
            BLACK
        )

        screen.blit(timer_text, (650, 20))

    else:

        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        score_text = font.render(
            f"Final Score: {score}",
            True,
            BLACK
        )

        restart_text = font.render(
            "Press R to restart",
            True,
            GREEN
        )

        screen.blit(
            game_over_text,
            game_over_text.get_rect(
                center=(WIDTH // 2, 240)
            )
        )

        screen.blit(
            score_text,
            score_text.get_rect(
                center=(WIDTH // 2, 320)
            )
        )

        screen.blit(
            restart_text,
            restart_text.get_rect(
                center=(WIDTH // 2, 380)
            )
        )

    pygame.display.flip()

    clock.tick(60)

pygame.quit()
