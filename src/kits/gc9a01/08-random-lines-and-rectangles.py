from machine import Pin, SPI
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

WIDTH = 240
HEIGHT = 240
# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, WIDTH, HEIGHT, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0)

tft.init()

tft.fill(gc9a01.BLACK)

while True:
    tft.line(
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT),
        gc9a01.color565(
            random.getrandbits(8),
            random.getrandbits(8),
            random.getrandbits(8)
            )
        )

    width = random.randint(0, WIDTH // 2)
    height = random.randint(0, HEIGHT // 2)
    col = random.randint(0, WIDTH - width)
    row = random.randint(0, HEIGHT - height)
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
