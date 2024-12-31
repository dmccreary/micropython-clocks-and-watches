"""
lines.py

    Draws lines and rectangles in random colors at random locations on the
    display.

"""
import random
from machine import Pin, SPI
import gc9a01 as gc9a01

SCL = 2
SDA = 3
DC = 4
CS = 5
RST = 6

def main():
    spi = SPI(0, baudrate=60000000, sck=Pin(SCL), mosi=Pin(SDA))
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(DC, Pin.OUT),
        cs=Pin(CS, Pin.OUT),
        reset=Pin(RST, Pin.OUT),
        rotation=0)

    tft.fill(gc9a01.BLACK)

    while True:
        tft.line(
            random.randint(0, tft.width),
            random.randint(0, tft.height),
            random.randint(0, tft.width),
            random.randint(0, tft.height),
            gc9a01.color565(
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8)
                )
            )

        width = random.randint(0, tft.width // 2)
        height = random.randint(0, tft.height // 2)
        col = random.randint(0, tft.width - width)
        row = random.randint(0, tft.height - height)
        tft.fill_rect(
            col,
            row,
            width,
            height,
            gc9a01.color565(
                random.getrandbits(8),
                random.getrandbits(8),
                random.getrandbits(8)
            )
        )


main()