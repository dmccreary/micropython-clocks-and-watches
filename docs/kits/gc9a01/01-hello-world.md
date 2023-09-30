# Hello World Test

We begin by carefully setting up the 7 wires that connect from
the gc9a01 graphics controller to the breadboard that we
have our Raspberry Pi Pico W connected.

```py
# 01-hello-world-firmware.py
# 
from machine import Pin, SPI
import gc9a01
import vga1_bold_16x32 as font

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
tft.fill(0) # fill the screen with black
tft.text(font, "Hello world!", 20, 100, gc9a01.color565(255,0,0), gc9a01.color565(0,0,255))
```