
import math
import random
import turtle

# 1. SCREEN SETUP

screen = turtle.Screen()
screen.setup(1400, 900)
screen.title(" Astronomy Observation")
screen.bgcolor("#030817")
screen.tracer(0)

pen = turtle.Turtle()
pen.speed(0)
pen.hideturtle()

random.seed(25)

# 2. BASIC DRAWING FUNCTIONS


def jump(x, y):
    pen.penup()
    pen.goto(x, y)
    pen.pendown()


def dot(x, y, size, color):
    pen.penup()
    pen.goto(x, y)
    pen.dot(size, color)


def circle(x, y, radius, color):
    pen.penup()
    pen.goto(x, y - radius)
    pen.pendown()
    pen.color(color)
    pen.begin_fill()
    pen.circle(radius)
    pen.end_fill()


def line(x1, y1, x2, y2, color, width=1):
    pen.penup()
    pen.goto(x1, y1)
    pen.pendown()
    pen.pensize(width)
    pen.pencolor(color)
    pen.goto(x2, y2)
    pen.pensize(1)


def polygon(points, color, outline=None):
    pen.penup()
    pen.goto(points[0])
    pen.pendown()
    pen.color(outline or color, color)
    pen.begin_fill()

    for point in points[1:]:
        pen.goto(point)

    pen.goto(points[0])
    pen.end_fill()


def label(x, y, message, color="#B9DFFF", size=10):
    pen.penup()
    pen.goto(x, y)
    pen.color(color)
    pen.write(message, font=("Arial", size, "bold"))


def ellipse(cx, cy, rx, ry, color, rotation=0):
    points = []
    angle = math.radians(rotation)

    for i in range(101):
        t = 2 * math.pi * i / 100
        x = rx * math.cos(t)
        y = ry * math.sin(t)

        px = cx + x * math.cos(angle) - y * math.sin(angle)
        py = cy + x * math.sin(angle) + y * math.cos(angle)

        points.append((px, py))

    polygon(points, color)

# 3. DEEP SPACE BACKGROUND


# Random distant stars
for i in range(650):
    x = random.randint(-690, 690)
    y = random.randint(-160, 440)

    size = random.choice([1, 1, 2, 2, 3])

    color = random.choice([
        "#FFFFFF", "#A8D8FF",
        "#758FFF", "#C9B5FF",
        "#FFDFA8"
    ])

    dot(x, y, size, color)

# Bright glowing stars
for x, y in [
    (-600, 350), (-400, 240), (-200, 380),
    (20, 350), (250, 400), (500, 300),
    (620, 180), (-550, 50), (400, 50),
    (150, 100), (-100, 100), (570, -20)
]:
    dot(x, y, 9, "#244C85")
    dot(x, y, 5, "#B9DDFF")
    dot(x, y, 2, "white")

# 4. MILKY WAY GALAXY

# Soft galaxy clouds
ellipse(80, 220, 270, 105, "#17133F", -28)
ellipse(80, 220, 220, 75, "#29205F", -28)
ellipse(80, 220, 165, 50, "#44317E", -28)
ellipse(80, 220, 100, 30, "#79529B", -28)
ellipse(80, 220, 48, 18, "#E8B5C7", -28)

# Spiral arms
for arm in range(4):
    offset = arm * math.pi / 2

    for i in range(260):
        t = i / 260 * 4.8
        radius = 12 + t * 36

        angle = t + offset

        x = 80 + radius * math.cos(angle)
        y = 220 + radius * 0.48 * math.sin(angle)

        if random.random() > 0.25:
            color = random.choice([
                "#8D75D6", "#6B9DEB",
                "#D49ACF", "#B8C8FF",
                "#F1C5D9"
            ])

            dot(x, y, random.choice([2, 3, 4]), color)

# Galaxy core
for r, c in [
    (34, "#8D6CBA"),
    (25, "#B88ACB"),
    (16, "#E2B5CB"),
    (8, "#FFF0D4")
]:
    dot(80, 220, r, c)

label(0, 370, "THE MILKY WAY", "#D5B7FF", 15)
label(0, 347, "SPIRAL GALAXY", "#A8B6E8", 9)

# 5. PLANET DRAWING FUNCTIONS


def draw_planet(x, y, r, base, highlight):
    # Planet shadow
    circle(x + 4, y - 4, r, "#080D25")

    # Main surface
    circle(x, y, r, base)

    # Highlight
    circle(x - r * 0.32, y + r * 0.25,
           r * 0.35, highlight)

    # Dark atmospheric edge
    ellipse(x + r * 0.35, y, r * 0.45,
            r * 0.9, "#10182D")


def draw_saturn(x, y, r):
    # Back ring
    ellipse(x, y, r * 2.0, r * 0.48,
            "#78644E", -18)

    ellipse(x, y, r * 1.8, r * 0.34,
            "#C5A77E", -18)

    # Planet
    circle(x, y, r, "#D8AA65")

    # Surface bands
    for i, color in enumerate([
        "#B67B46", "#EAC58C",
        "#C08B53", "#F0D09A",
        "#A97043"
    ]):
        yy = y - r * 0.65 + i * r * 0.3
        ellipse(x, yy, r * 0.82, r * 0.10,
                color)

    # Front ring
    ellipse(x, y, r * 2.0, r * 0.48,
            "#D9BC8E", -18)

    ellipse(x, y, r * 1.45, r * 0.24,
            "#8D715B", -18)

    # Planet center again
    circle(x, y, r * 0.88, "#D5A568")

    # Ring detail
    ellipse(x, y, r * 1.9, r * 0.40,
            "#B89A75", -18)

    # Restore visible planet
    circle(x, y, r * 0.86, "#D9AF76")

    for i, color in enumerate([
        "#C18A50", "#E8C18A", "#BD8249"
    ]):
        yy = y - r * 0.4 + i * r * 0.4
        ellipse(x, yy, r * 0.7, r * 0.07, color)

# 6. SATURN


draw_saturn(-450, 270, 48)

label(-500, 340, "SATURN", "#FFE0A8", 13)
label(-500, 321, "RINGED PLANET", "#B5C5E8", 8)

# 7. EARTH AND MOON

# Earth
draw_planet(-560, 65, 47, "#1763B2", "#63B8F0")

# Continents
polygon([
    (-586, 88), (-578, 105), (-560, 101),
    (-551, 89), (-557, 77), (-575, 72),
    (-580, 58), (-590, 66)
], "#3DAD72")

polygon([
    (-546, 46), (-533, 59), (-525, 47),
    (-530, 28), (-540, 20), (-550, 34)
], "#5DBD76")

# Earth clouds
ellipse(-563, 83, 27, 5, "#C9E9F9", -20)
ellipse(-552, 40, 18, 4, "#E0F2FF", 30)

# Earth atmosphere
ellipse(-560, 65, 52, 49, "#2866C8")

label(-620, 130, "EARTH", "#8ED9FF", 12)

# Moon
circle(-440, 30, 23, "#B9BCCB")
circle(-446, 37, 7, "#777F91")
circle(-431, 24, 5, "#7E8295")
circle(-448, 15, 4, "#8C91A3")
circle(-436, 45, 3, "#E0E2EB")

label(-462, -8, "MOON", "#D7DDF4", 10)

# 8. OTHER PLANETS

# Jupiter
draw_planet(-280, 55, 34, "#BD8759", "#F1D0A0")

for yy in [40, 52, 66]:
    ellipse(-280, yy, 28, 3, "#E9BD8B")

circle(-270, 47, 4, "#B45A43")

label(-310, 5, "JUPITER", "#FFD4A0", 10)

# Mars
draw_planet(350, 290, 27, "#C84C36", "#FF9667")
dot(340, 302, 5, "#A93630")
label(326, 250, "MARS", "#FFAA91", 10)

# Neptune
draw_planet(530, 130, 28, "#176AC5", "#65C5FF")
label(510, 88, "NEPTUNE", "#82CAFF", 10)

# Uranus
draw_planet(440, -20, 22, "#48BFC4", "#A2F3E8")
label(414, -57, "URANUS", "#8FE9E8", 9)

# Venus
draw_planet(320, -65, 24, "#D69B44", "#FFE2A0")
label(295, -103, "VENUS", "#FFD38A", 9)

# Mercury
draw_planet(550, -110, 15, "#99949B", "#E4D9D2")
label(527, -141, "MERCURY", "#D7D5E3", 8)

# 9. CONSTELLATIONS


def constellation(name, points, x, y):
    # Connect the stars
    for i in range(len(points) - 1):
        line(
            points[i][0], points[i][1],
            points[i + 1][0], points[i + 1][1],
            "#426CA9", 1
        )

    # Draw constellation stars
    for px, py in points:
        dot(px, py, 11, "#244D8D")
        dot(px, py, 5, "#A9DFFF")
        dot(px, py, 2, "white")

    label(x, y, name, "#9DD8FF", 10)


# Orion
constellation("ORION", [
    (-150, 110), (-125, 150), (-100, 110),
    (-80, 75), (-105, 35), (-145, 45),
    (-170, 80)
], -165, 170)

# Big Dipper
constellation("BIG DIPPER", [
    (470, 340), (510, 355), (550, 330),
    (585, 295), (615, 320), (645, 300),
    (660, 260)
], 550, 375)

# Cassiopeia
constellation("CASSIOPEIA", [
    (250, 40), (280, 75), (310, 45),
    (340, 80), (375, 45)
], 265, 100)

# 10. SHOOTING STARS


def shooting_star(x, y, length, angle):
    rad = math.radians(angle)

    dx = length * math.cos(rad)
    dy = length * math.sin(rad)

    # Glowing trail
    line(x, y, x + dx, y + dy, "#493B92", 5)
    line(x, y, x + dx, y + dy, "#92BFFF", 2)

    # Bright head
    dot(x, y, 9, "#A8DFFF")
    dot(x, y, 4, "white")


shooting_star(-350, 180, 75, -35)
shooting_star(190, 350, 65, -30)
shooting_star(450, 210, 85, -40)
shooting_star(-70, 300, 55, -25)
shooting_star(150, -30, 55, -35)

# 11. MOUNTAIN BACKGROUND

# Distant mountains
polygon([
    (-700, -200), (-600, -110), (-520, -190),
    (-400, -90), (-300, -190), (-180, -95),
    (-70, -190), (50, -105), (180, -200),
    (300, -100), (430, -200), (550, -115),
    (700, -200), (700, -450), (-700, -450)
], "#182B4D")

# Snow peaks
polygon([
    (-600, -110), (-550, -155), (-520, -125),
    (-500, -165), (-520, -190), (-400, -90),
    (-350, -145), (-300, -190), (-180, -95),
    (-120, -150), (-70, -190), (50, -105),
    (100, -155), (180, -200)
], "#8299B9")

# Foreground mountain range
polygon([
    (-700, -250), (-600, -190), (-520, -260),
    (-430, -205), (-330, -285), (-200, -205),
    (-90, -290), (30, -205), (150, -280),
    (280, -200), (400, -270), (520, -205),
    (700, -270), (700, -450), (-700, -450)
], "#09182E")

# Mountain snow highlights
polygon([
    (-600, -190), (-570, -215), (-540, -210),
    (-520, -260), (-560, -230)
], "#A6C7E7")

polygon([
    (-200, -205), (-165, -235), (-130, -230),
    (-90, -290), (-150, -245)
], "#A5B9D5")

polygon([
    (280, -200), (310, -235), (345, -230),
    (400, -270), (345, -245)
], "#A5BCD9")

# 12. OBSERVATORY BUILDING

# Building foundation
polygon([
    (-650, -430), (-650, -350),
    (-230, -350), (-230, -430)
], "#253A59", "#536F95")

# Main walls
polygon([
    (-635, -350), (-635, -260),
    (-245, -260), (-245, -350)
], "#354C6D", "#8AA3C4")

# Wall details
line(-635, -270, -245, -270, "#A4BAD6", 3)
line(-635, -340, -245, -340, "#172C4A", 3)

# Windows
for wx in [-590, -520, -320]:
    polygon([
        (wx, -345), (wx, -290),
        (wx + 42, -290), (wx + 42, -345)
    ], "#F5B95F", "#B67C38")

    line(wx + 21, -345, wx + 21, -290, "#754E35", 3)
    line(wx, -318, wx + 42, -318, "#754E35", 3)

# Building door
polygon([
    (-445, -430), (-445, -330),
    (-385, -330), (-385, -430)
], "#101D35", "#A3B9D6")

circle(-395, -380, 3, "#FFD477")

# 13. LARGE OBSERVATORY DOME

# Dome base
polygon([
    (-650, -270), (-650, -235),
    (-230, -235), (-230, -270)
], "#526E91", "#B4C7E1")

# Dome shape - semicircle
dome_points = [(-650, -235)]

for i in range(101):
    angle = math.pi * i / 100
    x = -440 + 210 * math.cos(angle)
    y = -235 + 210 * math.sin(angle)
    dome_points.append((x, y))

dome_points.append((-230, -235))

polygon(dome_points, "#263F66", "#A5BDE0")

# Dome curved panel lines
for angle in [30, 60, 90, 120, 150]:
    rad = math.radians(angle)

    x = -440 + 210 * math.cos(rad)
    y = -235 + 210 * math.sin(rad)

    line(-440, -235, x, y, "#607FA6", 2)

# Dome opening
polygon([
    (-455, -40), (-390, -40),
    (-390, -230), (-455, -230)
], "#080F22", "#B0C3DF")

# Golden inner glow
line(-390, -50, -390, -220, "#E6A65D", 5)
line(-455, -50, -455, -220, "#A66D42", 3)

# 14. TELESCOPE

# Telescope support tripod
line(-430, -225, -465, -130, "#8A9BB8", 7)
line(-430, -225, -370, -130, "#8A9BB8", 7)
line(-430, -225, -430, -120, "#D1B17A", 5)

# Telescope tube
line(-430, -135, -340, -75, "#B8C8D9", 27)
line(-430, -135, -340, -75, "#536D91", 19)

# Telescope barrel details
line(-405, -116, -395, -108, "#D8A95F", 4)
line(-380, -98, -370, -90, "#D8A95F", 4)

# Telescope lens
dot(-340, -75, 27, "#A5DDF8")
dot(-340, -75, 17, "#253E65")
dot(-344, -79, 8, "#D9F5FF")

# Telescope eyepiece
dot(-430, -135, 18, "#C2D0E3")

# 15. SMALL OBSERVATORY BUILDING

# Smaller building on the right
polygon([
    (-180, -430), (-180, -340),
    (-20, -340), (-20, -430)
], "#293E5E", "#8299B8")

# Roof
polygon([
    (-195, -340), (-100, -290),
    (-5, -340)
], "#536C8C", "#B0C1D7")

# Windows
for wx in [-160, -75]:
    polygon([
        (wx, -415), (wx, -365),
        (wx + 35, -365), (wx + 35, -415)
    ], "#FFD37A", "#C18B43")

    line(wx + 17, -415, wx + 17, -365, "#9A6735", 2)

# Small telescope dome
circle(40, -340, 45, "#314C70")
circle(40, -325, 45, "#526D94")

# Dome slit
polygon([
    (25, -285), (55, -285),
    (55, -330), (25, -330)
], "#0B172B")

# 16. OBSERVATORY LIGHTS

for x, y in [
    (-620, -340), (-500, -350),
    (-275, -350), (-120, -350),
    (-30, -360), (65, -380)
]:
    dot(x, y, 19, "#77512D")
    dot(x, y, 11, "#FFC96B")
    dot(x, y, 5, "#FFF2BA")

# 17. TITLE AND DECORATION

label(-170, 420, "BEYOND THE STARS",
      "#D5C5FF", 25)

label(-125, 395, "AN ASTRONOMICAL JOURNEY",
      "#8DBCEB", 11)

label(-590, -455, "MOUNTAIN OBSERVATORY",
      "#E5C58E", 10)

label(280, -430, "EXPLORE THE UNIVERSE",
      "#91B8E9", 10)

# Decorative horizontal line
line(-180, 385, 200, 385, "#5A72A7", 1)

# 18. FINAL RENDER

screen.update()
turtle.done()
