"""
display-test.py
Fills the screen with red, green and blue
"""

from utime import sleep
import st7789
import tft_config
tft = tft_config.config(1)
tft.init()

while True:
    tft.fill(st7789.RED)
    sleep(1)
    tft.fill(st7789.GREEN)
    sleep(1)
    tft.fill(st7789.BLUE)
    sleep(1)
