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

CENTER = 120
MIN_TICK_START = 80
MIN_TICK_END = 98
SEC_TICK_START = 100
SEC_TICK_END = 120

# our counter will range from 0 to 59
# A full circle is 2*Pi radians
TWO_PI = 3.145175*2
counter = 0
WHITE = gc9a01.color565(255, 255, 255)
BLUE = gc9a01.color565(0, 0, 255)
GREEN = gc9a01.color565(0, 255, 0)

BLACK = gc9a01.color565(0, 0, 0)
tft.fill(BLACK)

for i in range(0,60):
    radians = (i/60)*TWO_PI
    x1 = int(math.sin(radians)*SEC_TICK_START)
    y1 = -int(math.cos(radians)*SEC_TICK_START)
    x2 = int(math.sin(radians)*SEC_TICK_END)
    y2 = -int(math.cos(radians)*SEC_TICK_END)
    print(i, radians, x1, y1, x2, y2)  
    tft.line(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, BLUE)

for i in range(0,12):
    radians = (i/12)*TWO_PI
    x1 = int(math.sin(radians)*MIN_TICK_START)
    y1 = -int(math.cos(radians)*MIN_TICK_START)
    x2 = int(math.sin(radians)*MIN_TICK_END)
    y2 = -int(math.cos(radians)*MIN_TICK_END)
    print(i, radians, x1, y1, x2, y2)  
    tft.line(CENTER+x1, CENTER+y1, CENTER+x2, CENTER+y2, GREEN)