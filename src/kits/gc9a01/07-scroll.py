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

def cycle(p):
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

colors = cycle([0xe000, 0xece0, 0xe7e0, 0x5e0, 0x00d3, 0x7030])
foreground = next(colors)
background = gc9a01.BLACK

tft.init()
tft.fill(background)
# sleep(1)

height = tft.height()
width = tft.width()
last_line = height - font.HEIGHT

tfa = 0        # top free area
tfb = 0        # bottom free area
tft.vscrdef(tfa, height, tfb)

scroll = 0
character = font.FIRST

# left margin
lm = 50
while True:
    # clear top line before scrolling off display
    tft.fill_rect(0, scroll, width, 1, background)

    # Write new line when we have scrolled the height of a character
    if scroll % font.HEIGHT == 0:
        line = (scroll + last_line) % height

        # write character hex value as a string
        tft.text(
            font,
            'x{:02x}'.format(character),
            lm,
            line,
            foreground,
            background)

        # write character using a integer (could be > 0x7f)
        tft.text(
            font,
            character,
            lm+80,
            line,
            foreground,
            background)

        # change color for next line
        foreground = next(colors)

        # next character with rollover at 256
        character += 1
        if character > font.LAST:
            character = font.FIRST

    # scroll the screen up 1 row
    tft.vscsad(scroll+tfa)
    scroll += 1
    scroll %= height

    sleep(0.02)
