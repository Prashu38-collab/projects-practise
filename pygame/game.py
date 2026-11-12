import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 600, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge the Blocks")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 40)

PLAYER_SIZE = 50
player = pygame.Rect(WIDTH // 2 - PLAYER_SIZE // 2,
                     HEIGHT - 90, PLAYER_SIZE, PLAYER_SIZE)
player_speed = 7

BLOCK_SIZE = 40
blocks = []
block_timer = 0
score = 0
game_over = False


def draw_text(text, x, y, color=(255, 255, 255)):
    image = font.render(text, True, color)
    screen.blit(image, (x, y))


while True:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            player.x = WIDTH // 2 - PLAYER_SIZE // 2
            blocks.clear()
            score = 0
            block_timer = 0
            game_over = False

    keys = pygame.key.get_pressed()

    if not game_over:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player.x += player_speed

        player.clamp_ip(screen.get_rect())

        block_timer += dt
        if block_timer >= 650:
            x = random.randint(0, WIDTH - BLOCK_SIZE)
            blocks.append(pygame.Rect(x, -BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            block_timer = 0

        for block in blocks[:]:
            block.y += 5
            if block.top > HEIGHT:
                blocks.remove(block)
                score += 1
            elif player.colliderect(block):
                game_over = True

    screen.fill((25, 30, 45))
    pygame.draw.rect(screen, (70, 200, 255), player)

    for block in blocks:
        pygame.draw.rect(screen, (255, 90, 90), block)

    draw_text(f"Score: {score}", 20, 20)

    if game_over:
        draw_text("Game Over!", WIDTH // 2 - 90,
                  HEIGHT // 2 - 40, (255, 100, 100))
        draw_text("Press R to restart", WIDTH // 2 - 125, HEIGHT // 2 + 10)

    pygame.display.flip()
