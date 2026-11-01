
import math
import random
import turtle

# SCREEN
screen = turtle.Screen()
screen.setup(1000, 750)
screen.bgcolor("#101020")
screen.title("The Haunted Mansion")
screen.tracer(0)


def pen():
    t = turtle.Turtle()
    t.hideturtle()
    t.speed(0)
    t.penup()
    return t

# DRAW RECTANGLE


def rectangle(t, x, y, width, height, color):
    t.goto(x, y)
    t.color(color)
    t.begin_fill()
    for _ in range(2):
        t.forward(width)
        t.left(90)
        t.forward(height)
        t.left(90)
    t.end_fill()


# STARS
stars = pen()

for _ in range(100):
    stars.goto(random.randint(-480, 480),
               random.randint(100, 350))
    stars.dot(random.randint(2, 4), "white")

# MOON
moon = pen()
moon.goto(330, 230)
moon.dot(110, "#FFF0B5")
moon.goto(355, 250)
moon.dot(100, "#101020")

# GROUND
ground = pen()
rectangle(ground, -500, -350, 1000, 200, "#20232D")

# MAIN HOUSE
house = pen()
rectangle(house, -180, -150, 360, 300, "#393343")

# SECOND FLOOR
rectangle(house, -110, 30, 220, 150, "#4B4054")

# ROOF
roof = pen()
roof.color("#17131F")
roof.goto(-220, 150)
roof.begin_fill()
roof.goto(0, 310)
roof.goto(220, 150)
roof.goto(-220, 150)
roof.end_fill()

# DOOR
door = pen()
rectangle(door, -35, -150, 70, 120, "#211723")
door.goto(20, -90)
door.dot(7, "#FFD66B")

# WINDOWS
windows = []

for x, y in [
    (-140, -30), (90, -30),
    (-75, 75), (45, 75)
]:
    w = pen()
    windows.append((w, x, y))

# GRAVEYARD
graveyard = pen()

for x in range(-450, 451, 90):
    y = random.randint(-280, -240)
    graveyard.color("#777783")
    graveyard.pensize(5)
    graveyard.goto(x, y)
    graveyard.pendown()
    graveyard.goto(x, y + 40)
    graveyard.penup()
    graveyard.goto(x - 12, y + 25)
    graveyard.pendown()
    graveyard.goto(x + 12, y + 25)
    graveyard.penup()

# GHOST
ghost = pen()
ghost_x = 0
ghost_y = -10
ghost_direction = 1


def draw_ghost():
    ghost.clear()
    ghost.goto(ghost_x, ghost_y)
    ghost.color("white")
    ghost.dot(45)

    ghost.goto(ghost_x - 12, ghost_y + 5)
    ghost.dot(6, "black")

    ghost.goto(ghost_x + 12, ghost_y + 5)
    ghost.dot(6, "black")

    ghost.goto(ghost_x, ghost_y - 8)
    ghost.dot(7, "black")

    # Ghost tail
    ghost.goto(ghost_x - 15, ghost_y - 15)
    ghost.color("white")
    ghost.begin_fill()
    for point in [
        (ghost_x - 15, ghost_y - 30),
        (ghost_x - 7, ghost_y - 23),
        (ghost_x, ghost_y - 32),
        (ghost_x + 8, ghost_y - 23),
        (ghost_x + 15, ghost_y - 30),
        (ghost_x + 15, ghost_y - 15)
    ]:
        ghost.goto(point)
    ghost.goto(ghost_x - 15, ghost_y - 15)
    ghost.end_fill()


# BATS
bats = []

for _ in range(5):
    b = pen()
    bats.append([
        b,
        random.randint(-400, 400),
        random.randint(100, 300),
        random.uniform(1, 3)
    ])


def draw_bat(b, x, y):
    b.clear()
    b.color("#05050A")
    b.goto(x, y)
    b.dot(10)
    b.goto(x - 5, y)
    b.setheading(150)
    b.pendown()
    b.circle(12, 90)
    b.penup()
    b.goto(x + 5, y)
    b.setheading(30)
    b.pendown()
    b.circle(-12, 90)
    b.penup()


# LIGHTNING
lightning = pen()
lightning_on = False


def flash_lightning():
    global lightning_on
    lightning_on = not lightning_on
    lightning.clear()

    if lightning_on:
        lightning.color("#D9E8FF")
        lightning.pensize(5)
        lightning.goto(250, 300)
        lightning.pendown()
        lightning.goto(220, 220)
        lightning.goto(245, 220)
        lightning.goto(180, 100)
        lightning.penup()


# ANIMATION
paused = False
frame = 0


def toggle_pause():
    global paused
    paused = not paused


def move_ghost_left():
    global ghost_x
    ghost_x -= 15


def move_ghost_right():
    global ghost_x
    ghost_x += 15


def animate():
    global ghost_x, ghost_y, ghost_direction, frame

    if not paused:
        frame += 1

        ghost_x += ghost_direction * 2
        ghost_y += math.sin(frame / 10) * 0.5

        if ghost_x > 430 or ghost_x < -430:
            ghost_direction *= -1

        draw_ghost()

        for b, x, y, speed in bats:
            x -= speed
            if x < -480:
                x = 480
                y = random.randint(100, 300)
            draw_bat(b, x, y)
            b_index = bats.index(
                [b, bats[bats.index([b, x + speed, y, speed])][1], y, speed]) if False else None
            bats[bats.index(
                next(item for item in bats if item[0] == b))][1] = x

        # Random glowing windows
        for w, x, y in windows:
            w.clear()
            rectangle(w, x, y, 40, 50,
                      random.choice(["#FFD45A", "#40364C", "#F5A623"]))

        if frame % 120 == 0:
            flash_lightning()

    screen.update()
    screen.ontimer(animate, 30)


screen.listen()
screen.onkey(toggle_pause, "space")
screen.onkey(move_ghost_left, "Left")
screen.onkey(move_ghost_right, "Right")

animate()
screen.mainloop()
