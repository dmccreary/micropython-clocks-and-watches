"""ILI9341 demo (bouncing boxes)."""
from ili9341 import Display, color565
from machine import Pin, SPI
from random import random, seed
from utime import sleep, sleep_ms, sleep_us, ticks_cpu, ticks_us, ticks_diff

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

x=100
y=100
# box size
s=20
vx = 2
vy = 2.5

while True:
    # draw the rect
    display.fill_hrect(x, y , s, s, colors.BLUE)
    sleep_ms(10)
    # erase the entire rect
    display.fill_hrect(x, y, s, s, 0)

    # reverse direction if at the edge
    if x < 2 or x+s > WIDTH-2:
        vx *= -1
    if y < 2 or y+s > HEIGHT-2:
        vy *= -1
    
    # update position
    x += int(vx)
    y += int(vy)