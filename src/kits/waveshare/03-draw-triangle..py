from utime import localtime, sleep
from LCD_1inch28 import LCD_1inch28
from array import array
import math

LCD = LCD_1inch28()
white = 0xffff


CENTER = 120
# draw readability variables
ON = 1 # white
OFF = 0 # black
NO_FILL = 0 # just the border is drawn
FILL = 1 # all pixels within the polygon are drawn

LCD.fill(LCD.black)

# distance from the center to the tip of the traiangle
d = 50

my_array = array('B', [CENTER-d,CENTER+d, CENTER,CENTER-d, CENTER+d,CENTER+d])
LCD.poly(0,0, my_array, white, FILL)
LCD.show()

