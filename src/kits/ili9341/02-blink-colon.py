# print out "Hello World!" using the rotation=3 using 32-bit high font
# the default is white text on a black background
from ili9341 import Display, color565
from machine import Pin, SPI
from utime import sleep

# Use these PIN definitions.  SCK must be on 2 and data (SDL) on 3
SCK_PIN = 2
MISO_PIN = 3 # labeled SDI(MOSI) on the back of the display
DC_PIN = 4
RESET_PIN = 5
CS_PIN = 6

WIDTH=320
HEIGHT=240

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=90)

RED = color565(255,0,0)
ORANGE = color565(255,128,0)
YELLOW = color565(255,255,0)
GREEN = color565(0,255,0)
BLUE = color565(0,0,255)
PURPLE = color565(255,0,255)
WHITE = color565(255,255,255)
BLACK = color565(0,0,0)

display.clear()

display.fill_rectangle(0,0, 50,WIDTH, BLACK)

colon_xoffset = WIDTH//2
colon_yoffset = HEIGHT//3
colon_sep = 40
colon_size = 15

while True:
    display.fill_rectangle(colon_xoffset, colon_yoffset, colon_size,colon_size, WHITE)
    display.fill_rectangle(colon_xoffset, colon_yoffset+colon_sep, colon_size,colon_size, WHITE)
    sleep(1)
    display.fill_rectangle(colon_xoffset, colon_yoffset, colon_size,colon_size, BLACK)
    display.fill_rectangle(colon_xoffset, colon_yoffset+colon_sep, colon_size,colon_size, BLACK)
    sleep(1)

