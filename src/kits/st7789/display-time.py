from machine import Pin, SPI
from utime import sleep, localtime
import st7789

BACKLIGHT_PIN = 10
RESET_PIN = 11
DC_PIN = 12
CS_PIN = 13
CLK_PIN = 14
DIN_PIN = 15 # lower left corner

import vga1_bold_16x32 as font

spi = SPI(1, baudrate=31250000, sck=Pin(CLK_PIN), mosi=Pin(DIN_PIN))
tft = st7789.ST7789(spi, 240, 320,
    reset=Pin(RESET_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT),
    dc=Pin(DC_PIN, Pin.OUT),
    backlight=Pin(BACKLIGHT_PIN, Pin.OUT),
    rotation=3)
tft.init()

counter = 0
while True:
    now=localtime()
    year = now[0]
    month = now[1]
    day = now[2]
    hour = now[3]
    minutes = now[4]
    second = now[5]
    if hour > 12:
        display_hour = hour-12
        am_pm = "PM"
    else:
        am_pm = "AM"
    

    tft.text(font, f'{day}/{month}/{year}',10, 0, st7789.color565(255,255,255), st7789.color565(0,0,0))
    tft.text(font, f'{display_hour}:{minutes:02d}:{second:02d} {am_pm}',10, 50, st7789.color565(255,0,0), st7789.color565(0,0,0))
    tft.text(font, f'{display_hour}:{minutes:02d}:{second:02d} {am_pm}',10, 100, st7789.color565(0,255,0), st7789.color565(0,0,0))
    tft.text(font, f'{display_hour}:{minutes:02d}:{second:02d} {am_pm}',10, 150, st7789.color565(0,0,255), st7789.color565(0,0,0))
    tft.text(font, str(counter), 10, 200, st7789.color565(255,255,255), st7789.color565(0,0,0))
    counter += 1
    sleep(.5)
