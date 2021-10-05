# Robot-Arm
This project was designed to write letters for a robot arm. Rather than parsing an SVG file in python this assumes your end effector is the drawing tool and it is located at the x,y coordinates.

alphabet.txt is a file composed of equations to write letters in the x,y coordinate plane, with the bottom left of each letter at the origin. 

The alphabet file is parsed by:
; in between each letter 
, in between each 'vector'
{} holds the bounds of each 'vector'

The python code essentially writes dotted letters of your choice. If you do not want dotted letters and just want straight lines remove the 
if round(x * 100) % 25 == 0:

blocks in the code and replace with t.pendown()
