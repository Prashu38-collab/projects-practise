
import turtle
import random

# Screen setup
screen = turtle.Screen()
screen.setup(900, 700)
screen.bgcolor("#10152f")
screen.title("Happy Tihar")
screen.tracer(0)

t = turtle.Turtle()
t.speed(0)
t.hideturtle()
t.pensize(3)

# Light colors
light_colors = [
    "#ff3b6b", "#ffd93d", "#49f2c2",
    "#6b8cff", "#ff8c42", "#ff5cff",
    "#ffffff", "#00e5ff"
]

light_positions = []

# Rectangle drawing function


def rectangle(x, y, width, height, color):
    t.penup()
    t.goto(x, y)
    t.pendown()
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()
    t.penup()

# Polygon drawing function


def polygon(points, color):
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.color(color)
    t.begin_fill()

    for point in points[1:]:
        t.goto(point)

    t.goto(points[0])
    t.end_fill()
    t.penup()

# Text function


def write_text(x, y, message, size, color):
    t.penup()
    t.goto(x, y)
    t.color(color)
    t.write(
        message,
        align="center",
        font=("Arial", size, "bold")
    )


# Night sky stars
for _ in range(80):
    x = random.randint(-430, 430)
    y = random.randint(100, 330)

    t.penup()
    t.goto(x, y)
    t.dot(random.randint(2, 5), "white")

# Moon
t.penup()
t.goto(320, 240)
t.dot(75, "#fff2b2")

t.goto(340, 255)
t.dot(65, "#10152f")

# Ground
rectangle(-450, -300, 900, 100, "#244b38")

# House body
rectangle(-180, -200, 360, 250, "#f2b66d")

# Roof
polygon(
    [(-220, 50), (0, 210), (220, 50)],
    "#a83e32"
)

# Roof edges
t.penup()
t.goto(-220, 50)
t.pendown()
t.color("#ffcc66")
t.pensize(5)
t.goto(0, 210)
t.goto(220, 50)
t.pensize(3)
t.penup()

# Roof tile decorations
for x in range(-150, 180, 50):
    t.penup()
    t.goto(x, 80)
    t.pendown()
    t.color("#d96845")
    t.goto(x + 30, 105)
    t.penup()

# Door
rectangle(-35, -200, 70, 115, "#663522")

t.penup()
t.goto(20, -145)
t.dot(8, "#ffd166")

# Windows
for x in [-135, 75]:
    rectangle(x, -75, 60, 65, "#6ed9ff")

    t.color("#fff0bb")
    t.pensize(4)

    t.penup()
    t.goto(x + 30, -75)
    t.pendown()
    t.goto(x + 30, -10)

    t.penup()
    t.goto(x, -43)
    t.pendown()
    t.goto(x + 60, -43)
    t.penup()

# Roof light wire
t.color("#343434")
t.pensize(2)

t.penup()
t.goto(-205, 60)
t.pendown()
t.goto(0, 195)
t.goto(205, 60)
t.penup()

# Left and right roof lights
for i in range(15):
    fraction = i / 14

    x = -205 + 205 * fraction
    y = 60 + 135 * fraction
    light_positions.append((x, y, 15))

    x = 205 - 205 * fraction
    y = 60 + 135 * fraction
    light_positions.append((x, y, 15))

# Front light wire
t.penup()
t.goto(-170, 35)
t.pendown()
t.goto(170, 35)
t.penup()

# Front lights
for x in range(-165, 171, 25):
    light_positions.append((x, 35, 14))

# Decorative garland
for x in range(-40, 41, 15):
    t.penup()
    t.goto(x, -65)
    t.dot(10, random.choice(
        ["#ff4d6d", "#ffd93d", "#ff8c42"]
    ))

# Diya drawing


def diya(x, y):
    # Glow
    t.penup()
    t.goto(x, y + 25)
    t.dot(35, "#5c3925")

    t.goto(x, y + 22)
    t.dot(20, "#ff9f1c")

    t.goto(x, y + 24)
    t.dot(10, "#fff3a3")

    # Clay lamp
    polygon(
        [
            (x - 18, y),
            (x - 12, y - 10),
            (x + 12, y - 10),
            (x + 18, y)
        ],
        "#c65d35"
    )

    t.penup()
    t.goto(x - 18, y)
    t.pendown()
    t.color("#ffca75")
    t.goto(x + 18, y)
    t.penup()


# Three diyas
diya(-120, -240)
diya(0, -240)
diya(120, -240)

# Rangoli
rangoli_colors = [
    "#ff4d6d", "#ffd93d",
    "#53e0bc", "#a78bfa",
    "#ff8c42"
]

for i, color in enumerate(rangoli_colors):
    t.penup()
    t.goto(0, -275)
    t.dot(48 - i * 5, color)

t.penup()
t.goto(0, -275)
t.dot(12, "#ffffff")

# Greeting
write_text(0, 285, "HAPPY TIHAR!", 27, "#ffd93d")
write_text(
    0, 250,
    "May your home shine with happiness",
    13, "white"
)

# Twinkling animation


def twinkle():
    for x, y, size in light_positions:
        t.penup()
        t.goto(x, y)

        # Randomly change the light color
        color = random.choice(light_colors)

        # Draw a soft glow
        t.dot(size + 10, "#343044")

        # Draw the bright bulb
        t.dot(size, color)

    screen.update()

    # Repeat every 300 milliseconds
    screen.ontimer(twinkle, 300)


# Start animation
twinkle()

turtle.done()
