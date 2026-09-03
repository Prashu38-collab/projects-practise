from turtle import *
from colorsys import *

bgcolor("black")
tracer(0)
pensize(2)

h = 0

for i in range(360):
    h += 0.003
    r, g, b = hsv_to_rgb(h, 1, 1)     # glowing neon color
    color(r, g, b)

    up()
    goto(0, 0)
    down()

    # inner glowing swirl
    circle(i/3, 60)
    left(20)

    # outer shining petals
    for j in range(5):
        circle(150 - i/5, 60)
        right(120)

    right(7)          # rotation for 3D effect
    pensize(1 + i/150)  # glowing thickness

    update()          # smooth animation

done()