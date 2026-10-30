import math
import random
import turtle

# SCREEN SETUP
screen = turtle.Screen()
screen.setup(1000, 700)
screen.title("Deep Blue | Interactive Aquarium")
screen.bgcolor("#061B33")
screen.tracer(0)

WIDTH = 1000
HEIGHT = 700


# DRAWING HELPER
def draw_polygon(pen, points, color):
    pen.penup()
    pen.goto(points[0])
    pen.pendown()
    pen.fillcolor(color)
    pen.begin_fill()

    for point in points[1:]:
        pen.goto(point)

    pen.goto(points[0])
    pen.end_fill()
    pen.penup()



# AQUARIUM DECORATIONS
background = turtle.Turtle()
background.hideturtle()
background.speed(0)

# Ocean floor
draw_polygon(
    background,
    [(-500, -300), (-500, -240), (-300, -255),
     (-100, -235), (100, -260), (300, -240),
     (500, -260), (500, -300)],
    "#C28B45"
)

# Seaweed
for x in [-430, -390, -150, 180, 400, 450]:
    background.penup()
    background.goto(x, -250)
    background.pendown()
    background.pensize(5)
    background.pencolor("#16A085")

    for i in range(5):
        background.setheading(90 if i % 2 == 0 else 70)
        background.circle(15, 45)

    background.penup()

# Decorative rocks
for _ in range(25):
    x = random.randint(-480, 480)
    y = random.randint(-285, -255)

    background.goto(x, y)
    background.dot(random.randint(8, 20), "#73563E")



# FISH CLASS
class Fish:

    def __init__(self, x, y, color, speed, size=1):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.size = size

        self.direction = random.choice([-1, 1])

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)
        self.pen.penup()

    def draw(self):

        self.pen.clear()

        s = self.size
        d = self.direction

        # Fish body
        self.pen.goto(self.x, self.y)
        self.pen.dot(35 * s, self.color)

        # Tail
        tail = [
            (self.x - d * 15 * s, self.y),
            (self.x - d * 35 * s, self.y + 13 * s),
            (self.x - d * 35 * s, self.y - 13 * s)
        ]

        draw_polygon(self.pen, tail, self.color)

        # Eye
        self.pen.goto(self.x + d * 9 * s, self.y + 5 * s)
        self.pen.dot(6 * s, "white")

        self.pen.goto(self.x + d * 11 * s, self.y + 5 * s)
        self.pen.dot(3 * s, "black")

        # Small mouth
        self.pen.goto(self.x + d * 16 * s, self.y - 3 * s)
        self.pen.dot(3 * s, "black")

    def move(self):

        self.x += self.speed * self.direction

        # Change direction at boundaries
        if self.x > 470 or self.x < -470:
            self.direction *= -1

        # Gentle swimming motion
        self.y += math.sin(self.x / 35) * 0.8

    def update(self):
        self.move()
        self.draw()



# CREATE FISH


fish_colors = [
    "#FF6B6B",
    "#FFD93D",
    "#6BCB77",
    "#4D96FF",
    "#FF8FAB",
    "#C77DFF"
]

fishes = []

for i in range(9):
    fish = Fish(
        random.randint(-400, 400),
        random.randint(-180, 200),
        random.choice(fish_colors),
        random.uniform(1, 3),
        random.uniform(0.8, 1.4) # type: ignore
    )

    fishes.append(fish)



# BUBBLE CLASS


class Bubble:

    def __init__(self):
        self.x = random.randint(-470, 470)
        self.y = random.randint(-250, 300)
        self.radius = random.randint(3, 9)
        self.speed = random.uniform(1, 3)

        self.pen = turtle.Turtle()
        self.pen.hideturtle()
        self.pen.speed(0)

    def update(self):

        self.y += self.speed

        if self.y > 340:
            self.y = -280
            self.x = random.randint(-470, 470)

        self.pen.clear()
        self.pen.penup()
        self.pen.goto(self.x, self.y)
        self.pen.pendown()
        self.pen.pencolor("#9DEBFF")
        self.pen.pensize(2)
        self.pen.circle(self.radius)
        self.pen.penup()


bubbles = [Bubble() for _ in range(30)]



# TITLE


title = turtle.Turtle()
title.hideturtle()
title.penup()
title.goto(0, 300)
title.color("#A7E8FF")
title.write(
    "D E E P   B L U E",
    align="center",
    font=("Arial", 25, "bold")
)

subtitle = turtle.Turtle()
subtitle.hideturtle()
subtitle.penup()
subtitle.goto(0, 270)
subtitle.color("white")
subtitle.write(
    "An Interactive Underwater World",
    align="center",
    font=("Arial", 11, "italic")
)



# INTERACTIVE CONTROLS


paused = False
speed_multiplier = 1.0

status = turtle.Turtle()
status.hideturtle()
status.penup()
status.color("white")
status.goto(-470, 310)


def show_status():
    status.clear()
    status.write(
        f"Speed: {speed_multiplier:.1f}x | "
        f"{'PAUSED' if paused else 'RUNNING'}",
        font=("Arial", 11, "bold")
    )


def toggle_pause():
    global paused
    paused = not paused
    show_status()


def increase_speed():
    global speed_multiplier
    speed_multiplier = min(3.0, speed_multiplier + 0.2)
    show_status()


def decrease_speed():
    global speed_multiplier
    speed_multiplier = max(0.2, speed_multiplier - 0.2)
    show_status()


def reset_aquarium():
    global speed_multiplier

    speed_multiplier = 1.0

    for fish in fishes:
        fish.x = random.randint(-400, 400)
        fish.y = random.randint(-180, 200)

    show_status()


screen.listen()
screen.onkey(toggle_pause, "space")
screen.onkey(increase_speed, "Up")
screen.onkey(decrease_speed, "Down")
screen.onkey(reset_aquarium, "r")



# ANIMATION ENGINE


def animate():

    if not paused:

        for fish in fishes:
            original_speed = fish.speed
            fish.speed = original_speed * speed_multiplier
            fish.update()
            fish.speed = original_speed

        for bubble in bubbles:
            bubble.speed = bubble.speed
            bubble.update()

    screen.update()
    screen.ontimer(animate, 30)


show_status()
animate()

screen.mainloop()
