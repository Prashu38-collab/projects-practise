
import math
import random
import sys

import pygame

pygame.init()

WIDTH, HEIGHT = 1100, 720
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("METRO MANAGER")

clock = pygame.time.Clock()

# Colours
BG = (20, 24, 34)
PANEL = (29, 35, 48)
WHITE = (240, 243, 250)
MUTED = (145, 155, 175)
BLUE = (75, 160, 255)
GREEN = (75, 220, 160)
RED = (255, 100, 110)
YELLOW = (255, 205, 90)
PURPLE = (180, 130, 255)
GRID = (32, 39, 52)

font = pygame.font.SysFont("arial", 20)
small_font = pygame.font.SysFont("arial", 15)
title_font = pygame.font.SysFont("arial", 30, bold=True)

class Station:

    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.queue = []

    def draw(self):
        # Station circle
        congestion = len(self.queue)

        color = WHITE
        if congestion >= 7:
            color = RED
        elif congestion >= 4:
            color = YELLOW

        pygame.draw.circle(
            screen, color,
            (self.x, self.y), 14
        )

        pygame.draw.circle(
            screen, BG,
            (self.x, self.y), 8
        )

        pygame.draw.circle(
            screen, color,
            (self.x, self.y), 14, 2
        )

        # Station name
        label = small_font.render(
            self.name, True, WHITE
        )

        screen.blit(
            label,
            (self.x - label.get_width() // 2,
             self.y + 22)
        )

        # Passenger count
        count = small_font.render(
            str(congestion), True, YELLOW
        )

        screen.blit(
            count,
            (self.x + 17, self.y - 23)
        )

class Train:

    def __init__(self):
        self.current = 0
        self.next = 1
        self.progress = 0

        self.speed = 0.30
        self.capacity = 5
        self.passengers = []

        self.dwell = 1.0
        self.stopped = True

        self.x = 0
        self.y = 0

    def arrive(self, stations, route, game):
        station = stations[self.current]

        # Drop off passengers
        delivered = [
            p for p in self.passengers
            if p == self.current
        ]

        self.passengers = [
            p for p in self.passengers
            if p != self.current
        ]

        game.score += len(delivered) * 10
        game.money += len(delivered) * 5

        # Pick up passengers whose destinations
        # are reachable on the current route
        available = self.capacity - len(self.passengers)

        for destination in list(station.queue):

            if available <= 0:
                break

            if destination in route and destination != self.current:
                self.passengers.append(destination)
                station.queue.remove(destination)
                available -= 1

    def update(self, dt, stations, route, game):

        if len(route) < 2:
            return

        if self.stopped:
            self.dwell -= dt

            if self.dwell <= 0:
                self.stopped = False
                self.next = (
                    self.current + 1
                ) % len(route)
                self.progress = 0

            return

        self.progress += self.speed * dt

        if self.progress >= 1:
            self.progress = 1

            self.current = self.next
            self.stopped = True
            self.dwell = 1.0

            self.arrive(stations, route, game)

        # Interpolate position between stations
        a = stations[route[self.current]]
        b = stations[route[self.next]]

        t = self.progress

        self.x = a.x + (b.x - a.x) * t
        self.y = a.y + (b.y - a.y) * t

    def draw(self, stations, route):

        if len(route) < 2:
            return

        a = stations[route[self.current]]
        b = stations[route[self.next]]

        if self.stopped:
            x, y = a.x, a.y
        else:
            x, y = self.x, self.y

        pygame.draw.circle(
            screen, BLUE,
            (int(x), int(y)), 12
        )

        pygame.draw.circle(
            screen, WHITE,
            (int(x), int(y)), 5
        )

class Game:

    def __init__(self):

        self.stations = [
            Station("Central", 200, 220),
            Station("Museum", 430, 140),
            Station("Market", 680, 220),
            Station("University", 850, 430),
            Station("Airport", 420, 510),
        ]

        self.route = []
        self.train = Train()

        self.score = 0
        self.money = 100
        self.elapsed = 0

        self.spawn_timer = 0
        self.running = True

    def spawn_passenger(self):

        if len(self.route) < 2:
            return

        station_index = random.choice(self.route)

        possible_destinations = [
            i for i in self.route
            if i != station_index
        ]

        if possible_destinations:
            destination = random.choice(
                possible_destinations
            )

            self.stations[station_index].queue.append(
                destination
            )

    def handle_click(self, pos):

        for i, station in enumerate(self.stations):

            distance = math.hypot(
                pos[0] - station.x,
                pos[1] - station.y
            )

            if distance < 22:

                if i not in self.route:
                    self.route.append(i)

                elif self.route[-1] != i:
                    self.route.append(i)

                return

    def update(self, dt):

        self.elapsed += dt
        self.spawn_timer += dt

        # Passenger generation
        if self.spawn_timer >= 2:
            self.spawn_passenger()
            self.spawn_timer = 0

        # Train simulation
        self.train.update(
            dt, self.stations, self.route, self
        )

        # Congestion penalty
        for station in self.stations:
            if len(station.queue) > 8:
                self.score = max(
                    0, self.score - 1
                )

    def draw_grid(self):

        for x in range(0, WIDTH, 40):
            pygame.draw.line(
                screen, GRID,
                (x, 100), (x, HEIGHT)
            )

        for y in range(100, HEIGHT, 40):
            pygame.draw.line(
                screen, GRID,
                (0, y), (WIDTH, y)
            )

    def draw(self):

        screen.fill(BG)
        self.draw_grid()

        # Header
        pygame.draw.rect(
            screen, PANEL,
            (0, 0, WIDTH, 100)
        )

        title = title_font.render(
            "METRO MANAGER", True, WHITE
        )

        screen.blit(title, (35, 25))

        # Statistics
        stats = [
            f"Score: {self.score}",
            f"Money: ${self.money}",
            f"Passengers: {sum(len(s.queue) for s in self.stations)}",
            f"Time: {int(self.elapsed)}s"
        ]

        for i, item in enumerate(stats):
            label = font.render(
                item, True, GREEN
            )
            screen.blit(label, (400 + i * 165, 40))

        # Railway lines
        if len(self.route) >= 2:

            for i in range(len(self.route) - 1):

                a = self.stations[self.route[i]]
                b = self.stations[self.route[i + 1]]

                pygame.draw.line(
                    screen, BLUE,
                    (a.x, a.y),
                    (b.x, b.y),
                    6
                )

            # Close the route to form a loop
            a = self.stations[self.route[-1]]
            b = self.stations[self.route[0]]

            pygame.draw.line(
                screen, BLUE,
                (a.x, a.y),
                (b.x, b.y),
                3
            )

        # Stations
        for station in self.stations:
            station.draw()

        # Train
        self.train.draw(
            self.stations, self.route
        )

        # Instructions
        instructions = [
            "CLICK stations to build your railway route",
            "RIGHT CLICK to undo the last connection",
            "Passengers travel to their chosen destinations",
            "R - Reset route     ESC - Quit"
        ]

        for i, instruction in enumerate(instructions):
            label = small_font.render(
                instruction, True, MUTED
            )
            screen.blit(
                label, (30, HEIGHT - 105 + i * 22)
            )

        # Train capacity
        capacity = small_font.render(
            f"Train: {len(self.train.passengers)}/{self.train.capacity} passengers",
            True, YELLOW
        )

        screen.blit(capacity, (WIDTH - 290, HEIGHT - 45))

        # Overcrowding warning
        crowded = [
            s.name for s in self.stations
            if len(s.queue) >= 7
        ]

        if crowded:
            warning = title_font.render(
                "STATION OVERCROWDING!",
                True, RED
            )
            screen.blit(
                warning, (350, 115)
            )


def main():

    game = Game()

    while game.running:

        dt = min(clock.tick(FPS) / 1000, 0.05)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game.running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:

                if event.button == 1:
                    game.handle_click(event.pos)

                elif event.button == 3 and game.route:
                    game.route.pop()

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    game.running = False

                elif event.key == pygame.K_r:
                    game.route.clear()
                    game.train = Train()

        game.update(dt)
        game.draw()

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
