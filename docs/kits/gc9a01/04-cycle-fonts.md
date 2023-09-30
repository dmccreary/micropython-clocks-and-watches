# Cycle Through the Builtin Fonts

This program will cycle through the built-in fonts showing
greetings in different fonts, langauges and colors.

```py
# Adapted from the hersey.py program
from machine import Pin, SPI
from utime import sleep, localtime
import random
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
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0)

# Load several frozen fonts from flash

import greeks
import italicc
import italiccs
import meteo
import romanc
import romancs
import romand
import romanp
import romans
import scriptc
import scripts


def cycle(p):
    '''
    return the next item in a list
    '''
    try:
        len(p)
    except TypeError:
        cache = []
        for i in p:
            yield i
            cache.append(i)
        p = cache
    while p:
        yield from p


COLORS = cycle([0xe000, 0xece0, 0xe7e0, 0x5e0, 0x00d3, 0x7030])

FONTS = cycle([
    greeks, italicc, italiccs, meteo, romanc, romancs,
    romand, romanp, romans, scriptc, scripts])

GREETINGS = cycle([
    "bonjour", "buenas noches", "buenos dias",
    "good day", "good morning", "hey",
    "hi-ya", "hi", "how are you", "how goes it",
    "howdy-do", "howdy", "shalom", "welcome",
    "what's happening", "what's up"])

tft.init()
row = 120

while True:
    color = next(COLORS)
    tft.fill(gc9a01.BLACK)
    tft.draw(next(FONTS), next(GREETINGS), 0, row, color)
    sleep(0.5)
```

## References

1. [Russ Hughes Example](https://github.com/russhughes/gc9a01_mpy/blob/main/examples/RP2/hershey.py)