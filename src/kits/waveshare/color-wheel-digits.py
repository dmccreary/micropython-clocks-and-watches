from LCD_1inch28 import LCD_1inch28
import math
from utime import sleep
LCD = LCD_1inch28()

def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colors are a transition r - g - b - back to r.
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

def colorRGB(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) + ((B&0b11111000)>>3)<<8) + (R&0b11111000) + ((G&0b11100000)>>5)

LCD.fill(LCD.black)
TWO_PI = 2*3.1415917
CENTER = 120
HAND_LENGTH = 120
RESOLUTION = 255
for i in range(0, RESOLUTION):
    radians = (i/RESOLUTION)*TWO_PI
    x = int(math.sin(radians)*HAND_LENGTH)
    y = -int(math.cos(radians)*HAND_LENGTH)
    rgb_triple = wheel(i)
    red = rgb_triple[0]
    green = rgb_triple[1]
    blue = rgb_triple[2]
    print('i:', i, ' rgb: ', red, green, blue, ' rad x y', radians, x, y)
    color = colorRGB(red, green, blue)
    LCD.line(CENTER, CENTER, CENTER+x,CENTER+y, color)
    sleep(.01)
    LCD.show()

# draw the digits for the 12 hour markers
DIGIT_DIST = 100
for i in range(0, 12):
    radians = (i/12)*TWO_PI
    x = int(math.sin(radians)*DIGIT_DIST)
    y = -int(math.cos(radians)*DIGIT_DIST)
    
