from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math

LCD = LCD_1inch28()
# bit order is blue, red, green
black = 0x0000
red   = 0x07E0
green = 0x001f
blue  = 0xf800
white = 0xffff
#
yellow = 0b0000011111111111
orange = 0b0000001111000010
cyan = 0b1111100000111111
brown = 0b0000000001000001
gold = 0b0000001110011110
purple = 0b1111111111000000
magenta = 0b0000001100011000
pink = 0b0000111111000010
olive = 0b0000000001000010
gray = 0b00001000010000100
lightGreen = 0b0000100001111111
darkGreen  = 0b0000000000000001

ColorList = (red, green, blue, white, yellow, orange, cyan, brown, gold, purple, magenta, pink, olive, gray, lightGreen, darkGreen)
ColorNames = ('red', 'green', 'blue', 'white', 'yellow', 'orange', 'cyan', 'brown', 'gold', 'purple', 'magenta', 'pink', 'olive', 'gray', 'lightGreen', 'darkGreen')

CENTER = 120
# draw readability variables
ON = 1 # white
OFF = 0 # black
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn

while True:
    now = localtime()
    sec = now[5] # 0 to 59
    radians = (sec/60)*3.145175*2
    x = int(math.sin(radians)*120)
    y = -int(math.cos(radians)*120)
    print(sec, radians, x, y)
    LCD.fill(LCD.black)
    # axis lines
    LCD.line(CENTER, 0, CENTER, 2*CENTER, blue)
    LCD.line(0, CENTER, 2*CENTER, CENTER, blue)
    LCD.line(CENTER, CENTER, 100, 100, ON)

    my_array = array('B', [CENTER-5,CENTER-5, CENTER+x,CENTER+y, CENTER+5,CENTER+5])
    LCD.poly(0,0, my_array, white, FILL)
    LCD.show()
    sleep(1)
