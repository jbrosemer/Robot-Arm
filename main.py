# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import turtle
import math
from adafruit_servokit import ServoKit
t = turtle.Turtle()
# declaring servo kit
kit = ServoKit(channels=16)
j_index = int(input('Please input how many letters you want to write: '))
offset = -j_index*200+j_index*100
width = (200*j_index)+(200*j_index)/(j_index+1)
# turtle.screensize(canvwidth=width,canvheight=300)
t.speed(1)
t.pensize(10)
t.penup()
t.goto(0, 0)


file = open("alphabet.txt")
alphabet = file.read()
# x offset from origin
xoff = 0
# y offset from paper
yoff = 2
abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters = alphabet.split(';')
j = 0
#theta direction servo
kit.servo[0].angle = 90
# r direction servo
kit.servo[1].angle = 0
# dump servo
kit.servo[2].angle = 180
dump = False
while j < j_index:
    letter = input('Please input the letter you want to write: ')
    jj = 0

    #find which letter we want to write
    for jj in range(len(abc)):
        if letter == abc[jj]:
            index = jj
            jj = len(abc)
        else:
            jj += 1
    vectors = letters[index].split(',')

    t.goto(offset, 0)
    max = 0
    for i in range(len(vectors)):
        t.penup()
        bounds = vectors[i].split('{')
        function = bounds[0]
        function = function.split('=')
        bounds = bounds[1].split('}')
        lowerbound = bounds[0].split('<')
        if len(lowerbound) > 2:
            LB = float(lowerbound[0])
            UB = float(lowerbound[2])
        else:
            LB = 0
            UB = float(lowerbound[1])
        # for z in range(UB*100):



        # Function Parsing
        if function[0] == 'y':
            x = LB
            while x <= UB:

                y = eval(function[1])
                t.goto(x*100 + offset, y*100)
                if (x*100 + offset) != 0:
                    theta = math.atan(((y+yoff)*100)/(x*100 + offset))
                else:
                    theta = (math.pi)/2
                t.penup()
                print(round(x * 100))
                if round(x*100) % 18 == 0:
                    t.pendown()
                    if not dump:
                        kit.servo[2].angle = 0
                        dump = True
                if x >= UB-0.01:
                    t.pendown()
                    if not dump:
                        kit.servo[2].angle = 0
                        dump = True
                    kit.servo[2].angle = 0
                else:
                    if dump:
                        kit.servo[2].angle = 180
                        dump = False
                x += 0.002
                if(x>max):
                    max = x
        elif function[0] == 'x':
            y = LB
            while y <= UB:
                x = eval(function[1])
                t.goto(x * 100 + offset, y * 100)
                t.penup()
                kit.servo[2].angle = 180
                if round(y*100) % 25 == 0:
                    t.pendown()
                    kit.servo[2].angle = 0
                if y >= UB-0.02:
                    t.pendown()
                    kit.servo[2].angle = 0
                y += 0.001
        else:
            if lowerbound[0] == 'x':
                x = LB
                while x <= UB:
                    y = eval(function[1])
                    t.goto(x * 100 + offset, y * 100)
                    t.penup()
                    kit.servo[2].angle = 180
                    if round(x * 100) % 25 == 0:
                        t.pendown()
                        kit.servo[2].angle = 0
                    if x >= UB - 0.02:
                        kit.servo[2].angle = 0
                        t.pendown()
                    x += 0.001
                    if (x > max):
                        max = x
            else:
                y = LB
                while y <= UB:
                    x = eval(function[1])
                    t.goto(x * 100 + offset, y * 100)
                    t.penup()
                    if round(y * 100) % 25 == 0:
                        t.pendown()
                    if y >= UB - 0.02:
                        t.pendown()
                    y += 0.001
        t.penup()
        i += 1
    offset = offset + max*100 + 50
    j += 1
t.goto(0,0)
turtle.exitonclick()
