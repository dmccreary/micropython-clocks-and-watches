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

LCD.fill(LCD.white)

# left eye
LCD.ellipse(60, 90, 50, 30, ON, FILL)

# right eye
LCD.ellipse(175, 90, 50, 30, ON, FILL)

# mouth
LCD.ellipse(CENTER, 150, 70, 30, ON, NO_FILL, 12)

LCD.show()
