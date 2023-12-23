"""ILI9341 demo (fonts)."""
from ili9341 import Display, color565
from machine import Pin, SPI
from time import sleep
import config
import colors
from math import sin, cos
from xglcd_font import XglcdFont

# Use these PIN definitions.  SCK must be on 2 and data (SDL) on 3
SCK_PIN = config.SCK_PIN
MISO_PIN = config.MISO_PIN # labeled SDI(MOSI) on the back of the display
DC_PIN = config.DC_PIN
RESET_PIN = config.RESET_PIN
CS_PIN = config.CS_PIN

WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
ROTATION=config.ROTATION

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

# this makes our code a little more readable
white = colors.WHITE
red = colors.RED
orange = colors.ORANGE
yellow = colors.YELLOW
green = colors.GREEN
blue = colors.BLUE
cyan = colors.CYAN
purple = colors.PURPLE
black = colors.BLACK

print('Loading unispace font')
unispace = XglcdFont('fonts/Unispace12x24.c', 12, 24)
print('Fonts loaded.')

HW = WIDTH // 2
HH = HEIGHT // 2
RADIANS_PER_DIGIT = 3.141529 / 6
FACE_RADIUS = 104

def drawFilledTriangle(x1, y1, x2, y2, x3, y3, color=white):
    def swap(x, y):
        return y, x

    # get our points in order
    if y1 > y2:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
    if y1 > y3:
        x1, x3 = swap(x1, x3)
        y1, y3 = swap(y1, y3)
    if y2 > y3:
        x2, x3 = swap(x2, x3)
        y2, y3 = swap(y2, y3)

    for y in range(y1, y3+1):
        if y2 - y1 != 0 and y < y2:
            xa = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
        elif y3 - y1 != 0:
            xa = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if y3 - y2 != 0 and y >= y2:
            xb = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
        elif y3 - y1 != 0:
            xb = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if xa > xb:
            xa, xb = swap(xa, xb)

        for x in range(xa, xb+1):
            # sleep(.1)
            display.draw_line(x, y, x, y, color)

def draw_digits():
    for i in range(0, 12):
        x = HW + int(sin(i*RADIANS_PER_DIGIT) * FACE_RADIUS) - 6
        y = HH - int(cos(i*RADIANS_PER_DIGIT) * FACE_RADIUS) - 9
        if i == 0:
            text = '12'
        else: text = str(i)
        display.draw_text(x, y, text, unispace, cyan)

display.draw_circle(HW, HH, 119, yellow)
while True:
    for i in range(0, 12):
        # mockups of hands
        # minute hand on 3
        drawFilledTriangle(HW, HH -5, HW+80, HH, HW, HH +5, white)
        # hour hand
        drawFilledTriangle(HW+7,HH, HW+10,70, HW-7, HH, green)
        draw_digits()
        # 119 is the max radius that can be drawn on the display
        
        x = HW + int(sin(i*RADIANS_PER_DIGIT) * (FACE_RADIUS+10))
        y = HH - int(cos(i*RADIANS_PER_DIGIT) * (FACE_RADIUS+10))
        display.draw_line(HW, HH, x, y, red)
        sleep(1)
        display.draw_line(HW, HH, x, y, black)
