"""
lines.py

    Draws lines and rectangles in random colors at random locations on the
    display.

"""
import random
from machine import Pin, SPI
import gc9a01 as gc9a01


def main():
    SCL_PIN = 2
    SDA_PIN = 3
    DC_PIN = 4
    CS_PIN = 5
    RST_PIN = 6
    spi = SPI(0, baudrate=60000000, sck=Pin(SCL_PIN), mosi=Pin(SDA_PIN))
    tft = gc9a01.GC9A01(
        spi,
        dc=Pin(DC_PIN, Pin.OUT),
        cs=Pin(CS_PIN, Pin.OUT),
        reset=Pin(RST_PIN, Pin.OUT),
        # backlight=Pin(14, Pin.OUT),
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