import random

import pygame

# Initialize pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Display settings
WIDTH, HEIGHT = 600, 400
DIS = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Snake Game - Speed Increases!')

CLOCK = pygame.time.Clock()
SNAKE_BLOCK = 10

# Initial speed 
INITIAL_SPEED = 10
#  increase speed per food eaten by 2 units
SPEED_INCREMENT = 1


def game_loop():
    game_over = False
    game_close = False

    x1 = WIDTH / 2
    y1 = HEIGHT / 2
    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    # Place initial food
    foodx = round(random.randrange(0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
    foody = round(random.randrange(0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0

    # Current speed starts at initial value
    current_speed = INITIAL_SPEED

    while not game_over:
        while game_close:
            DIS.fill(BLACK)
            font = pygame.font.SysFont("bahnschrift", 35)
            mesg = font.render(
                f"Game Over! Score: {length_of_snake-1}", True, RED)
            score_msg = font.render("Press C-Play Again or Q-Quit", True, BLUE)

            # Center the text
            DIS.blit(mesg, [WIDTH/6, HEIGHT/3])
            DIS.blit(score_msg, [WIDTH/6, HEIGHT/3 + 50])

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()  # Restart the game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = SNAKE_BLOCK
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -SNAKE_BLOCK
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = SNAKE_BLOCK
                    x1_change = 0

        # Check boundaries
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        DIS.fill(BLACK)

        # Draw Food
        pygame.draw.rect(DIS, GREEN, [foodx, foody, SNAKE_BLOCK, SNAKE_BLOCK])

        # Snake Logic
        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        # Check if snake hit itself
        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        # Draw Snake
        for segment in snake_list:
            pygame.draw.rect(
                DIS, WHITE, [segment[0], segment[1], SNAKE_BLOCK, SNAKE_BLOCK])

        pygame.display.update()

        # Eat Food
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(
                0, WIDTH - SNAKE_BLOCK) / 10.0) * 10.0
            foody = round(random.randrange(
                0, HEIGHT - SNAKE_BLOCK) / 10.0) * 10.0
            length_of_snake += 1

            # Increase speed slightly when food is eaten
            current_speed += SPEED_INCREMENT

            # Optional: Cap the maximum speed so it doesn't become impossible
            if current_speed > 40:
                current_speed = 40

        # Use the dynamic current_speed instead of a fixed constant
        CLOCK.tick(current_speed)

    pygame.quit()
    quit()


game_loop()
