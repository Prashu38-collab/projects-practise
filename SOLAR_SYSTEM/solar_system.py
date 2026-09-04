import pygame
import math

pygame.init()


# Screen setup

WIDTH, HEIGHT = 1000, 900

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Simulation")

clock = pygame.time.Clock()


# Sun position

SUN_X = WIDTH // 2
SUN_Y = HEIGHT // 2



# Planet orbit distances

mercury_distance = 60
venus_distance = 100
earth_distance = 150
mars_distance = 200
jupiter_distance = 270
saturn_distance = 340
uranus_distance = 410
neptune_distance = 480



# Planet angles

mercury_angle = 0
venus_angle = 1
earth_angle = 2
mars_angle = 3
jupiter_angle = 4
saturn_angle = 5
uranus_angle = 6
neptune_angle = 7



# Planet speeds

mercury_speed = 0.05
venus_speed = 0.04
earth_speed = 0.03
mars_speed = 0.025
jupiter_speed = 0.015
saturn_speed = 0.012
uranus_speed = 0.008
neptune_speed = 0.006


running = True

while running:

    
    # Handle events
    
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False


    
    # Background
    
    screen.fill((0, 0, 0))


    
    # Draw Sun
    
    pygame.draw.circle(
        screen,
        (255, 255, 0),
        (SUN_X, SUN_Y),
        35
    )


    
    # MERCURY
    

    mercury_x = SUN_X + mercury_distance * math.cos(mercury_angle)
    mercury_y = SUN_Y + mercury_distance * math.sin(mercury_angle)

    pygame.draw.circle(
        screen,
        (169, 169, 169),
        (int(mercury_x), int(mercury_y)),
        5
    )


    
    # VENUS
    

    venus_x = SUN_X + venus_distance * math.cos(venus_angle)
    venus_y = SUN_Y + venus_distance * math.sin(venus_angle)

    pygame.draw.circle(
        screen,
        (255, 165, 0),
        (int(venus_x), int(venus_y)),
        8
    )


    
    # EARTH
    

    earth_x = SUN_X + earth_distance * math.cos(earth_angle)
    earth_y = SUN_Y + earth_distance * math.sin(earth_angle)

    pygame.draw.circle(
        screen,
        (0, 100, 255),
        (int(earth_x), int(earth_y)),
        10
    )


    
    # MARS
    

    mars_x = SUN_X + mars_distance * math.cos(mars_angle)
    mars_y = SUN_Y + mars_distance * math.sin(mars_angle)

    pygame.draw.circle(
        screen,
        (255, 70, 50),
        (int(mars_x), int(mars_y)),
        8
    )


    
    # JUPITER
    

    jupiter_x = SUN_X + jupiter_distance * math.cos(jupiter_angle)
    jupiter_y = SUN_Y + jupiter_distance * math.sin(jupiter_angle)

    pygame.draw.circle(
        screen,
        (210, 140, 80),
        (int(jupiter_x), int(jupiter_y)),
        22
    )


    
    # SATURN
    

    saturn_x = SUN_X + saturn_distance * math.cos(saturn_angle)
    saturn_y = SUN_Y + saturn_distance * math.sin(saturn_angle)

    pygame.draw.circle(
        screen,
        (230, 200, 120),
        (int(saturn_x), int(saturn_y)),
        18
    )


    
    # URANUS
    

    uranus_x = SUN_X + uranus_distance * math.cos(uranus_angle)
    uranus_y = SUN_Y + uranus_distance * math.sin(uranus_angle)

    pygame.draw.circle(
        screen,
        (100, 220, 255),
        (int(uranus_x), int(uranus_y)),
        14
    )


    
    # NEPTUNE
    

    neptune_x = SUN_X + neptune_distance * math.cos(neptune_angle)
    neptune_y = SUN_Y + neptune_distance * math.sin(neptune_angle)

    pygame.draw.circle(
        screen,
        (50, 80, 255),
        (int(neptune_x), int(neptune_y)),
        13
    )


    
    # Update all planet angles
    
    mercury_angle += mercury_speed
    venus_angle += venus_speed
    earth_angle += earth_speed
    mars_angle += mars_speed
    jupiter_angle += jupiter_speed
    saturn_angle += saturn_speed
    uranus_angle += uranus_speed
    neptune_angle += neptune_speed


    
    # Update display
    
    pygame.display.flip()

    # 60 FPS
    clock.tick(60)


pygame.quit()