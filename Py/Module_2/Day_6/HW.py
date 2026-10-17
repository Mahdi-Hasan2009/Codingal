import turtle

t = turtle
t.Screen().bgcolor("Green")
T = turtle.Turtle()
T.color("white")
T.width(1)
T.penup()
T.goto(-100,100)
T.pendown()
T.fillcolor("Red")
T.begin_fill()
for i in range(0,8,2):
  T.forward(100)
  T.right(90)
T.end_fill()


T.hideturtle()

t.done()