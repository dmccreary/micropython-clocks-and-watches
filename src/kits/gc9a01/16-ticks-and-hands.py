from machine import Pin, SPI
from utime import sleep, localtime
import math
import gc9a01

# this uses the standard Dupont ribbon cable spanning rows 4-9 on our breadboard
SCK_PIN = 2 # row 4
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
# GND is row 8
RST_PIN = 6

# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0
)
tft.init()
# A full circle is 2*Pi radians
TWO_PI = 3.1415926*2
WHITE = gc9a01.color565(255, 255, 255)
BLUE = gc9a01.color565(0, 0, 255)
GREEN = gc9a01.color565(0, 255, 0)
PURPLE = gc9a01.color565(255, 0, 255)
BLACK = gc9a01.color565(0, 0, 0)
tft.fill(BLACK)
CENTER = 120
MIN_TICK_START = 80
MIN_TICK_END = 98
SEC_TICK_START = 100
SEC_TICK_END = 120

def drawFilledTriangle(x1, y1, x2, y2, x3, y3, color=WHITE):
    def swap(x, y):
        return y, x
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
            tft.line(x, y, x, y, color)

def drawTicks():
    for i in range(0,60):
        radians = (i/60)*TWO_PI
        x1 = int(math.sin(radians)*SEC_TICK_START)
        y1 = -int(math.cos(radians)*SEC_TICK_START)
        x2 = int(math.sin(radians)*SEC_TICK_END)
        y2 = -int(math.cos(radians)*SEC_TICK_END)
        # print(i, radians, x1, y1, x2, y2)  
        tft.line(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, BLUE)

    for i in range(0,12):
        radians = (i/12)*TWO_PI
        x1 = int(math.sin(radians)*MIN_TICK_START)
        y1 = -int(math.cos(radians)*MIN_TICK_START)
        x2 = int(math.sin(radians)*MIN_TICK_END)
        y2 = -int(math.cos(radians)*MIN_TICK_END)
        # print(i, radians, x1, y1, x2, y2)  
        tft.line(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, GREEN)

CENTER = 120
SEC_HAND_LENGTH = 118
def drawSecondHand(sec):
    # print('sec=', sec)
    if sec ==0:
        radians = 0
    else: radians = (sec/60)*TWO_PI
    x = int(math.sin(radians)*SEC_HAND_LENGTH)
    y = -int(math.cos(radians)*SEC_HAND_LENGTH)
    # print(radians, x, y)
    tft.line(CENTER, CENTER, CENTER+x,CENTER+y, WHITE)
    sleep(.1)
    tft.line(CENTER, CENTER, CENTER+x,CENTER+y, BLACK)


MIN_HAND_LENGTH = 90
MIN_HAND_WIDTH = 5
def drawMinuteHand(min, color):
    radians = (min/60)*TWO_PI
    x1 = -int(math.cos(radians)*MIN_HAND_WIDTH)
    y1 = -int(math.sin(radians)*MIN_HAND_WIDTH)
    x2 = int(math.sin(radians)*MIN_HAND_LENGTH)
    y2 = -int(math.cos(radians)*MIN_HAND_LENGTH)
    x3 = int(math.cos(radians)*MIN_HAND_WIDTH)
    y3 = int(math.sin(radians)*MIN_HAND_WIDTH)
    # print('min:', x1, y1, x2, y2, x3, y3)
    drawFilledTriangle(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, CENTER+x3, CENTER+y3, color)

HOUR_HAND_LENGTH = 60
HOUR_HAND_WIDTH = 6
def drawHourHand(hour, color):
    radians = (hour/12)*TWO_PI
    x1 = -int(math.cos(radians)*HOUR_HAND_WIDTH)
    y1 = -int(math.sin(radians)*HOUR_HAND_WIDTH)
    x2 = int(math.sin(radians)*HOUR_HAND_LENGTH)
    y2 = -int(math.cos(radians)*HOUR_HAND_LENGTH)
    x3 = int(math.cos(radians)*HOUR_HAND_WIDTH)
    y3 = int(math.sin(radians)*HOUR_HAND_WIDTH)
    # print('hour:', x1, y1, x2, y2, x3, y3)
    drawFilledTriangle(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, CENTER+x3, CENTER+y3, color)

counter = 0
min = 58
hour = 6
drawMinuteHand(min, GREEN)
drawHourHand(hour, PURPLE)
hour = 6
while True:
    # this is the flicker
    # tft.fill(BLACK)
    drawTicks()
    drawHourHand(hour, PURPLE)
    drawMinuteHand(min, GREEN)
    drawSecondHand(counter)
    # if we are at 60 we start over
    if counter > 59:
        drawMinuteHand(min, BLACK)
        counter = 0
        min += 1
        drawMinuteHand(min, GREEN)
        if min > 59:
            min=0
            drawHourHand(hour, BLACK)
            hour += 1
            drawHourHand(hour, PURPLE)
            if hour > 11:
                hour = 0
    counter += 1
    # sleep(.5)
    