"""
hello.py

    Writes "Hello!" in random colors at random locations on the display.
"""

import random
import utime
import st7789
import tft_config
import vga2_bold_16x32 as font

tft = tft_config.config(1)
tft.init()

# draw text using a 16X32 font using blue text on a white background
tft.text(
        font,
        'Hello World!',
        tft.width()//2-100, # 2 - length // 2 * font.WIDTH,
        tft.height()//2-50, # 2 - font.HEIGHT //2,
        st7789.BLUE,
        st7789.WHITE
)
