
import turtle
import random
import math
import time

# MAGICAL WIZARD'S LIBRARY

screen = turtle.Screen()
screen.setup(1100, 800)
screen.bgcolor("#100d25")
screen.title("The Magical Wizard's Library")
screen.tracer(0)

pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)

# Drawing helpers

def rectangle(x, y, width, height, color, outline=None):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()
    pen.fillcolor(color)
    pen.pencolor(outline if outline else color)
    pen.begin_fill()

    for _ in range(2):
        pen.forward(width)
        pen.left(90)
        pen.forward(height)
        pen.left(90)

    pen.end_fill()


def circle(x, y, radius, color, outline=None):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.fillcolor(color)
    pen.pencolor(outline if outline else color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()


def line(x1, y1, x2, y2, color, width=2):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.pencolor(color)
    pen.pensize(width)
    pen.goto(x2, y2)
    pen.pensize(1)


def text(x, y, message, color, size=12):
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    pen.write(message, align="center",
              font=("Georgia", size, "bold"))


# Background and floor

rectangle(-550, -400, 1100, 800, "#100d25")

rectangle(-550, -400, 1100, 190, "#21152d")
rectangle(-550, -210, 1100, 12, "#65452f")

# Floor tiles
for x in range(-500, 550, 100):
    line(x, -400, x, -210, "#39233c", 2)

for y in [-260, -320, -380]:
    line(-550, y, 550, y, "#39233c", 2)

# Magical starry window

rectangle(-110, 70, 220, 250, "#543d62", "#b98a51")
rectangle(-100, 80, 200, 230, "#101c42", "#d9b46b")

# Window frame
line(0, 80, 0, 330, "#d9b46b", 6)
line(-100, 205, 100, 205, "#d9b46b", 6)

# Moon
circle(55, 275, 27, "#f7e9ad")
circle(68, 286, 25, "#101c42")

# Stars outside window
for _ in range(35):
    x = random.randint(-90, 90)
    y = random.randint(95, 320)
    circle(x, y, random.choice([1, 2, 3]), "#fff2b5")

text(0, 335, "THE NIGHT SKY", "#e7c87e", 11)

# Huge wooden bookshelves


def bookshelf(x, y, width, height):
    rectangle(x, y, width, height, "#53301f", "#bd8750")

    # Shelves
    shelf_height = height // 4

    for i in range(1, 4):
        sy = y + i * shelf_height
        rectangle(x, sy, width, 10, "#a16a3b")

    colors = [
        "#9d354b", "#245d78", "#b38b39",
        "#4c376e", "#27664c", "#a45b2c",
        "#7b315a", "#315c9d"
    ]

    # Books
    for shelf in range(4):
        book_x = x + 8
        book_y = y + shelf * shelf_height + 12

        while book_x < x + width - 15:
            book_width = random.randint(12, 22)
            book_height = random.randint(
                shelf_height - 28, shelf_height - 12
            )

            rectangle(
                book_x, book_y, book_width,
                book_height, random.choice(colors), "#d7ae68"
            )

            # Book decoration
            line(
                book_x + 3, book_y + 8,
                book_x + book_width - 3, book_y + 8,
                "#e4c47e", 1
            )

            book_x += book_width + 3


# Left and right bookshelves
bookshelf(-520, -190, 330, 520)
bookshelf(190, -190, 330, 520)

# Shelf labels
text(-355, 340, "ANCIENT SPELLS", "#f5d68d", 13)
text(355, 340, "FORBIDDEN MAGIC", "#f5d68d", 13)

# Wizard's desk

rectangle(-175, -160, 350, 25, "#633d27", "#d3a05b")
rectangle(-155, -160, 18, 90, "#4a2b20")
rectangle(137, -160, 18, 90, "#4a2b20")

# Desk decorations
rectangle(-105, -130, 70, 12, "#9c6a37")
rectangle(-95, -118, 50, 5, "#d9b46b")

# Open book
rectangle(-35, -135, 45, 8, "#e8d8aa", "#a88a54")
rectangle(10, -135, 45, 8, "#e8d8aa", "#a88a54")

line(10, -135, 10, -127, "#7a583c", 2)

# Magical potion bottles


def potion(x, y, color):
    # Bottle body
    circle(x, y + 15, 20, color, "#e6c778")
    rectangle(x - 20, y + 15, 40, 25, color, "#e6c778")

    # Neck and cork
    rectangle(x - 9, y + 40, 18, 15, "#9c8054")
    rectangle(x - 11, y + 55, 22, 9, "#68452e")

    # Bottle shine
    line(x - 10, y + 25, x - 10, y + 35, "#fff1bd", 2)


potion(-135, -90, "#4aabce")
potion(95, -90, "#a04fbc")
potion(150, -90, "#3aaf75")

# Potion labels
text(-135, -153, "MANA", "#a8e9ff", 8)
text(95, -153, "VOID", "#e4a9ff", 8)
text(150, -153, "LIFE", "#a9ffc5", 8)

# Candles


def candle(x, y):
    rectangle(x - 7, y, 14, 35, "#e7d5a2")

    # Flame
    circle(x, y + 43, 7, "#ffad33")
    circle(x, y + 45, 3, "#fff3a1")


candle(-170, -115)
candle(175, -115)

# Magic circle on floor


def magic_circle(cx, cy, radius):
    pen.penup()
    pen.goto(cx, cy - radius)
    pen.pendown()
    pen.pencolor("#a75bdb")
    pen.pensize(3)
    pen.circle(radius)

    pen.penup()
    pen.goto(cx, cy - radius * 0.75)
    pen.pendown()
    pen.circle(radius * 0.75)

    # Magic symbols and lines
    for angle in range(0, 360, 60):
        rad = math.radians(angle)

        x1 = cx + radius * math.cos(rad)
        y1 = cy + radius * math.sin(rad)

        x2 = cx + radius * 0.75 * math.cos(rad)
        y2 = cy + radius * 0.75 * math.sin(rad)

        line(x1, y1, x2, y2, "#d19aff", 2)

    # Inner pentagram
    points = []

    for i in range(5):
        angle = math.radians(90 + i * 72)
        points.append((
            cx + radius * 0.48 * math.cos(angle),
            cy + radius * 0.48 * math.sin(angle)
        ))

    for i in range(5):
        p1 = points[i]
        p2 = points[(i + 2) % 5]
        line(p1[0], p1[1], p2[0], p2[1], "#d19aff", 2)

    pen.pensize(1)


magic_circle(0, -300, 85)

# Floating animated spell books

books = []

for i in range(4):
    book = turtle.Turtle()
    book.shape("square")
    book.shapesize(stretch_wid=0.9, stretch_len=1.5)
    book.color(random.choice([
        "#c94d79", "#4b83c7", "#d5a43a", "#8555b8"
    ]))
    book.penup()

    book.goto(
        random.randint(-80, 80),
        random.randint(-30, 120)
    )

    books.append({
        "turtle": book,
        "base_y": book.ycor(),
        "phase": random.uniform(0, 6.28)
    })

# Floating magical particles

particles = []

for _ in range(45):
    particle = turtle.Turtle()
    particle.hideturtle()
    particle.penup()
    particle.speed(0)

    x = random.randint(-500, 500)
    y = random.randint(-200, 350)

    particle.goto(x, y)
    particle.color(random.choice([
        "#d9a7ff", "#fff2a6",
        "#8de8ff", "#ffb9e7"
    ]))

    particles.append({
        "turtle": particle,
        "x": x,
        "y": y,
        "speed": random.uniform(0.5, 1.8),
        "size": random.choice([2, 3, 4])
    })

# Animation

frame = 0


def animate():
    global frame

    frame += 1

    # Floating books
    for book_data in books:
        book = book_data["turtle"]

        y = (
            book_data["base_y"]
            + math.sin(frame * 0.04 + book_data["phase"]) * 15
        )

        book.goto(book.xcor(), y)
        book.left(1.5)

    # Floating particles
    for particle_data in particles:
        particle = particle_data["turtle"]

        particle_data["y"] += particle_data["speed"]

        if particle_data["y"] > 380:
            particle_data["y"] = -200
            particle_data["x"] = random.randint(-500, 500)

        particle.goto(
            particle_data["x"],
            particle_data["y"]
        )

        particle.dot(particle_data["size"])

    screen.update()
    screen.ontimer(animate, 30)



animate()

screen.mainloop()
