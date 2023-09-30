"""
01-hello_firmware.py

    Writes "Hello World" in random colors at random locations split
    across a pair of GC9A01 displays connected to a Raspberry Pi Pico W.

    BBRow Pin   tft0
    =========  =======
    4   GP2  CLK
    5   GP3  DIN
    6   GP4  DC
    7   GP5  CS
    8   GND  GND
    9   GP6  RST

"""
from machine import Pin, SPI
import random
import gc9a01
import vga1_bold_16x32 as font

SCK_PIN = 2
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
RST_PIN = 6

spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0
)

tft.init()

while True:
    for rotation in range(4):
        tft.rotation(rotation)
        tft.fill(0)

        tft.rotation(rotation)
        tft.fill(0)

        col_max = tft.width() - font.WIDTH*5
        row_max = tft.height() - font.HEIGHT

        for _ in range(128):
            col = random.randint(0, col_max)
            row = random.randint(0, row_max)

            fg = gc9a01.color565(
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8)
            )

            bg = gc9a01.color565(
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8)
            )

            tft.text(font, "Hello", col, row, fg, bg)
            tft.text(font, "World", col, row, fg, bg)