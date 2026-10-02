

import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Neon Dodge")
clock = pygame.time.Clock()

WHITE = (240, 240, 255)
BLACK = (10, 10, 22)
CYAN = (0, 235, 255)
PINK = (255, 50, 170)
YELLOW = (255, 230, 70)

font = pygame.font.SysFont("arial", 30, bold=True)
big_font = pygame.font.SysFont("arial", 58, bold=True)


class Player:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40)
        self.speed = 7

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.rect.y += self.speed

        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        pygame.draw.rect(screen, CYAN, self.rect, border_radius=8)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=8)


class Enemy:
    def __init__(self, speed):
        size = random.randint(22, 50)
        self.rect = pygame.Rect(
            random.randint(0, WIDTH - size),
            -size,
            size,
            size
        )
        self.speed = speed + random.uniform(0, 2)

    def update(self):
        self.rect.y += self.speed

    def draw(self):
        pygame.draw.rect(screen, PINK, self.rect, border_radius=6)
        pygame.draw.rect(screen, WHITE, self.rect, 1, border_radius=6)


def draw_text(text, text_font, color, x, y):
    image = text_font.render(text, True, color)
    screen.blit(image, (x, y))


def game():
    player = Player()
    enemies = []
    score = 0
    spawn_timer = 0
    running = True
    game_over = False

    while running:
        dt = clock.tick(60)
        screen.fill(BLACK)

        # Grid background
        for x in range(0, WIDTH, 40):
            pygame.draw.line(screen, (20, 25, 50), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, 40):
            pygame.draw.line(screen, (20, 25, 50), (0, y), (WIDTH, y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return game()
                if event.key == pygame.K_ESCAPE:
                    running = False

        if not game_over:
            player.move()

            spawn_timer += dt
            if spawn_timer > max(250, 850 - score * 8):
                enemies.append(Enemy(4 + score / 35))
                spawn_timer = 0

            for enemy in enemies[:]:
                enemy.update()

                if enemy.rect.top > HEIGHT:
                    enemies.remove(enemy)
                    score += 1

                if player.rect.colliderect(enemy.rect):
                    game_over = True

            player.draw()
            for enemy in enemies:
                enemy.draw()

            draw_text(f"Score: {score}", font, YELLOW, 20, 18)

        else:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))

            title = big_font.render("GAME OVER", True, PINK)
            score_text = font.render(f"Final score: {score}", True, WHITE)
            restart = font.render(
                "Press R to restart or ESC to quit", True, CYAN)

            screen.blit(title, title.get_rect(center=(WIDTH // 2, 235)))
            screen.blit(score_text, score_text.get_rect(
                center=(WIDTH // 2, 315)))
            screen.blit(restart, restart.get_rect(center=(WIDTH // 2, 375)))

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    game()
