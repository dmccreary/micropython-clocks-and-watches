# 01-draw-circle.py

# print out "Hello World!" using the rotation=3 using 32-bit high font
# the default is white text on a black background
from ili9341 import Display, color565
from machine import Pin, SPI
import config
import colors

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

# get the blue value
blue = colors.BLUE
black = colors.BLACK

# draw a black rectangle that fills the screen
display.fill_hrect(0,0, WIDTH, HEIGHT, black)
# draw a blue circle in the center of the display
display.fill_circle(WIDTH//2, HEIGHT//2, 100, blue)