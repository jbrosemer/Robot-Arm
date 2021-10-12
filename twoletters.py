

# all turtle commands and t lines are commented for the display.
# To note the turtle code runs much slower than the actual motors.
# Displaying the letters slows down the computation by a lot.

# import turtle
import math
from adafruit_servokit import ServoKit
# t = turtle.Turtle()
# declaring servo kit
kit = ServoKit(channels=16)
# ask the command line what to write
# kit.servo[2].set_pulse_width_range(600, 3600)
# kit.servo[2].angle = 180

# theta direction servo
# kit.servo[1].angle = 90
# r direction servo
# kit.servo[3].angle = 0

initials = (input('Please input what you want to write: '))
# defines the scaler variable, defines the size of the letter you are writing
        # going below 0 is not recommended
scaler = 2
# offset of the letters is based on the number of letters you want to write
offset = -(scaler)
#defines basic turtle display variables
# t.speed(1)
# t.pensize(10)
# t.penup()
# t.goto(0, 0)

# opens the alphabet vector file
file = open("alphabet.txt")
# reads the alphabet file into a string
alphabet = file.read()
# y offset from paper
yoff = 5
# r extension to max position
rlimit = 13

xinc = 0.00003
yinc = 0.0004

# all of the letters in the alphabet
abc = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

# splits the alphabet file by all of the letters
letters = alphabet.split(';')

# don't dump initially
dump = False
# variable to index through
j = 0
# loops through all of the letters you said to write
for j in range(len(initials)):
    jj = 0
    ##
    # loop to find which letter we want to write
    for jj in range(len(abc)):
        if initials[j] == abc[jj]:
            index = jj
            jj = len(abc)
        else:
            jj += 1
    # vectors is the string of all the functions that compose the letter you chose
    vectors = letters[index].split(',')
    # sends turtle to your predefined offset and the 0 y position
    # t.goto(offset, 0)

    max = 0
    for i in range(len(vectors)):

        # t.penup()
        # beginning of the overall loop that loops through each vector
        # the next 16 lines find the bounds of each vector each time through the loop.
        # all it is doing is parsing the vector components of each letter
        bounds = vectors[i].split('{')
        function = bounds[0]
        function = function.split('=')
        bounds = bounds[1].split('}')
        lowerbound = bounds[0].split('<')

        # if the length of the bound parse is long
        # there is a lower and upper bound to the vector
        if len(lowerbound) > 2:
            LB = float(lowerbound[0])
            UB = float(lowerbound[2])

        # if not there is only an upper bound
        # and set the lowerbound to 0
        else:
            LB = 0
            UB = float(lowerbound[1])

        # scales the bounds by the scaler variable
        LB = float(scaler*LB)
        UB = float(scaler*UB)

        # this just prints what kind of function is being written. one in terms of y or x
        print(function[0] + " LINE")
        # Function Parsing
        # If the function is in terms of y we go here
        if function[0] == 'y':
            # set the x position to the lowerbound
            x = LB
            # define the function in terms of the scaler.
            # In order to scale a y function you need to divide the x component by the scaler
            # this line replaces the x in every function with x divided by the scaler
            # when scaler is 1 this is just x/1
            function[1] = function[1].replace("x", "x/" + str(scaler))
            while x <= UB:
                # evaluates the function and sets it equal to y
                # also to scale a y function you must multiply the result of the evaluation by the scaler
                y = scaler * eval(function[1])
                # print("y " + str(y))
                # print("x " + str(x))
                # any scaling needed is finished now.

                # if the x position is 0 the math cannot be calculated without an error
                # this if just basically stops dividing by 0. Will need to be changed when the offset changes
                if (x+offset) != 0:
                    theta = math.atan(((y + yoff))/(x + offset))*180/math.pi
                # if divide by 0 would occur set theta to pi/2
                else:
                    theta = 90
                # r is basic polar sqrt of x^2 + y^2 the offsets
                # are needed to define position based on them
                r = math.sqrt(((x + offset)) ** 2 + (y + yoff) ** 2)
                # when some of the letter is in the left
                # half of the plane the resulting angle is negative
                # this is fixed by adding the negative angle to 180.
                # so the motor successfully can rotate from 0 degrees to 180
                # if theta < 0:
                    # kit.servo[1].angle = 180 + theta
                # else:
                    # kit.servo[1].angle = theta
                # the r limit defines the distance r CAN travel. if r is the longest distance theta should be 180
                # kit.servo[3].angle = 180 * ((r) / rlimit)
                # print("r " + str(180 * ((r) / rlimit)))



                # this block is how dots are written rather than straight lines
                # AKA if the x value is divisible by some arbitrary value draw otherwise don't
                # I could have done the math for the length of the vector
                # and set some variable for how many dots I want to draw but I didn't bother
                if round(x*100) % round(18*scaler) == 0:

                    # if we are not currently dumping and we should be. Turn the motor and dump
                    if not dump:

                        # kit.servo[2].angle = 0
                        dump = True
                        # slow down the incrementation when we are supposed to be dumping.
                        # this allows for all the salt to come out
                        xinc = 0.00003
                # if the number is not divisible by my arbitrary value, BUT it IS near a bound point draw
                elif x >= UB-0.01:
                    # if we are not currently dumping and we should be. Turn the motor and dump
                    if not dump:
                        dump = True
                        # slow down the incrementation when we are supposed to be dumping.
                        # this needs to be smaller than the previous slow incrementation
                        # because on curves the bound points tend to require a lot of detail.
                        xinc = 0.00003
                    # kit.servo[2].angle = 0
                # if neither of the prior cases are true we should not be dumping
                else:
                    # if dump is still true rotate the motor back and stop dump
                    # we move faster through this loop because we do not slow to dump
                    if dump:
                        print("r " + str(180 * ((r) / rlimit)))
                        if theta < 0:
                            print("theta " + str(180 + theta))
                        else:
                            print("theta " + str(theta))
                        print("y " + str(y+yoff))
                        print("x " + str(x + offset))
                        # kit.servo[2].angle = 180
                        dump = False
                        xinc = 0.0005

                # increment x by the defined x increment.
                # Essentially the last 40 lines are all to rotate the dump motor and get this value.
                x += xinc

                # an important not to be overlooked line.
                # This defines the offset needed for the last letter written
                # so we can offset and write the next letter
                if x>max:
                    max = x

        # this is all essentially the same thing as the last 70 lines except for a function defined by x
        # this is pretty much just to write straight vertical lines
        # these lines could probably be removed and i could do everything in the y if statement
        # but I don't feel like fixing that
        elif function[0] == 'x':
            y = LB
            function[1] = function[1].replace("y", "y/" + str(scaler))
            while y <= UB:
                x = eval(function[1])*scaler
                if (x+offset) != 0:
                    theta = math.atan(((y + yoff))/(x + offset))*180/math.pi
                else:
                    theta = 90
                r = math.sqrt((x + offset - 1) ** 2 + (y + yoff) ** 2)
                # if theta < 0:
                    # kit.servo[1].angle = 180 + theta
                    # print("theta " + str(180 + theta))
                # else:
                    # kit.servo[1].angle = theta
                    # print("theta " + str(theta))
                # print("theta " + str(theta))
                # kit.servo[3].angle = 180 * ((r) / rlimit)
                if round(y*100) % round(18*scaler) == 0:
                    if not dump:
                        # kit.servo[2].angle = 0
                        dump = True
                        yinc = 0.00005
                elif y >= UB-0.02:
                    if not dump:
                        dump = True
                        yinc = 0.00005
                    # kit.servo[2].angle = 0
                else:
                    if dump:
                        print("r " + str(180 * ((r) / rlimit)))
                        if theta < 0:
                            print("theta " + str(180 + theta))
                        else:
                            print("theta " + str(theta))
                        print("y " + str(y+yoff))
                        print("x " + str(x + offset))
                        # kit.servo[2].angle = 180
                        dump = False
                        yinc = 0.0004
                # increments by the y value decided
                y += yinc
                # although these are vertical lines. There is still one letter
                # that is only composed of x domain equations can you guess which letter it is?
                if x>max:
                    max = x
        # im not sure if these elses are needed
        else:
            if lowerbound[0] == 'x':
                x = LB
                function[1] = function[1].replace("x", "x/" + str(scaler))
                while x <= UB:
                    y = eval(function[1])*scaler
                    # kit.servo[2].angle = 180
                    if round(x * 100) % 25 == 0:
                        if not dump:
                            # kit.servo[2].angle = 0
                            dump = True
                            xinc = 0.0001
                    elif x >= UB - 0.02:
                        if not dump:
                            dump = True
                            xinc = 0.0001
                        # kit.servo[2].angle = 0
                    else:
                        if dump:
                            # kit.servo[2].angle = 180
                            dump = False
                            xinc = 0.00001
                    if (x > max):
                        max = x
            else:
                y = LB
                function[1] = function[1].replace("y", "y/" + str(scaler))
                while y <= UB:
                    x = eval(function[1])*scaler
                    if round(y * 100) % 25 == 0:
                        if not dump:
                            # kit.servo[2].angle = 0
                            dump = True
                            yinc = 0.0001
                    elif y >= UB - 0.02:
                        if not dump:
                            dump = True
                            yinc = 0.0001
                        # kit.servo[2].angle = 0
                    else:
                        if dump:
                            # kit.servo[2].angle = 180
                            dump = False
                            yinc = 0.0002
        # go to the next vector of the function
        i += 1
    # offset your letter so you can write the next letter not on top of the prior
    # offset = offset + max*100 + 50
    yoff -= (scaler*2 + 1)
    # reset the theta motor to 90
    # go to the next letter
    j += 1
# turtle.exitonclick()
