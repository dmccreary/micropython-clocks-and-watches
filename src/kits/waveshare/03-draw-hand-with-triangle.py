from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math
TWO_PI = 3.145175*2

LCD = LCD_1inch28()

CENTER = 120
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn
HAND_LENGTH = 100
TRIANGLE_SIZE = 10

def drawTriangle(x, y, size, seconds):
    radians = (seconds/60)*TWO_PI
    # calculate the offsets
    xo = int(math.cos(radians)*size)
    yo = int(math.sin(radians)*size)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('B', [x-xo,y-yo,  x+yo,y-xo,  x+xo,y+yo])
    LCD.poly(0,0, arr, LCD.white, FILL)

counter = 0
while True:
    LCD.fill(LCD.blue)
    radians = (counter/60)*TWO_PI
    x = int(math.sin(radians)*HAND_LENGTH)
    y = -int(math.cos(radians)*HAND_LENGTH)
    LCD.line(CENTER, CENTER, CENTER+x,CENTER+y, LCD.white)
    drawTriangle(CENTER+x, CENTER+y, TRIANGLE_SIZE, counter)
    LCD.show()
    sleep(.1)
    counter += 1
    # if we are at 60 we start over
    if counter > 59:
        counter = 0