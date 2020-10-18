from tkinter import *
from time import *
from random import *

myInterface = Tk()
s = Canvas(myInterface, width=800, height=800, background="black")
s.pack()

#INITIAL VALUES - DO NOT CHANGE
n = 20   #number of balls
d = 30   #diameter of the balls

#WALL LOCATIONS - DO NOT CHANGE
wallLeft = 100
wallTop = 100
wallRight = 700
wallBottom = 700

#DRAW WALLS
s.create_line(100, 100, 100, 700, fill = 'yellow', width = 6)
s.create_line(100, 700, 700, 700, fill = 'yellow', width = 6)
s.create_line(700, 100, 700, 700, fill = 'yellow', width = 6)
s.create_line(100, 100, 700, 100, fill = 'yellow', width = 6)


#CREATE EMPTY ARRAYS
x = []
y = []
xSpeed = []
ySpeed = []
drawings = []
colours = []

#FILL ARRAYS WITH STARTING VALUES
for i in range(n):
    x.append(400)
    y.append(400)
    xSpeed.append(randint(-8, 8))
    ySpeed.append(randint(-8, 8))
    colours.append(choice(['red', 'blue', 'green', 'purple', 'white']))
    drawings.append(0)

while True:
    for i in range(n):
        drawings[i] = s.create_oval(x[i]-d/2, y[i]-d/2, x[i]+d/2, y[i]+d/2, fill = colours[i], outline = colours[i])

        if x[i]-d/2 <= wallLeft or x[i]+d/2 >= wallRight:
            xSpeed[i] = -xSpeed[i]

        if y[i]-d/2 <= wallTop or y[i]+d/2 >= wallBottom:
            ySpeed[i] = -ySpeed[i]

        x[i] += xSpeed[i]
        y[i] += ySpeed[i]

    s.update()
    sleep(0.03)
    for i in range(n):
        s.delete(drawings[i])
