import math
import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A Birthday Wish 🎂")

clock = pygame.time.Clock()

# Colors
BG = (45, 35, 42)
SKIN = (238, 177, 143)
HAIR = (48, 28, 25)
PURPLE = (126, 86, 157)
CREAM = (255, 239, 210)
PINK = (247, 112, 145)
CHOCOLATE = (91, 43, 29)

font = pygame.font.SysFont("Georgia", 34, bold=True)

start_time = pygame.time.get_ticks()
particles = []


def ellipse(color, rect):
    pygame.draw.ellipse(screen, color, rect)


def draw_background():
    screen.fill(BG)

    # Warm background lights
    for x, y, r in [
        (70, 90, 5), (900, 130, 6),
        (830, 70, 4), (110, 200, 4),
        (930, 240, 5), (760, 100, 3)
    ]:
        pygame.draw.circle(screen, (205, 157, 103), (x, y), r)

    # Table
    pygame.draw.rect(screen, (111, 65, 45),
                     (0, 550, WIDTH, 150))
    pygame.draw.line(screen, (171, 110, 73),
                     (0, 565), (WIDTH, 565), 4)


def draw_girl(blowing=False):
    # Hair behind head
    ellipse(HAIR, (85, 100, 310, 350))

    # Body and sweater
    pygame.draw.polygon(
        screen, PURPLE,
        [(60, 520), (90, 365), (190, 315),
         (285, 365), (350, 520)]
    )

    # Neck
    pygame.draw.rect(screen, SKIN, (174, 280, 65, 70))

    # Face
    ellipse(SKIN, (110, 95, 200, 240))

    # Hair framing face
    ellipse(HAIR, (95, 110, 65, 245))
    ellipse(HAIR, (260, 110, 55, 245))
    ellipse(HAIR, (105, 80, 195, 90))

    # Eyes
    for x in (160, 235):
        pygame.draw.ellipse(
            screen, (255, 255, 255),
            (x, 190, 22, 13)
        )
        pygame.draw.circle(
            screen, (40, 27, 24), (x + 12, 196), 6
        )

    # Eyebrows
    pygame.draw.arc(screen, HAIR, (148, 171, 35, 17),
                    0.2, 2.8, 3)
    pygame.draw.arc(screen, HAIR, (224, 171, 35, 17),
                    0.2, 2.8, 3)

    # Nose
    pygame.draw.line(
        screen, (183, 116, 91),
        (202, 205), (196, 224), 2
    )

    # Mouth
    if blowing:
        ellipse((165, 55, 72), (189, 240, 23, 17))
        ellipse((100, 40, 55), (197, 244, 7, 6))
    else:
        pygame.draw.arc(
            screen, (140, 57, 68),
            (177, 232, 42, 26),
            math.pi, 2 * math.pi, 3
        )


def draw_cake():
    # Plate
    ellipse((214, 207, 199), (390, 525, 420, 35))

    # Cake body
    pygame.draw.rect(
        screen, (241, 211, 177),
        (420, 425, 360, 115)
    )

    # Frosting
    pygame.draw.ellipse(
        screen, CREAM, (410, 400, 380, 65)
    )

    # Chocolate top edge
    pygame.draw.arc(
        screen, CHOCOLATE,
        (410, 400, 380, 65), math.pi, 2 * math.pi, 8
    )

    # Dripping chocolate
    for x, length in [
        (445, 24), (490, 38), (540, 22),
        (600, 34), (660, 25), (720, 30)
    ]:
        pygame.draw.line(
            screen, CHOCOLATE,
            (x, 435), (x, 435 + length), 7
        )
        pygame.draw.circle(
            screen, CHOCOLATE,
            (x, 435 + length), 4
        )

    # Cream swirls and cherries
    for x in range(440, 780, 48):
        pygame.draw.circle(screen, (255, 252, 240),
                           (x, 412), 13)
        pygame.draw.circle(screen, (202, 43, 53),
                           (x + 5, 397), 7)

    # Sprinkles
    random.seed(5)
    for _ in range(65):
        x = random.randint(435, 765)
        y = random.randint(450, 525)
        color = random.choice([
            (238, 73, 94), (66, 156, 220),
            (250, 198, 61), (141, 89, 181)
        ])
        pygame.draw.line(
            screen, color, (x, y), (x + 5, y + 3), 3
        )


def draw_candle(flame=True, bend=0, scale=1):
    x, y = 590, 400

    # Candle
    pygame.draw.rect(
        screen, PINK, (x, y - 80, 22, 80)
    )

    # Stripes
    for offset in (12, 35, 58):
        pygame.draw.line(
            screen, (255, 255, 240),
            (x, y - offset), (x + 22, y - offset + 12), 5
        )

    pygame.draw.line(
        screen, (45, 32, 28),
        (x + 11, y - 80), (x + 11, y - 91), 3
    )

    if flame:
        flicker = math.sin(
            pygame.time.get_ticks() * 0.018
        ) * 4

        points = [
            (x + 11 + bend, y - 92),
            (x - 2 + bend, y - 107 - flicker),
            (x + 10 + bend, y - 135 * scale),
            (x + 24 + bend, y - 108 - flicker),
            (x + 11 + bend, y - 92)
        ]

        pygame.draw.polygon(screen, (255, 137, 31), points)

        pygame.draw.ellipse(
            screen, (255, 232, 111),
            (x + 5 + bend, y - 112,
             max(3, int(12 * scale)), max(3, int(18 * scale)))
        )


def draw_air(progress):
    if progress <= 0:
        return

    for strand in range(3):
        points = []

        for i in range(35):
            p = i / 34
            x = 235 + (365 * p * progress)
            y = 260 + strand * 8 + math.sin(
                p * 16 + strand
                + pygame.time.get_ticks() * 0.01
            ) * 5

            points.append((int(x), int(y)))

        if len(points) > 1:
            pygame.draw.lines(
                screen, (184, 211, 224), False, points, 2
            )


def draw_smoke():
    now = pygame.time.get_ticks() / 1000

    points = []
    for i in range(25):
        p = i / 24
        x = 601 + math.sin(now * 3 + p * 8) * 9 * p
        y = 310 - p * 85
        points.append((int(x), int(y)))

    pygame.draw.lines(
        screen, (190, 183, 183), False, points, 3
    )


running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    elapsed = (pygame.time.get_ticks() - start_time) / 1000

    # Animation phases
    blowing = 2.5 <= elapsed < 5.5
    extinguished = elapsed >= 5.5

    progress = max(0, min(1, (elapsed - 2.5) / 2.5))

    if extinguished:
        flame_scale = 0
    elif blowing:
        flame_scale = max(0.15, 1 - progress * 0.8)
    else:
        flame_scale = 1

    bend = progress * 25 if blowing else 0

    draw_background()
    draw_girl(blowing)
    draw_cake()

    draw_candle(
        flame=not extinguished,
        bend=bend,
        scale=flame_scale
    )

    if blowing:
        draw_air(progress)

    if elapsed >= 5.5:
        draw_smoke()

    title = font.render(
        "Happy Birthday!" if elapsed >= 6 else "Make a wish...",
        True, (255, 222, 190)
    )
    screen.blit(title, title.get_rect(center=(500, 45)))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
