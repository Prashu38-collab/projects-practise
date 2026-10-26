
import colorsys
import math
import random
import turtle

# Screen setup
screen = turtle.Screen()
screen.setup(900, 750)
screen.bgcolor("#09091c")
screen.title("Dream Art Generator")
screen.tracer(0)

artist = turtle.Turtle()
artist.hideturtle()
artist.speed(1)
artist.pensize(1)

# Random dream color palette
palette = [
    "#ff4fa3", "#7b61ff", "#00e5ff",
    "#ffb703", "#80ff72", "#ff6b6b",
    "#e0aaff", "#ffffff"
]

# colorful flower


def dream_flower(cx, cy, size, petals, twist):
    artist.penup()
    artist.goto(cx, cy)
    artist.pendown()

    for i in range(360):
        hue = (i / 360 + random.random() * 0.1) % 1
        color = colorsys.hsv_to_rgb(hue, 0.8, 1)
        artist.pencolor(color)

        angle = i * twist
        radius = size * math.sin(
            math.radians(i * petals)
        )

        x = cx + radius * math.cos(math.radians(angle))
        y = cy + radius * math.sin(math.radians(angle))

        artist.goto(x, y)

# ribbons


def dream_spiral(cx, cy, size):
    artist.penup()
    artist.goto(cx, cy)
    artist.pendown()

    for i in range(500):
        artist.pencolor(random.choice(palette))
        artist.forward(i * size / 500)
        artist.left(91 + math.sin(i / 10) * 12)

# stars


def stars():
    artist.penup()

    for _ in range(180):
        x = random.randint(-430, 430)
        y = random.randint(-350, 350)

        artist.goto(x, y)
        artist.dot(random.randint(2, 5),
                   random.choice(palette))



stars()

for _ in range(7):
    x = random.randint(-250, 250)
    y = random.randint(-200, 200)
    size = random.randint(40, 120)
    petals = random.randint(3, 9)
    twist = random.randint(2, 7)

    dream_flower(x, y, size, petals, twist)

for _ in range(5):
    x = random.randint(-250, 250)
    y = random.randint(-200, 200)

    dream_spiral(x, y, random.uniform(0.5, 1.2))

screen.update()
screen.mainloop()
