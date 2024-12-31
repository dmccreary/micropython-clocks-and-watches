# Test that we have the right version of the MicroPython runtime v1.19.1-854-g35524a6fd on 2023-02-07
from machine import Pin,I2C,SPI,PWM,ADC
import framebuf
import time
from LCD_1inch28 import LCD_1inch28, QMI8658

CENTER = 125
LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

# draw readability
ON = 1
OFF = 0
NO_FILL = 0
FILL = 1
black = 0x0000
red   =   0x07E0
green =   0x001f
blue  =   0xf800
white = 0xffff

eye_height = 20
LCD.fill(LCD.black)

# left eye
LCD.ellipse(60, 90, 50, eye_height, white, FILL)
LCD.ellipse(60, 90, 10, 10, black, FILL)

# right eye
LCD.ellipse(180, 90, 50, eye_height, white, FILL)
LCD.ellipse(180, 90, 10, 10, black, FILL)

# nose
LCD.ellipse(CENTER, 140, 15, 10, white, NO_FILL, 12)

# mouth
LCD.ellipse(CENTER, 150, 70, 30, white, NO_FILL, 12)
LCD.ellipse(CENTER, 151, 70, 30, white, NO_FILL, 12)
LCD.ellipse(CENTER, 152, 70, 30, white, NO_FILL, 12)

LCD.show()
