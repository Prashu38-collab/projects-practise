
import random
import sys
import time

import pygame

pygame.init()
WIDTH, HEIGHT = 1000, 650
FPS = 60
DURATION = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TypeRush | Typing Speed Test")

clock = pygame.time.Clock()

# Colors
BG = (18, 18, 28)
PANEL = (28, 28, 42)
WHITE = (240, 240, 245)
GREY = (130, 130, 150)
GREEN = (70, 220, 150)
RED = (255, 90, 110)
PURPLE = (155, 110, 255)

# Fonts
title_font = pygame.font.SysFont("arial", 38, bold=True)
normal_font = pygame.font.SysFont("arial", 24)
small_font = pygame.font.SysFont("arial", 18)
word_font = pygame.font.SysFont("arial", 25)

# ---------------- SENTENCES ----------------

SENTENCES = [
    "Python makes programming simple and enjoyable.",
    "Practice every day to become a better developer.",
    "Consistency is more important than motivation.",
    "Great software starts with solving small problems.",
    "Technology changes the world one idea at a time.",
    "Learning to code requires patience and practice.",
    "Build projects to improve your programming skills.",
    "Every expert was once a beginner."
]


def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))


class TypingTest:

    def __init__(self):
        self.reset()

    def reset(self):
        self.target = random.choice(SENTENCES)
        self.typed = ""
        self.start_time = None
        self.end_time = None
        self.finished = False
        self.duration = DURATION

    def elapsed(self):
        if self.start_time is None:
            return 0

        end = self.end_time if self.finished else time.time()
        return end - self.start_time # type: ignore

    def remaining(self):
        return max(0, self.duration - self.elapsed())

    def calculate_wpm(self):
        minutes = self.elapsed() / 60

        if minutes <= 0:
            return 0

        return round((len(self.typed) / 5) / minutes)

    def calculate_accuracy(self):
        if not self.typed:
            return 100

        correct = sum(
            1 for i, char in enumerate(self.typed)
            if i < len(self.target) and char == self.target[i]
        )

        return round((correct / len(self.typed)) * 100)

    def handle_input(self, event):
        if self.finished:
            return

        if event.key == pygame.K_BACKSPACE:
            self.typed = self.typed[:-1]

        elif event.key == pygame.K_RETURN:
            return

        elif event.unicode.isprintable() and len(self.typed) < len(self.target):
            if self.start_time is None:
                self.start_time = time.time()

            self.typed += event.unicode

        if len(self.typed) == len(self.target):
            self.finish()

    def finish(self):
        self.finished = True
        self.end_time = time.time()

    def update(self):
        if self.start_time is not None and self.remaining() <= 0:
            self.finish()

    def draw_sentence(self):
        x, y = 80, 300

        for i, char in enumerate(self.target):
            if i < len(self.typed):
                color = GREEN if self.typed[i] == char else RED
            else:
                color = GREY

            rendered = word_font.render(char, True, color)
            screen.blit(rendered, (x, y))

            x += rendered.get_width()

            if x > WIDTH - 80:
                x = 80
                y += 40

    def draw(self):
        screen.fill(BG)

        # Header
        draw_text("TYPERUSH", title_font, PURPLE, 70, 45)
        draw_text("Typing Speed Challenge", small_font, GREY, 73, 95)

        # Statistics panel
        pygame.draw.rect(
            screen, PANEL,
            (70, 150, 860, 110),
            border_radius=15
        )

        draw_text(
            f"WPM: {self.calculate_wpm()}",
            normal_font, GREEN, 110, 185
        )

        draw_text(
            f"Accuracy: {self.calculate_accuracy()}%",
            normal_font, WHITE, 380, 185
        )

        draw_text(
            f"Time: {int(self.remaining())}s",
            normal_font, PURPLE, 700, 185
        )

        # Typing area
        pygame.draw.rect(
            screen, PANEL,
            (70, 280, 860, 150),
            border_radius=15
        )

        self.draw_sentence()

        # Instructions
        if self.start_time is None:
            instruction = "Start typing to begin the timer!"
        else:
            instruction = "Keep going! Accuracy matters."

        draw_text(instruction, small_font, GREY, 75, 470)

        draw_text(
            "Press ESC to quit | BACKSPACE to correct",
            small_font, GREY, 75, 550
        )

        # Results
        if self.finished:
            pygame.draw.rect(
                screen, PANEL,
                (250, 200, 500, 280),
                border_radius=20
            )

            draw_text(
                "CHALLENGE COMPLETE",
                title_font, PURPLE, 285, 230
            )

            draw_text(
                f"Final WPM: {self.calculate_wpm()}",
                normal_font, GREEN, 390, 310
            )

            draw_text(
                f"Accuracy: {self.calculate_accuracy()}%",
                normal_font, WHITE, 390, 355
            )

            draw_text(
                "Press R to play again",
                small_font, GREY, 390, 420
            )

def main():
    game = TypingTest()

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    running = False

                elif event.key == pygame.K_r and game.finished:
                    game.reset()

                else:
                    game.handle_input(event)

        game.update()
        game.draw()

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
