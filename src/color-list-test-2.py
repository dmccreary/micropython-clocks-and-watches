import random
from machine import Pin, SPI
from time import sleep
import gc9a01 as gc9a01
from gc9a01 import color565

SCL = 2
SDA = 3
DC = 4
CS = 5
RST = 6

spi = SPI(0, baudrate=60000000, sck=Pin(SCL), mosi=Pin(SDA))
tft = gc9a01.GC9A01(spi,dc=Pin(DC,Pin.OUT),cs=Pin(CS,Pin.OUT),reset=Pin(RST,Pin.OUT),rotation=0)

tft.fill(gc9a01.BLACK)
tft.line(20,20, 200,200, 0xFFFF)

# draw readability
ON = 1
OFF = 0
NO_FILL = 0
FILL = 1
# bit order is blue, red, green
black = 0x0000
green   = color565(0, 255, 0)
blue = color565(0, 0, 255)
red  = color565(255, 0, 0)
white = 0xffff
#
cyan = color565(0, 255, 255)

purple = color565(255, 0, 255)

gold = color565(200, 200, 0)
yellow = color565(255, 255, 0)
orange  = color565(255, 70, 0)
brown = color565(100, 50, 50)
magenta = color565(50, 0, 50)
pink = color565(255, 150, 150)
olive = color565(25, 100, 25)
gray = color565(50, 50, 50)
lightGreen = color565(25, 255, 25)
darkGreen = color565(25, 50, 25)


ColorList = (red, green, blue, white, yellow, orange, cyan, brown, gold, purple, magenta, pink, olive, gray, lightGreen, darkGreen)
ColorNames = ('red', 'green', 'blue', 'white', 'yellow', 'orange', 'cyan', 'brown', 'gold', 'purple', 'magenta', 'pink', 'olive', 'gray', 'lightGreen', 'darkGreen')

width = 220
tft.fill(gc9a01.BLACK)

for i in range(0, len(ColorList)):
    print(ColorNames[i])
    tft.fill_rect(0, i*15, width, 15, ColorList[i])
    sleep(2)
