# 01-hello-world.py on the gc9a01 240x240 SPI watch face display

from machine import Pin, SPI
import gc9a01 as gc9a01
from fonts import vga2_bold_16x32 as font

# hardware config
SCK_PIN = 2
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
RST_PIN = 6

# create the SPI on 2
spi = SPI(2, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))

# initialize the driver
tft = gc9a01.GC9A01(spi,
    dc=Pin(DC_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    reset=Pin(RST_PIN, Pin.OUT),
    rotation=0)


tft.text(font, "Hello world!", 10, 100, 1, 0)


