# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import turtle
import math
# from adafruit_servokit import ServoKit
t = turtle.Turtle()
# declaring servo kit
# kit = ServoKit(channels=16)
initials = (input('Please input what you want to write: '))
j_index = len(initials)
offset = -j_index*200+j_index*100
t.speed(1)
t.pensize(10)
t.penup()
t.goto(0, 0)


file = open("alphabet.txt")
alphabet = file.read()
# x offset from origin
xoff = 0
# y offset from paper
yoff = 1
rlimit = 10
abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
letters = alphabet.split(';')
j = 0
# theta direction servo
# kit.servo[0].angle = 90
# r direction servo
# kit.servo[1].angle = 0
# dump servo
# kit.servo[2].set_pulse_width_range(700, 3000)
# kit.servo[2].angle = 180
dump = False
xinc = 0.002
yinc = 0.001
while j < j_index:
    jj = 0

    #find which letter we want to write
    for jj in range(len(abc)):
        if initials[j] == abc[jj]:
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
        scaler = 2
        LB = float(scaler*LB)
        UB = float(scaler*UB)

        print(function[0])
        # Function Parsing
        if function[0] == 'y':
            x = LB
            if scaler > 1:
                function[1] = function[1].replace("x", "x/" + str(scaler))
            while x <= UB:
                y = scaler * eval(function[1])
                if (x*100 + offset) != 0:
                    theta = math.atan(((y+yoff)*100)/(x*100 + offset))*180/math.pi
                else:
                    theta = 90
                r = math.sqrt((x + offset / 100) ** 2 + (y + yoff) ** 2)
                # if theta < 0:
                    # kit.servo[0].angle = 180 + theta
                # else:
                    # kit.servo[0].angle = theta
                # kit.servo[1].angle = 180 * (r / rlimit)
                t.goto(x*100 + offset, y*100)
                t.penup()
                if round(x*100) % 18 == 0:
                    t.pendown()
                    if not dump:
                        # kit.servo[2].angle = 0
                        dump = True
                        xinc = 0.005
                elif x >= UB-0.01:
                    t.pendown()
                    if not dump:
                        dump = True
                        xinc = 0.0025
                    # kit.servo[2].angle = 0
                else:
                    if dump:
                        # kit.servo[2].angle = 180
                        dump = False
                        xinc = 0.01
                x += xinc
                if x>max:
                    max = x

        elif function[0] == 'x':
            y = LB
            function[1] = function[1].replace("y", "y/" + str(scaler))
            while y <= UB:
                x = eval(function[1])*scaler
                if (x*100 + offset) != 0:
                    theta = math.atan(((y+yoff)*100)/(x*100 + offset))*180/math.pi
                else:
                    theta = 90
                r = math.sqrt((x + offset / 100) ** 2 + (y + yoff) ** 2)
                # if theta < 0:
                    # kit.servo[0].angle = 180 + theta
                # else:
                    # kit.servo[0].angle = theta
                # kit.servo[1].angle = 180 * (r / rlimit)
                t.goto(x * 100 + offset, y * 100)
                t.penup()
                if round(y*100) % 25 == 0:
                    t.pendown()
                    if not dump:
                        # kit.servo[2].angle = 0
                        dump = True
                        yinc = 0.002
                elif y >= UB-0.02:
                    t.pendown()
                    if not dump:
                        dump = True
                        yinc = 0.002
                    # kit.servo[2].angle = 0
                else:
                    if dump:
                        # kit.servo[2].angle = 180
                        dump = False
                        yinc = 0.02
                y += yinc
                if x>max:
                    max = x
        else:
            if lowerbound[0] == 'x':
                x = LB
                function[1] = function[1].replace("x", "x/" + str(scaler))
                while x <= UB:
                    y = eval(function[1])*scaler
                    t.goto(x * 100 + offset, y * 100)
                    t.penup()
                    # kit.servo[2].angle = 180
                    if round(x * 100) % 25 == 0:
                        t.pendown()
                        if not dump:
                            # kit.servo[2].angle = 0
                            dump = True
                            xinc = 0.001
                    elif x >= UB - 0.02:
                        if not dump:
                            dump = True
                            xinc = 0.001
                        # kit.servo[2].angle = 0
                    else:
                        if dump:
                            # kit.servo[2].angle = 180
                            dump = False
                            xinc = 0.02
                    if (x > max):
                        max = x
            else:
                y = LB
                function[1] = function[1].replace("y", "y/" + str(scaler))
                while y <= UB:
                    x = eval(function[1])*scaler
                    t.goto(x * 100 + offset, y * 100)
                    t.penup()
                    if round(y * 100) % 25 == 0:
                        if not dump:
                            # kit.servo[2].angle = 0
                            dump = True
                            yinc = 0.01
                    elif y >= UB - 0.02:
                        if not dump:
                            dump = True
                            yinc = 0.01
                        # kit.servo[2].angle = 0
                    else:
                        if dump:
                            # kit.servo[2].angle = 180
                            dump = False
                            yinc = 0.02
        i += 1
        t.penup()
    offset = offset + max*100 + 50
    # kit.servo[0].angle = 90
    j += 1
t.penup()
t.goto(0,0)
turtle.exitonclick()
