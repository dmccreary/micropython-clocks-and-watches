# Lab #3: Color List Test
from machine import Pin,I2C,SPI,PWM,ADC
from time import sleep
from LCD_1inch28 import LCD_1inch28, QMI8658

CENTER = 120
LCD = LCD_1inch28()
LCD.set_bl_pwm(65535)

# draw readability
ON = 1
OFF = 0
NO_FILL = 0
FILL = 1
# hex representation of colors
# note that the bit order is blue, red, green
black = 0x0000
red   = 0x07E0
green = 0x001f
blue  = 0xf800
white = 0xffff

# binary representations of colors
yellow = 0b0000011111111111
orange = 0b0000001111000010
cyan = 0b1111100000111111
brown = 0b0000000001000001
gold = 0b0000001110011110
purple = 0b1111111111000000
magenta = 0b0000001100011000
pink = 0b0000111111000010
olive = 0b0000000001000010
gray = 0b00001000010000100
lightGreen = 0b0000100001111111
darkGreen  = 0b0000000000000001

ColorList =  (red,    green,   blue,   white,   yellow,  orange,
              cyan, brown, gold, purple, magenta, pink, olive, gray, lightGreen, darkGreen)
ColorNames = ('red', 'green', 'blue', 'white', 'yellow', 'orange',
              'cyan', 'brown', 'gold', 'purple', 'magenta', 'pink', 'olive', 'gray', 'lightGreen', 'darkGreen')

radius = 120
LCD.fill(LCD.black)

for i in range(0, len(ColorList)):
    print(ColorNames[i])
    # LCD.ellipse(CENTER, CENTER, radius, radius, ColorList[i], FILL)
    LCD.fill(ColorList[i])
    # draw the text in both black and white
    LCD.text(ColorNames[i], 100, 100, black)
    LCD.text(ColorNames[i], 100, 120, white)
    LCD.show()
    sleep(1)
