from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math
TWO_PI = 3.145175*2

LCD = LCD_1inch28()
# turn on the backlight to full
LCD.set_bl_pwm(65535)

WIDTH = 240
HEIGHT = 240
CENTER = 120
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn
green = 0x001f
yellow = 0b0000011111111111

def drawTriangle(x, y, size, seconds, color):
    radians = (seconds/60)*TWO_PI
    # calculate the offsets
    xo = int(math.cos(radians)*size)
    yo = int(math.sin(radians)*size)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('B', [x-xo,y-yo,  x+yo,y-xo,  x+xo,y+yo])
    LCD.poly(0,0, arr, color, FILL)

def drawMinuteHand(minute, width, length, color):
    radians = (minute/60)*TWO_PI
    # calculate the offsets
    x1 = int(math.cos(-radians)*width)
    y1 = int(math.sin(-radians)*width)
    x2 = int(math.sin(radians)*length)
    y2 = -int(math.cos(radians)*length)
    # print(x1, y1, x2, y2)
    # LCD.line(CENTER, CENTER, CENTER+x2, CENTER+y2, LCD.white)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('h', [x1,-y1,  x2,y2,  -x1,y1])
    LCD.poly(CENTER, CENTER, arr, color, FILL)

def drawHourHand(hours, minutes, width, length, color):
    radians = (hours/12 + minutes/60/12																																																																																																																																																			)*TWO_PI
    # calculate the offsets
    x1 = int(math.cos(-radians)*width)
    y1 = int(math.sin(-radians)*width)
    x2 = int(math.sin(radians)*length)
    y2 = -int(math.cos(radians)*length)
    # build the array - use B if we have under 255 and h if over 255
    arr = array('h', [x1,-y1,  x2,y2,  -x1,y1])
    LCD.poly(CENTER,CENTER, arr, color, FILL)

def drawSecondHand(seconds, length, triange_size, color):
    radians = (seconds/60)*TWO_PI
    x = int(math.sin(radians)*length)
    y = -int(math.cos(radians)*length)
    LCD.line(CENTER, CENTER, CENTER+x, CENTER+y, color)
    drawTriangle(CENTER+x, CENTER+y, triange_size, seconds, color)
    
# draw the 60 minute markers
MIN_MARKER_START = 100
MIN_MARKER_END = 120

c=CENTER
def draw_minute_ticks():
    for i in range(0,60):
        radians = (i/60)*TWO_PI
        x1 = int(math.sin(radians)*MIN_MARKER_START)
        y1 = -int(math.cos(radians)*MIN_MARKER_START)
        x2 = int(math.sin(radians)*MIN_MARKER_END)
        y2 = -int(math.cos(radians)*MIN_MARKER_END)
        LCD.line(c+x1, c+y1, c+x2, c+y2, LCD.white)

# draw the hour markers
HOUR_MARKER_START = 75
HOUR_MARKER_END = 90
def draw_hour_ticks():
    for i in range(0,12):
        radians = (i/12)*TWO_PI
        x1 = int(math.sin(radians)*HOUR_MARKER_START)
        y1 = -int(math.cos(radians)*HOUR_MARKER_START)
        x2 = int(math.sin(radians)*HOUR_MARKER_END)
        y2 = -int(math.cos(radians)*HOUR_MARKER_END)
        LCD.line(c+x1, c+y1, c+x2, c+y2, LCD.green)

# main event loop

# main code

SECOND_HAND_TRIANGLE_SIZE = 6
SECOND_HAND_LENGTH = 110

MINUTE_HAND_WIDTH = 4
MINUTE_HAND_LENGTH = 100

HOUR_HAND_WIDTH = 8
HOUR_HAND_LENGTH = 60

# for demo mode
# hours = 9
# minutes = 55
# seconds = 20

hours = localtime()[3]
minutes = localtime()[4]
seconds = localtime()[5]

seconds = 0
while True:
    LCD.fill(LCD.blue)
    draw_minute_ticks()
    draw_hour_ticks()
    drawSecondHand(seconds, SECOND_HAND_LENGTH, SECOND_HAND_TRIANGLE_SIZE, LCD.red)
    drawMinuteHand(minutes, MINUTE_HAND_WIDTH, MINUTE_HAND_LENGTH, yellow)
    drawHourHand(hours, minutes, HOUR_HAND_WIDTH, HOUR_HAND_LENGTH, yellow)
    # drawHourHand(hours, 10, 50)
    # send buffer to the display
    LCD.show()
    seconds += 1
    if seconds > 59:
        seconds = 0
        minutes += 1
        if minutes > 59:
            minutes = 0
            hours += 1
            if hours > 11:
                hours = 0
    sleep(.01)
