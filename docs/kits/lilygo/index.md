# LILYGO T-Display RP2040 

[LILYGO](https://www.lilygo.cc/) makes low-cost and high-quality microcontroller development boards that include small displays.  Although
most of their boards run on C programs on ESP-32 processors, they
do have one that runs MicroPython on an RP2040.  This "kit" is
really just that development board placed on a breadboard.  The device
has two buttons on it which can be used to adjust the time.

This is a color 1.14 inch LCD display PS with 240*135 resolution.
It uses the ST7789V chip that has an extreamly high quality
driver created by Russ Hughes that allows for flicker-free
drawing.

I purchased mine on [Ebay](https://www.ebay.com/itm/255602844724) for $10.66 and three dollars for shipping.

Although the display is too small for most robotic applications where the
robot is on the floor and we are standing, it is a good example of how
we can get both clocks and watches to look great.  My hope is that LILYGO
comes out with a larger display in the future.

Lilygo also sells their own ["wearable" watch kits](https://www.lilygo.cc/collections/wearable-kit)] for $35 to $45.  However, I have not purchased any of these that can be programmed with an RP2040 and MicroPython yet.  Here is a [GitHub Page for the T-Watch](https://github.com/Xinyuan-LilyGO/MicroPython_ESP32_psRAM_LoBo#micropython-for-ttgo-t-watch) that implies it might be on the way.  Note that using this requires extensive knowledge of the ESP32 development system.

## Getting Started

To use the ST7789V driver we MUST use a custom image provide by Rull Hughes.  This is because the driver is written in low-level C code
and the python driver requires it to be combiled into the firmware image.

I downloaded the custom image here:

[T-DISPLAY RP2040 Firmware](https://github.com/russhughes/st7789_mpy/tree/master/firmware/T-DISPLAY-RP2040)

I then held the Boot button down while I powered up the device.

I soldered my own header pins on the LILYGO and placed it on a breadboard.  Unfortunatly this makes it impossible to hold down the
boot button with the device on the breadboard.

## Pinouts

The pinouts are very different from the Raspberry Pi Pico.

![Lilygo T-Display RP2040 Pinout](./T-display-RP2040.jpg)

## Config File

This implementation puts the driver in a hidden C program, but it
does have a configuration file that we must upload and place in
the /lib directory.

Here is a [Link to the File for the T-Display RP2040](https://github.com/russhughes/st7789_mpy/blob/b4aa060b74e2d2490770fa92310571f7602059f9/examples/configs/tdisplay_rp2040/tft_config.py)


```py
"""TTGO T-Display RP2040 display"""

from machine import Pin, SPI
from time import sleep
import st7789

TFA = 40	# top free area when scrolling
BFA = 40	# bottom free area when scrolling

def config(rotation=0, buffer_size=0, options=0):

    Pin(22, Pin.OUT, value=1)

    spi = SPI(0,
        baudrate=62500000,
        polarity=1,
        phase=0,
        sck=Pin(2, Pin.OUT),
        mosi=Pin(3, Pin.OUT),
        miso=None)

    return st7789.ST7789(
        spi,
        135,
        240,
        cs=Pin(5, Pin.OUT),
        dc=Pin(1, Pin.OUT),
        backlight=Pin(4, Pin.OUT),
        rotation=rotation,
        options=options,
        buffer_size=buffer_size)
```

## Blink The Onboard LED

This red LED is on the bottom of the board.

Blink Timer example:

```py
from machine import Pin, Timer
led = Pin(25,Pin.OUT)
tim = Timer()
def tick(timer):
    global led
    led.toggle()
tim.init(freq=2.5, mode=Timer.PERIODIC, callback=tick)
```

## Display Example

```py
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

```

## Drawing Text

For this example to work, you will need to load a font library
into the /lib directory.

```py
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
        tft.width()//2-100, # x position to start writing
        tft.height()//2-50, # y position
        st7789.BLUE, # font in blue
        st7789.WHITE # background in white
)
```

## Referneces

[Item on Aliexpress](https://www.aliexpress.us/item/3256803094729227.html?gatewayAdapt=glo2usa4itemAdapt)
Sample GitHub repo: https://github.com/Xinyuan-LilyGO/LILYGO-T-display-RP2040

ST7789V Submodule:
[Russ Hughes GitHub Repo](https://github.com/russhughes/st7789_mpy/tree/b4aa060b74e2d2490770fa92310571f7602059f9)

Config:
[Sample Config File](https://github.com/russhughes/st7789_mpy/blob/b4aa060b74e2d2490770fa92310571f7602059f9/examples/configs/tdisplay_rp2040/tft_config.py)
