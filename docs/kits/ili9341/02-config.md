# Creating a Hardware Configuration File
 
Rather than hard coding the pin numbers in every example, lets put all
our hardware configuration data in a single file.  All the examples
from here on can use that configuration data.

## Hardware Configuration File

```py
# Dan's Robot Labs configuration file for ILI9341 clock project
# The colors on the SPI bus cable are:
# 3.3v power - red
# SCK - orange
# MISO/Data - yellow
# DC - green
# RESET - blue
# GND - black
# CS - purple
SCK_PIN = 2
MISO_PIN = 3 # labeled SDI(MOSI) on the back of the display
DC_PIN = 4
RESET_PIN = 5
CS_PIN = 6
ROTATION = 90

WIDTH=320
HEIGHT=240
```

## Sample Use of Hardwre Configuration File

```py
# print out "Hello World!" using the rotation=3 using 32-bit high font
# the default is white text on a black background
from ili9341 import Display, color565
from machine import Pin, SPI
import config

# Use these PIN definitions.  SCK must be on 2 and data (SDL) on 3
SCK_PIN = config.SCK_PIN
MISO_PIN = config.MISO_PIN # labeled SDI(MOSI) on the back of the display
DC_PIN = config.DC_PIN
RESET_PIN = config.RESET_PIN
CS_PIN = config.CS_PIN

WIDTH=config.WIDTH
HEIGHT=config.HEIGHT
ROTATION=config.ROTATION

# mosi=Pin(23)
# miso=Pin(MISO_PIN)
spi = SPI(0, baudrate=40000000, sck=Pin(SCK_PIN), mosi=Pin(MISO_PIN))
display = Display(spi, dc=Pin(DC_PIN), cs=Pin(CS_PIN), rst=Pin(RESET_PIN), width=WIDTH, height=HEIGHT, rotation=ROTATION)

RED = color565(255,0,0)
ORANGE = color565(255,128,0)
YELLOW = color565(255,255,0)
GREEN = color565(0,255,0)
BLUE = color565(0,0,255)
PURPLE = color565(255,0,255)
WHITE = color565(255,255,255)
BLACK = color565(0,0,0)

display.fill_rectangle(0,0, 50,HEIGHT, RED)
display.fill_rectangle(50,0, 50,HEIGHT, ORANGE)
display.fill_rectangle(100,0, 50,HEIGHT, YELLOW)
display.fill_rectangle(150,0, 50,HEIGHT, GREEN)
display.fill_rectangle(200,0, 50,HEIGHT, BLUE)
display.fill_rectangle(250,0, 50,HEIGHT, PURPLE)
display.fill_rectangle(300,0, 20,HEIGHT, WHITE)

print('Done')
```