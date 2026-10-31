
import turtle
import random
import math


# SCREEN SETUP


screen = turtle.Screen()
screen.setup(1000, 750)

screen.bgcolor("#10182C")
screen.tracer(0)


# TURTLE HELPER



def create_pen():
    pen = turtle.Turtle()
    pen.hideturtle()
    pen.speed(0)
    pen.penup()
    return pen



# BACKGROUND STARS


stars = create_pen()

for _ in range(100):
    x = random.randint(-480, 480)
    y = random.randint(80, 350)

    stars.goto(x, y)
    stars.dot(random.randint(2, 4), "#FFF4D6")


# Moon
moon = create_pen()
moon.goto(350, 260)
moon.dot(85, "#FFF1C1")
moon.goto(375, 275)
moon.dot(75, "#10182C")



# GROUND


ground = create_pen()
ground.goto(-500, -180)
ground.color("#243D38")
ground.begin_fill()

for point in [(-500, -180), (-500, -350),
              (500, -350), (500, -180)]:
    ground.goto(point)

ground.end_fill()



# CHERRY BLOSSOM TREE


tree = create_pen()
tree.pensize(15)
tree.pencolor("#70452F")

tree.goto(-180, -180)
tree.setheading(90)
tree.pendown()
tree.forward(230)

# Main branches
tree.pensize(9)

branches = [
    (-180, 20, 145, 100),
    (-180, 30, 35, 120),
    (-180, 0, 170, 65),
    (-180, 60, 15, 75),
    (-180, 40, 95, 110)
]

for x, y, angle, distance in branches:
    tree.penup()
    tree.goto(x, y)
    tree.setheading(angle)
    tree.pendown()
    tree.forward(distance)

tree.penup()



# BLOSSOM CLUSTERS


blossoms = create_pen()

clusters = [
    (-320, 90, 70),
    (-240, 150, 75),
    (-120, 130, 80),
    (-40, 180, 65),
    (-280, 10, 55),
    (-110, 35, 65),
    (-180, 220, 50)
]

pink_colors = [
    "#FFB7D5",
    "#FFC9E2",
    "#F78FB3",
    "#FFDCEC",
    "#EFA4C8"
]

for cx, cy, radius in clusters:
    for _ in range(65):
        angle = random.uniform(0, 2 * math.pi)
        distance = random.uniform(0, radius)

        x = cx + math.cos(angle) * distance
        y = cy + math.sin(angle) * distance

        blossoms.goto(x, y)
        blossoms.dot(random.randint(5, 11),
                     random.choice(pink_colors))



# POND


pond = create_pen()
pond.goto(80, -290)
pond.color("#173E59")
pond.begin_fill()
pond.pendown()
pond.setheading(0)
pond.circle(170, 360)
pond.end_fill()
pond.penup()

# Water reflections
water = create_pen()

for _ in range(35):
    x = random.randint(-40, 380)
    y = random.randint(-310, -180)

    water.goto(x, y)
    water.pensize(random.randint(1, 3))
    water.pencolor("#65A9C4")
    water.pendown()
    water.forward(random.randint(5, 25))
    water.penup()



# JAPANESE LANTERNS


def draw_lantern(x, y):

    lamp = create_pen()

    # Hanging string
    lamp.goto(x, y + 45)
    lamp.pencolor("#D7B58A")
    lamp.pendown()
    lamp.goto(x, y + 20)
    lamp.penup()

    # Lantern body
    lamp.goto(x - 17, y - 10)
    lamp.color("#E65B68")
    lamp.begin_fill()

    for _ in range(2):
        lamp.forward(34)
        lamp.right(90)
        lamp.forward(50)
        lamp.right(90)

    lamp.end_fill()

    # Lantern glow
    lamp.goto(x, y - 35)
    lamp.dot(10, "#FFE9A8")

    # Top and bottom
    lamp.goto(x - 21, y - 10)
    lamp.color("#D5A45C")
    lamp.pendown()
    lamp.forward(42)

    lamp.penup()
    lamp.goto(x - 21, y - 60)
    lamp.pendown()
    lamp.forward(42)


draw_lantern(-420, 50)
draw_lantern(430, 70)



# FALLING PETALS


class Petal:

    def __init__(self):
        self.x = random.randint(-400, 400)
        self.y = random.randint(-100, 350)
        self.speed = random.uniform(1, 3)
        self.drift = random.uniform(-1, 1)
        self.size = random.randint(5, 10)
        self.color = random.choice(pink_colors)

        self.pen = create_pen()

    def update(self):

        self.y -= self.speed
        self.x += self.drift

        if self.y < -340:
            self.y = 350
            self.x = random.randint(-450, 450)

        if self.x > 490:
            self.x = -490
        elif self.x < -490:
            self.x = 490

        self.pen.clear()
        self.pen.goto(self.x, self.y)
        self.pen.dot(self.size, self.color)


petals = [Petal() for _ in range(35)]
# ANIMATION


paused = False


def toggle_animation():
    global paused
    paused = not paused


def animate():

    if not paused:
        for petal in petals:
            petal.update()

    screen.update()
    screen.ontimer(animate, 30)


screen.listen()
screen.onkey(toggle_animation, "space")

animate()
screen.mainloop()
