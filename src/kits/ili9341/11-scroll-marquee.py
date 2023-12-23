"""ILI9341 demo (Scrolling Marquee)."""
from ili9341 import Display, color565
from machine import Pin, SPI
from random import random, seed
from utime import sleep, sleep_ms
from sys import implementation

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
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

blue = colors.BLUE
green = colors.GREEN
# Draw non-moving rectangles
display.fill_rectangle(0, 0, 100, 50, blue)
display.fill_rectangle(0, 150, 100, 50, green)

# Load Marquee image
display.draw_image('images/Rototron128x26.raw', 0, 75, 128, 26)

# Set up scrolling - this is not working
"""Set the height of the top and bottom scroll margins.

        Args:
            top (int): Height of top scroll margin
            bottom (int): Height of bottom scroll margin
"""
display.set_scroll(top=150, bottom=100)

spectrum = list(range(0, 200)) + list(reversed(range(0, 200)))
while True:
    for y in spectrum:
        display.scroll(y)
        sleep(.01)