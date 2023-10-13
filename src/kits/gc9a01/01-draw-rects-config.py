# 01-draw-rect.py on the gc9a01 display
from machine import Pin, SPI
import gc9a01 as gc9a01
import config

# hardware config
spi = SPI(0, baudrate=60000000, sck=Pin(config.SCL_PIN), mosi=Pin(config.SDA_PIN))

# initialize the display default rotation=0
tft = gc9a01.GC9A01(spi,
        dc   =Pin(config.DC_PIN,    Pin.OUT),
        cs   =Pin(config.CS_PIN,    Pin.OUT),
        reset=Pin(config.RESET_PIN, Pin.OUT))

tft.fill(gc9a01.BLACK)

# x, y, width, height
# red
tft.fill_rect(50,  75, 50, 60, gc9a01.color565(255,0,0))
# green
tft.fill_rect(100, 75, 50, 60, gc9a01.color565(0,255,0))
# blue
tft.fill_rect(150, 75, 50, 60, gc9a01.color565(0,0,255))


