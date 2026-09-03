from turtle import *
from colorsys import *

bgcolor("black")
speed(0)
hideturtle()

h = 0

for i in range(1000):

    # Slowly change color
    h += 0.002
    color(hsv_to_rgb(h, 1, 1))

    # Draw outward
    forward(i * 0.5)

    # Rotate
    right(137)

done()