# Test that we have the right version of the MicroPython runtime v1.19.1-854-g35524a6fd on 2023-02-07
from machine import Pin,I2C,SPI,PWM,ADC
from time import sleep
import framebuf
import time
from LCD_1inch28 import LCD_1inch28, QMI8658

CENTER = 120
LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

# draw readability
ON = 1
OFF = 0
NO_FILL = 0
FILL = 1
black = 0x0000
red   = 0x07E0
green = 0x001f
blue  = 0xf800
white = 0xffff
yellow = 0xEFE4
orange = 0xFFA500
cyan = 0x00FFFF
brown = 0xA52A2A
gold = 0xFFD700
purple = 0x800080
pink = 0x07E0
gray = 0x808080
lightGreen = 0x90EE90

ColorList = (red, green, blue, white, yellow, orange, cyan, brown, gold, purple, pink, gray, lightGreen)
ColorNames = ('red', 'green', 'blue', 'white', 'yellow', 'orange', 'cyan', 'brown', 'gold', 'purple', 'pink', 'gray', 'lightGreen')

radius = 120
LCD.fill(LCD.black)

for i in range(0, len(ColorList)):
    print(ColorNames[i])
    LCD.ellipse(CENTER, CENTER, radius, radius, ColorList[i], FILL)
    LCD.text(ColorNames[i],100,100,1)
    LCD.show()
    sleep(3)
