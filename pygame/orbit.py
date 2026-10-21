
import random

import pygame

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Playground")

clock = pygame.time.Clock()

# Create stars once
stars = []
for _ in range(120):
    x = random.randrange(WIDTH)
    y = random.randrange(HEIGHT)
    radius = random.choice([1, 1, 1, 2])
    stars.append((x, y, radius))

# Store all created planets
planets = []

# Different planet colors
planet_colors = [
    (100, 180, 255),  # Blue
    (255, 120, 100),  # Red
    (180, 120, 255),  # Purple
    (100, 230, 170),  # Green
    (255, 200, 90),   # Yellow
]

running = True

while running:
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Create a planet when the left mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = event.pos

            planet = {
                "x": x,
                "y": y,
                "radius": random.randint(15, 35),
                "color": random.choice(planet_colors),
            }

            planets.append(planet)

    # Dark space background
    screen.fill((8, 12, 30))

    # Draw stars
    for x, y, radius in stars:
        pygame.draw.circle(
            screen, (180, 190, 220), (x, y), radius
        )

    # Draw planets
    for planet in planets:
        position = (planet["x"], planet["y"])
        radius = planet["radius"]
        color = planet["color"]

        pygame.draw.circle(screen, color, position, radius)

        # Small highlight to make the planet look round
        highlight_position = (
            planet["x"] - radius // 3,
            planet["y"] - radius // 3,
        )

        pygame.draw.circle(
            screen,
            (220, 230, 255),
            highlight_position,
            max(2, radius // 5),
        )

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
