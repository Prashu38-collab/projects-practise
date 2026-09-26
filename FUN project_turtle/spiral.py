
import turtle

# Set up the screen
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Colorful Spiral")

# Create a turtle
t = turtle.Turtle()
t.speed(0)  # Fastest speed
t.width(2)

# List of colors
colors = ["red", "orange", "yellow", "green", "blue", "purple"]

# Draw the spiral
for i in range(360):
    t.pencolor(colors[i % len(colors)])  # Cycle through colors
    t.forward(i * 2)                     # Move forward 
    t.right(59)                          # Turn right by 59 degrees

# Keep the window open
t.hideturtle()
screen.mainloop()
