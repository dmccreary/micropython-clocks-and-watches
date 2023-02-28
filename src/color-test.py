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

radius = 120
LCD.fill(LCD.black)

print('red')
LCD.ellipse(CENTER, CENTER, radius, radius, red, FILL)
LCD.show()
sleep(1)

print('green')
LCD.ellipse(CENTER, CENTER, radius, radius, green, FILL)
LCD.show()
sleep(1)

print('blue')
LCD.ellipse(CENTER, CENTER, radius, radius, blue, FILL)
LCD.show()
sleep(1)

print('white')
LCD.ellipse(CENTER, CENTER, radius, radius, white, FILL)
LCD.show()
sleep(1)

LCD.ellipse(CENTER, CENTER, radius, radius, black, FILL)
LCD.show()
print('done')

LCD.show()
