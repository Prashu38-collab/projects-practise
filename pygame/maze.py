import math

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magnetic Maze")
clock = pygame.time.Clock()

# Colors
BACKGROUND = (17, 22, 36)
GRID = (27, 34, 52)
WALL_COLOR = (65, 81, 112)
WALL_EDGE = (105, 132, 174)
CYAN = (68, 214, 255)
CYAN_DARK = (26, 117, 155)
GOLD = (255, 197, 77)
GOLD_DARK = (166, 113, 28)
GREEN = (91, 235, 151)
RED = (255, 100, 120)
WHITE = (235, 242, 255)
MUTED = (157, 171, 198)

font = pygame.font.Font(None, 28)
small_font = pygame.font.Font(None, 21)
large_font = pygame.font.Font(None, 58)

# Maze walls are rectangles. All coordinates are in pixels.
WALLS = [
    pygame.Rect(120, 100, 560, 18),
    pygame.Rect(120, 100, 18, 150),
    pygame.Rect(220, 190, 18, 180),
    pygame.Rect(138, 332, 100, 18),
    pygame.Rect(300, 118, 18, 100),
    pygame.Rect(300, 260, 180, 18),
    pygame.Rect(462, 160, 18, 118),
    pygame.Rect(380, 350, 18, 150),
    pygame.Rect(398, 350, 150, 18),
    pygame.Rect(530, 260, 18, 108),
    pygame.Rect(530, 350, 150, 18),
    pygame.Rect(662, 118, 18, 250),
    pygame.Rect(600, 430, 18, 100),
    pygame.Rect(480, 500, 138, 18),
    pygame.Rect(120, 430, 180, 18),
    pygame.Rect(120, 430, 18, 100),
    pygame.Rect(220, 500, 18, 50),
]

PLAYER_START = (65, 65)
BALL_START = (340, 220)
PLATE = pygame.Rect(565, 445, 42, 42)
EXIT = pygame.Rect(705, 505, 55, 55)
PLAYER_SIZE = 28
BALL_RADIUS = 12
PLAYER_SPEED = 3.2
BALL_FRICTION = 0.94
MAGNET_STRENGTH = 0.17
MAX_BALL_SPEED = 5.0


def reset_game():
    player = pygame.Rect(
        PLAYER_START[0], PLAYER_START[1], PLAYER_SIZE, PLAYER_SIZE)
    ball_pos = pygame.Vector2(BALL_START)
    ball_velocity = pygame.Vector2(0, 0)
    return player, ball_pos, ball_velocity, False, False, False, 0


def draw_text(text, font_obj, color, x, y, center=False):
    image = font_obj.render(text, True, color)
    rect = image.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(image, rect)


def circle_hits_wall(pos, radius):
    for wall in WALLS:
        closest_x = max(wall.left, min(pos.x, wall.right))
        closest_y = max(wall.top, min(pos.y, wall.bottom))
        dx = pos.x - closest_x
        dy = pos.y - closest_y
        if dx * dx + dy * dy < radius * radius:
            return True
    return False


def move_player(player, dx, dy):
    # Resolve each axis separately so the player can slide along walls.
    player.x += round(dx)
    for wall in WALLS:
        if player.colliderect(wall):
            if dx > 0:
                player.right = wall.left
            elif dx < 0:
                player.left = wall.right

    player.y += round(dy)
    for wall in WALLS:
        if player.colliderect(wall):
            if dy > 0:
                player.bottom = wall.top
            elif dy < 0:
                player.top = wall.bottom

    player.clamp_ip(screen.get_rect())


def move_ball(ball_pos, velocity):
    # Move X and Y independently to let the ball slide along walls.
    ball_pos.x += velocity.x
    if circle_hits_wall(ball_pos, BALL_RADIUS):
        ball_pos.x -= velocity.x
        velocity.x *= -0.55

    ball_pos.y += velocity.y
    if circle_hits_wall(ball_pos, BALL_RADIUS):
        ball_pos.y -= velocity.y
        velocity.y *= -0.55

    ball_pos.x = max(BALL_RADIUS, min(WIDTH - BALL_RADIUS, ball_pos.x))
    ball_pos.y = max(BALL_RADIUS, min(HEIGHT - BALL_RADIUS, ball_pos.y))


player, ball_pos, ball_velocity, magnet_on, won, show_help, moves = reset_game()
running = True

while running:
    dt = clock.tick(FPS) / 1000.0
    dt = min(dt, 0.04)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_SPACE and not won:
                magnet_on = not magnet_on
            elif event.key == pygame.K_r:
                player, ball_pos, ball_velocity, magnet_on, won, show_help, moves = reset_game()
            elif event.key == pygame.K_h:
                show_help = not show_help

    keys = pygame.key.get_pressed()

    if not won:
        dx = 0
        dy = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += PLAYER_SPEED
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= PLAYER_SPEED
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += PLAYER_SPEED

        if dx and dy:
            diagonal_factor = 1 / math.sqrt(2)
            dx *= diagonal_factor
            dy *= diagonal_factor

        if dx or dy:
            old_pos = player.topleft
            move_player(player, dx, dy)
            if player.topleft != old_pos:
                moves += 1

        # The magnet attracts the ball toward the robot's center.
        if magnet_on:
            player_center = pygame.Vector2(player.center)
            toward_player = player_center - ball_pos
            distance = toward_player.length()
            if distance > 1:
                # Attraction gets weaker with distance and is capped for control.
                force = min(MAGNET_STRENGTH, 150 / (distance * distance + 900))
                ball_velocity += toward_player.normalize() * force * 18

        if ball_velocity.length() > MAX_BALL_SPEED:
            ball_velocity.scale_to_length(MAX_BALL_SPEED)

        ball_velocity *= BALL_FRICTION
        if ball_velocity.length() < 0.035:
            ball_velocity.update(0, 0)

        move_ball(ball_pos, ball_velocity)

        plate_center = pygame.Vector2(PLATE.center)
        ball_on_plate = ball_pos.distance_to(plate_center) < 22
        if ball_on_plate and player.colliderect(EXIT):
            won = True

    # Background and subtle grid
    screen.fill(BACKGROUND)
    for x in range(0, WIDTH, 40):
        pygame.draw.line(screen, GRID, (x, 0), (x, HEIGHT), 1)
    for y in range(0, HEIGHT, 40):
        pygame.draw.line(screen, GRID, (0, y), (WIDTH, y), 1)

    # Exit changes color when the ball activates the plate.
    ball_on_plate = ball_pos.distance_to(pygame.Vector2(PLATE.center)) < 22
    exit_color = GREEN if ball_on_plate else RED
    pygame.draw.rect(screen, (35, 45, 64), EXIT.inflate(8, 8), border_radius=8)
    pygame.draw.rect(screen, exit_color, EXIT, border_radius=6)
    pygame.draw.rect(screen, BACKGROUND,
                     EXIT.inflate(-20, -12), border_radius=3)
    draw_text("EXIT", small_font, WHITE, EXIT.centerx,
              EXIT.top - 18, center=True)

    # Pressure plate
    plate_color = GREEN if ball_on_plate else GOLD
    pygame.draw.rect(screen, (40, 47, 65),
                     PLATE.inflate(10, 10), border_radius=8)
    pygame.draw.rect(screen, plate_color, PLATE, border_radius=6)
    pygame.draw.rect(screen, BACKGROUND,
                     PLATE.inflate(-12, -12), border_radius=3)
    draw_text("PLATE", small_font, plate_color,
              PLATE.centerx, PLATE.bottom + 14, center=True)

    # Maze walls
    for wall in WALLS:
        pygame.draw.rect(screen, WALL_COLOR, wall, border_radius=4)
        pygame.draw.rect(screen, WALL_EDGE, wall, width=2, border_radius=4)

    # Magnetic field effect
    if magnet_on and not won:
        pygame.draw.circle(screen, CYAN_DARK, player.center, 95, 1)
        pygame.draw.circle(screen, CYAN_DARK, player.center, 65, 1)
        pygame.draw.line(screen, CYAN_DARK, player.center,
                         (round(ball_pos.x), round(ball_pos.y)), 2)

    # Metal ball
    pygame.draw.circle(screen, GOLD_DARK, (round(ball_pos.x),
                       round(ball_pos.y)), BALL_RADIUS + 3)
    pygame.draw.circle(screen, GOLD, (round(ball_pos.x),
                       round(ball_pos.y)), BALL_RADIUS)
    pygame.draw.circle(screen, WHITE, (round(
        ball_pos.x - 4), round(ball_pos.y - 4)), 3)

    # Robot body and eye
    pygame.draw.rect(screen, CYAN_DARK, player.inflate(6, 6), border_radius=8)
    pygame.draw.rect(screen, CYAN, player, border_radius=6)
    pygame.draw.circle(screen, BACKGROUND,
                       (player.centerx + 5, player.centery - 3), 4)
    pygame.draw.circle(
        screen, WHITE, (player.centerx + 6, player.centery - 4), 1)

    # Header and instructions
    pygame.draw.rect(screen, (12, 16, 28), (0, 0, WIDTH, 48))
    draw_text("MAGNETIC MAZE", font, WHITE, 18, 13)
    magnet_label = "MAGNET ON" if magnet_on else "MAGNET OFF"
    magnet_color = CYAN if magnet_on else MUTED
    draw_text(magnet_label, small_font, magnet_color, 245, 16)
    draw_text("SPACE: magnet   R: restart   H: help   ESC: quit",
              small_font, MUTED, 420, 16)

    if show_help:
        panel = pygame.Rect(190, 175, 420, 230)
        pygame.draw.rect(screen, (12, 16, 28), panel, border_radius=12)
        pygame.draw.rect(screen, WALL_EDGE, panel, 2, border_radius=12)
        draw_text("HOW TO PLAY", font, WHITE,
                  panel.centerx, panel.y + 30, center=True)
        draw_text("Move: Arrow keys or WASD", small_font,
                  MUTED, panel.x + 28, panel.y + 72)
        draw_text("Press SPACE to toggle the magnet.",
                  small_font, MUTED, panel.x + 28, panel.y + 102)
        draw_text("Pull the gold ball onto the plate.",
                  small_font, MUTED, panel.x + 28, panel.y + 132)
        draw_text("Then guide the robot to the exit.",
                  small_font, MUTED, panel.x + 28, panel.y + 162)
        draw_text("Press H to close this panel.", small_font,
                  CYAN, panel.x + 28, panel.y + 192)

    if won:
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((5, 10, 20, 190))
        screen.blit(overlay, (0, 0))
        draw_text("MAZE SOLVED!", large_font, GREEN,
                  WIDTH // 2, HEIGHT // 2 - 42, center=True)
        draw_text("You activated the pressure plate and reached the exit.", font, WHITE,
                  WIDTH // 2, HEIGHT // 2 + 8, center=True)
        draw_text("Press R to play again or ESC to quit.", small_font, MUTED,
                  WIDTH // 2, HEIGHT // 2 + 48, center=True)

    pygame.display.flip()

pygame.quit()
