
import math
import random
import turtle

# Screen setup
screen = turtle.Screen()
screen.setup(900, 650)
screen.bgcolor("black")
screen.title("Diwali Fireworks Show")
screen.tracer(0)

# Colors
colors = [
    "red", "orange", "yellow", "cyan",
    "magenta", "lime", "white", "deep pink",
    "gold", "deepskyblue"
]

# One drawing turtle for all fireworks
pen = turtle.Turtle()
pen.hideturtle()
pen.speed(0)
pen.penup()

rockets = []
sparks = []


def launch_rocket():
    x = random.randint(-420, 420)

    rockets.append({
        "x": x,
        "y": -320,
        "speed": random.uniform(3, 7),
        "target": random.randint(-50, 230),
        "color": random.choice(colors)
    })


def explode(rocket):
    # Create many particles moving in all directions
    for _ in range(65):
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 5)

        sparks.append({
            "x": rocket["x"],
            "y": rocket["y"],
            "dx": math.cos(angle) * speed,
            "dy": math.sin(angle) * speed,
            "color": random.choice(colors),
            "life": random.randint(25, 45)
        })


frame = 0


def animate():
    global frame

    pen.clear()

    # Launch new rockets at different intervals
    if frame % 9 == 0:
        launch_rocket()

    #  move rockets
    for rocket in rockets[:]:
        rocket["y"] += rocket["speed"]

        #  glowing rocket trail
        pen.goto(rocket["x"], rocket["y"])
        pen.dot(8, rocket["color"])

        pen.goto(
            rocket["x"] - random.uniform(-2, 2),
            rocket["y"] - 15
        )
        pen.dot(3, "white")

        # Explode when the rocket reaches its target
        if rocket["y"] >= rocket["target"]:
            explode(rocket)
            rockets.remove(rocket)

    # Update all explosions simultaneously
    for spark in sparks[:]:
        spark["x"] += spark["dx"]
        spark["y"] += spark["dy"]

        # Gravity pulls sparks down
        spark["dy"] -= 0.08
        spark["life"] -= 1

        pen.goto(spark["x"], spark["y"])

        # Fade effect simulated by shrinking particles
        size = max(1, min(5, spark["life"] // 7))
        pen.dot(size, spark["color"])

        if spark["life"] <= 0:
            sparks.remove(spark)

    screen.update()
    frame += 1

    #  next animation frame
    screen.ontimer(animate, 25)


animate()
turtle.done()
