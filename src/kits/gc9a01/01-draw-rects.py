# 01-draw-rect.py on the gc9a01 display
import random
from machine import Pin, SPI
import gc9a01 as gc9a01

# hardware config
SCL_PIN = 2
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
RST_PIN = 6
spi = SPI(0, baudrate=60000000, sck=Pin(SCL_PIN), mosi=Pin(SDA_PIN))

# initialize the display
tft = gc9a01.GC9A01(
    spi,
    dc=Pin(DC_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    reset=Pin(RST_PIN, Pin.OUT),
    rotation=0)

tft.fill(gc9a01.BLACK)

# x, y, width, height
# red
tft.fill_rect(50,  75, 50, 60, gc9a01.color565(255,0,0))
# green
tft.fill_rect(100, 75, 50, 60, gc9a01.color565(0,255,0))
# blue
tft.fill_rect(150, 75, 50, 60, gc9a01.color565(0,0,255))


