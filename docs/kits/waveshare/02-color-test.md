# Color Tests

Now let's try to make the background screen change colors:

```py
from LCD_1inch28 import LCD_1inch28
from utime import sleep

LCD = LCD_1inch28()  
LCD.set_bl_pwm(65535)

LCD.fill(LCD.black)
LCD.show()
sleep(1)
LCD.fill(LCD.white)
sleep(1)
LCD.show()
LCD.fill(LCD.red)
LCD.show()
sleep(1)
LCD.fill(LCD.green)
LCD.show()
sleep(1)
LCD.fill(LCD.blue)
LCD.show()
print('done')
```

What happens when you change the color "red" to be "orange"?  You shouild see:

```linenums="0"
Traceback (most recent call last):
  File "<stdin>", line 10, in <module>
AttributeError: 'LCD_1inch28' object has no attribute 'orange'
```

This shows you that although the driver knows about some basic colors, (black, white, red, green and blue), it has
no understanding of other colors.

To draw these colors we need to add our own color lists.

## Custom Color Lists

In order to get more nuanced colors, we need to define them using the binary of their red, green and blue values.  With
this display, we order the bits, blue, red and green.

We can use the following binary notation to represent the colors:

```py
# binary representations of colors B=Blue bits, R=Red bits, G=Green bits
# color = 0bBBBBBRRRRRGGGGGG
# Cyan has all the blue and green bits on and the red bits off
cyan = cyan = 0b1111100000111111
```

```py
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
# binary representations of colors B=5 Blue bits, R=5 Red bits, G=6 green bits
# color = 0bBBBBBRRRRRGGGGGG
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
    LCD.text(ColorNames[i], 100, 100, 1)
    LCD.text(ColorNames[i], 100, 120, white)
    LCD.show()
    sleep(1)
```

Note that we are using the fill function to draw on all the pixels on the screen.
We could have used the ellipse funtion to draw into the frame buffer, but the fill function is a bit easier.

## Converting RGB888 to BRG556

```py
def convert_color_RGB888_RGB565(R,G,B): # Convert RGB888 to RGB565
    return (((G&0b00011100)<<3) +((B&0b11111000)>>3)<<8) + (R&0b11111000)+((G&0b11100000)>>5)

```