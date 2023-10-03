# Test that we have the right version of the MicroPython runtime v1.19.1-854-g35524a6fd on 2023-02-07
from machine import Pin,I2C,SPI,PWM,ADC
from time import sleep
import framebuf
import time
from random import randint
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

radius = 121
# blue, red, green
b = 0b1111100000000000
r = 0b0000011111000000
g = 0b0000000000111111

max = 220
x=CENTER
y=CENTER
dx=1 + randint(0,2)
dy=1 + randint(0,2)
while True:
    LCD.fill(LCD.white)
    LCD.ellipse(x, y, 10, 10, b, FILL)
    LCD.show()
    x = x + dx
    y = y + dy
    if x < 0:
        dx = 1 + randint(0,2)
    if x > max:
        dx = -1
    if y < 0:
        dy = 1 + randint(0,2)
    if y > max:
        dy = -1     

print('done')

