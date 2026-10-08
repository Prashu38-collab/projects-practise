import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memory Pattern")

clock = pygame.time.Clock()

# Colors
BACKGROUND = (30, 30, 30)
WHITE = (255, 255, 255)
RED = (220, 70, 70)
GREEN = (70, 200, 100)
BLUE = (70, 120, 220)
YELLOW = (230, 200, 70)

colors = [RED, GREEN, BLUE, YELLOW]

# Create 4 squares
squares = [
    pygame.Rect(100, 100, 180, 180),
    pygame.Rect(320, 100, 180, 180),
    pygame.Rect(100, 320, 180, 180),
    pygame.Rect(320, 320, 180, 180)
]

pattern = []
player_input = []

level = 1
showing_pattern = False
pattern_index = 0
last_show_time = 0

font = pygame.font.Font(None, 50)


def create_pattern():
    global pattern

    pattern = []

    for i in range(level):
        pattern.append(random.randint(0, 3))


def show_pattern():
    global showing_pattern
    global pattern_index
    global last_show_time

    showing_pattern = True
    pattern_index = 0
    last_show_time = pygame.time.get_ticks()


def draw_game():
    screen.fill(BACKGROUND)

    for i, square in enumerate(squares):

        color = colors[i]

        # Highlight the current pattern square
        if showing_pattern and pattern_index < len(pattern):  # noqa: SIM102
            if i == pattern[pattern_index]:
                color = WHITE

        pygame.draw.rect(screen, color, square)

    text = font.render(
        "Level: " + str(level),
        True,
        WHITE
    )

    screen.blit(text, (20, 20))

    pygame.display.update()


create_pattern()
show_pattern()

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and not showing_pattern:

            mouse_position = event.pos

            for i, square in enumerate(squares):

                if square.collidepoint(mouse_position):

                    player_input.append(i)

                    # Check whether the latest click is correct
                    current_position = len(player_input) - 1

                    if player_input[current_position] != pattern[current_position]:

                        print("Game Over!")
                        print("You reached level:", level)

                        running = False

                    elif len(player_input) == len(pattern):

                        print("Correct!")

                        level += 1
                        player_input = []

                        create_pattern()
                        show_pattern()

    # Handle pattern animation
    if showing_pattern:

        current_time = pygame.time.get_ticks()

        if current_time - last_show_time > 700:

            pattern_index += 1
            last_show_time = current_time

            if pattern_index >= len(pattern):

                showing_pattern = False
                pattern_index = 0

    draw_game()

    clock.tick(60)

pygame.quit()
