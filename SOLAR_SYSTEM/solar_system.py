import pygame
import math

pygame.init()

# 1. SCREEN SETUp

WIDTH = 1000
HEIGHT = 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System V2 - Fake 3D")

clock = pygame.time.Clock()

# 2. SUN POSITIO

SUN_X = WIDTH // 2
SUN_Y = HEIGHT // 2

# 3. PLANET DAT

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

# 4. MAIN GAME LOOp

running = True

while running:

    # Handle events
   
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
    # Clear previous frame
   
    screen.fill((0, 0, 0))
   
    # Draw the Sun
   
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (SUN_X, SUN_Y),
        35
    )

    # 5. PROCESS EVERY PLANE

    for planet in planets:

        distance = planet["distance"]
        angle = planet["angle"]
       
        # 6. CREATE 3D POSITION
       
        x = distance * math.cos(angle)

        z = distance * math.sin(angle)

        y = 0
       
        # 7. PROJECT 3D -2D SCREEN
       
        screen_x = SUN_X + x

        screen_y = SUN_Y + z * 0.5
       
        # 8. DRAW PLANET
    
        pygame.draw.circle(
            screen,
            planet["color"],
            (int(screen_x), int(screen_y)),
            planet["size"]
        )

        # 9. UPDATE PLANET
       
        planet["angle"] += planet["speed"]
    # Show new frame

    pygame.display.flip()

    # Limit FPS

    clock.tick(60)


pygame.quit()