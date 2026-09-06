import math
import turtle

# Setup screen 
screen = turtle.Screen()
screen.setup(width=650, height=800)
screen.title("National Flag of Nepal")
screen.bgcolor("white")

t = turtle.Turtle()
t.speed(0)
t.hideturtle()

CRIMSON = "#DC143C"
BLUE = "#003893"
WHITE = "#FFFFFF"


def draw_polygon(points, fill_color):
    t.penup()
    t.goto(points[0])
    t.pendown()
    t.color(fill_color, fill_color)
    t.begin_fill()
    for pt in points[1:]:
        t.goto(pt)
    t.goto(points[0])
    t.end_fill()
    t.penup()


# Outer Blue Frame
blue_frame = [
    (-130, -250),
    (130, -250),
    (-30, -80),
    (130, -80),
    (-130, 190),
]
draw_polygon(blue_frame, BLUE)

# Inner Crimson triangle
crimson_body = [
    (-110, -230),
    (90, -230),
    (-45, -80),
    (90, -80),
    (-110, 160),
]
draw_polygon(crimson_body, CRIMSON)


def draw_sun(cx, cy, radius, rays, color):
    # Calculating all vertices first
    points = []
    for i in range(rays * 2):
        r = radius if i % 2 == 0 else radius * 0.50
        angle = math.radians(i * (360 / (rays * 2)))
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))

    # Move to starting point FIRST before beginning fill
    t.penup()
    t.goto(points[0])
    t.pendown()

    t.color(color, color)
    t.begin_fill()
    for pt in points[1:]:
        t.goto(pt)
    t.goto(points[0])
    t.end_fill()
    t.penup()



draw_sun(-45, -155, 26, 12, WHITE)

# Upper Crescent Moon and Inner Sun
# Outer White Moon Circle
t.penup()
t.goto(-45, 15)

t.pendown()
t.color(WHITE, WHITE)
t.begin_fill()
t.circle(20)
t.end_fill()
t.penup()

# Crimson 
t.goto(-45, 23)
t.pendown()
t.color(CRIMSON, CRIMSON)
t.begin_fill()
t.circle(18)
t.end_fill()
t.penup()

# Sun inside Crescent
draw_sun(-45, 20, 10, 12, WHITE)

turtle.done()