# print out "Hello World!" using the rotation=3 using 32-bit high font
# the default is white text on a black background
from ili9341 import Display, color565
from machine import Pin, SPI

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

display.fill_rectangle(0,0, 50,HEIGHT, RED)
display.fill_rectangle(50,0, 50,HEIGHT, ORANGE)
display.fill_rectangle(100,0, 50,HEIGHT, YELLOW)
display.fill_rectangle(150,0, 50,HEIGHT, GREEN)
display.fill_rectangle(200,0, 50,HEIGHT, BLUE)
display.fill_rectangle(250,0, 50,HEIGHT, PURPLE)
display.fill_rectangle(300,0, 20,HEIGHT, WHITE)

print('Done')


