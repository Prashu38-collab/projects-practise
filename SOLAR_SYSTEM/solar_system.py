
import pygame
import math
import random

pygame.init()

# 1. SCREEN SETUp

WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System V2")

clock = pygame.time.Clock()

# 2. SUN POSITIOn

SUN_X = WIDTH // 2
SUN_Y = HEIGHT // 2

# 3. PLANET DATa

planets = [
    {
        "name": "Mercury",
        "distance": 60,
        "angle": 0,
        "speed": 0.05,
        "color": (169, 169, 169),
        "size": 5
    },
    {
        "name": "Venus",
        "distance": 100,
        "angle": 1,
        "speed": 0.04,
        "color": (255, 165, 0),
        "size": 8
    },
    {
        "name": "Earth",
        "distance": 150,
        "angle": 2,
        "speed": 0.03,
        "color": (0, 100, 255),
        "size": 10
    },
    {
        "name": "Mars",
        "distance": 200,
        "angle": 3,
        "speed": 0.025,
        "color": (255, 70, 50),
        "size": 8
    },
    {
        "name": "Jupiter",
        "distance": 270,
        "angle": 4,
        "speed": 0.015,
        "color": (210, 140, 80),
        "size": 22
    },
    {
        "name": "Saturn",
        "distance": 340,
        "angle": 5,
        "speed": 0.012,
        "color": (230, 200, 120),
        "size": 18
    },
    {
        "name": "Uranus",
        "distance": 410,
        "angle": 6,
        "speed": 0.008,
        "color": (100, 220, 255),
        "size": 14
    },
    {
        "name": "Neptune",
        "distance": 480,
        "angle": 7,
        "speed": 0.006,
        "color": (50, 80, 255),
        "size": 13
    }
]

# 4. CREATE BACKGROUND STAR

stars = []

for _ in range(150):

    star_x = random.randint(0, WIDTH)
    star_y = random.randint(0, HEIGHT)
    star_size = random.randint(1, 3)

    stars.append(
        (star_x, star_y, star_size)
    )

# 5. CREATE ASTEROID

asteroids = []

for _ in range(100):

    asteroid = {
        "distance": random.randint(225, 250),
        "angle": random.uniform(0, math.pi * 2),
        "speed": random.uniform(0.002, 0.008),
        "size": random.randint(1, 3)
    }

    asteroids.append(asteroid)

# 6. MOON DAT

moon_distance = 30
moon_angle = 0
moon_speed = 0.08

# 7. MAIN GAME LOOP

running = True

while running:

    # Handle events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    # Clear previous frame
    screen.fill((0, 0, 0))

    # DRAW STARS

    for star in stars:

        star_x = star[0]
        star_y = star[1]
        star_size = star[2]

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (star_x, star_y),
            star_size
        )

    # DRAW SUN

    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (SUN_X, SUN_Y),
        35
    )

    # PROCESS EVERY PLANET

    # We need these for the Moon
    earth_x = 0
    earth_y = 0

    for planet in planets:

        distance = planet["distance"]
        angle = planet["angle"]


        # 3D world coordinates
        x = distance * math.cos(angle)
        y = 0
        z = distance * math.sin(angle)


        # Project 3D -> 2D
        screen_x = SUN_X + x
        screen_y = SUN_Y + z * 0.5

        # Draw planet
        pygame.draw.circle(
            screen,
            planet["color"],
            (int(screen_x), int(screen_y)),
            planet["size"]
        )

        # Save Earth's screen position
        if planet["name"] == "Earth":

            earth_x = screen_x
            earth_y = screen_y
        # Update planet
        planet["angle"] += planet["speed"]

    # DRAW MOON
    moon_x = (
        earth_x
        + moon_distance * math.cos(moon_angle)
    )

    moon_y = (
        earth_y
        + moon_distance * math.sin(moon_angle)
    )

    pygame.draw.circle(
        screen,
        (200, 200, 200),
        (int(moon_x), int(moon_y)),
        4
    )

    moon_angle += moon_speed

    # DRAW ASTEROIDS

    for asteroid in asteroids:

        asteroid_x = (
            SUN_X
            + asteroid["distance"]
            * math.cos(asteroid["angle"])
        )

        asteroid_y = (
            SUN_Y
            + asteroid["distance"]
            * math.sin(asteroid["angle"])
            * 0.5
        )

        pygame.draw.circle(
            screen,
            (130, 130, 130),
            (int(asteroid_x), int(asteroid_y)),
            asteroid["size"]
        )

        asteroid["angle"] += asteroid["speed"]
    # SHOW NEW FRAME
    pygame.display.flip()

    clock.tick(60)


pygame.quit()

