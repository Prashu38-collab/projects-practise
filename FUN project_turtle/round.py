
import turtle

screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Colorful Turtle Pattern")

pen = turtle.Turtle()
pen.speed(0)
pen.width(2)

colors = ["red", "orange", "yellow", "lime", "cyan", "magenta", "purple"]

for i in range(72):
    pen.color(colors[i % len(colors)])

    for j in range(4):
        pen.forward(100)
        pen.right(90)

    pen.right(5)

turtle.done()
