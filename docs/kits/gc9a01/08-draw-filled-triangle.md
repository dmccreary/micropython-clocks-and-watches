# Draw a Filled Triangle

Analog clock hands can be draw with simple lines.  But the display will
be more pleasing if we use clock hands that are made of triangles.

If the framebuf functions were supported in the driver drawing a filled triangle
would be easy.  We would just put the three points in an array and call
the ```poly()``` with a fill option.

However, the current driver does not support the framebuf functions.  To
overcome this limiation we will need to write our own function that
will fill all the points in a triangle.

Our founction must take in the three points and a color and
draw the traingle.

## Draw Filled Triangle

Without going into too much detail, here is
the algorithm we will use dto draw a filled triangle.
Note that only the last line does drawing using the ```line()``` function.
You will note that it must get the points in order
before the main loops run.
This version also checks for divide by zero errors.

```py
def drawFilledTriangle(x1, y1, x2, y2, x3, y3, color=WHITE):
    def swap(x, y):
        return y, x

    # get our points in order
    if y1 > y2:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
    if y1 > y3:
        x1, x3 = swap(x1, x3)
        y1, y3 = swap(y1, y3)
    if y2 > y3:
        x2, x3 = swap(x2, x3)
        y2, y3 = swap(y2, y3)

    for y in range(y1, y3+1):
        if y2 - y1 != 0 and y < y2:
            xa = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
        elif y3 - y1 != 0:
            xa = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if y3 - y2 != 0 and y >= y2:
            xb = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
        elif y3 - y1 != 0:
            xb = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if xa > xb:
            xa, xb = swap(xa, xb)

        for x in range(xa, xb+1):
            # sleep(.1)
            tft.line(x, y, x, y, color)
```

## Full Test Program

To test our alforithm we can genrate three random points near the center of the display
and then call the traingle fill on these points.  If you would like to see
how the algorithm does the drawing, you can uncomment the sleep function just
before the ```tft.line()``` above.

```py
# 01-display-test.py
# 
from machine import Pin, SPI
import random
import gc9a01
import vga1_16x16 as font
from utime import sleep

# this uses the standard Dupont ribbon cable spanning rows 4-9 on our breadboard
SCK_PIN = 2 # row 4
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
# GND is row 8
RST_PIN = 6

# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0
)

WHITE = gc9a01.color565(255,255,255)
BLUE = gc9a01.color565(0,0,255)
BLACK = gc9a01.color565(0,0,0)

tft.init()
tft.fill(0) # fill the screen with black
tft.text(font, "Draw Filled Triangle Test", 20, 10, BLUE, BLACK)



def drawFilledTriangle(x1, y1, x2, y2, x3, y3, color=WHITE):
    def swap(x, y):
        return y, x

    if y1 > y2:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
    if y1 > y3:
        x1, x3 = swap(x1, x3)
        y1, y3 = swap(y1, y3)
    if y2 > y3:
        x2, x3 = swap(x2, x3)
        y2, y3 = swap(y2, y3)

    for y in range(y1, y3+1):
        if y2 - y1 != 0 and y < y2:
            xa = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
        elif y3 - y1 != 0:
            xa = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if y3 - y2 != 0 and y >= y2:
            xb = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
        elif y3 - y1 != 0:
            xb = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if xa > xb:
            xa, xb = swap(xa, xb)

        for x in range(xa, xb+1):
            tft.line(x, y, x, y, color)


min = 50
max = 150
while True:
    tft.fill(BLACK)
    x1 = random.randint(min, max)
    y1 = random.randint(min, max)
    x2 = random.randint(min, max)
    y2 = random.randint(min, max)
    x3 = random.randint(min, max)
    y3 = random.randint(min, max)
    drawFilledTriangle(x1, y1, x2, y2, x3, y3, WHITE)
    sleep(.1)
```

## Crazy Triangles

```py
# lab 15: Filled Triangles
# 
from machine import Pin, SPI
import random
import gc9a01
import vga1_16x16 as font
from utime import sleep

# this uses the standard Dupont ribbon cable spanning rows 4-9 on our breadboard
SCK_PIN = 2 # row 4
SDA_PIN = 3
DC_PIN = 4
CS_PIN = 5
# GND is row 8
RST_PIN = 6

# define the SPI intrface
spi = SPI(0, baudrate=60000000, sck=Pin(SCK_PIN), mosi=Pin(SDA_PIN))
tft = gc9a01.GC9A01(spi, 240, 240, reset=Pin(RST_PIN, Pin.OUT),
    cs=Pin(CS_PIN, Pin.OUT), dc=Pin(DC_PIN, Pin.OUT), rotation=0
)

WHITE = gc9a01.color565(255,255,255)
BLUE = gc9a01.color565(0,0,255)
BLACK = gc9a01.color565(0,0,0)

tft.init()
tft.fill(0) # fill the screen with black
tft.text(font, "Triangles", 57, 22, BLUE, BLACK)

def drawFilledTriangle(x1, y1, x2, y2, x3, y3, color=WHITE):
    def swap(x, y):
        return y, x

    if y1 > y2:
        x1, x2 = swap(x1, x2)
        y1, y2 = swap(y1, y2)
    if y1 > y3:
        x1, x3 = swap(x1, x3)
        y1, y3 = swap(y1, y3)
    if y2 > y3:
        x2, x3 = swap(x2, x3)
        y2, y3 = swap(y2, y3)

    for y in range(y1, y3+1):
        if y2 - y1 != 0 and y < y2:
            xa = x1 + (x2 - x1) * (y - y1) // (y2 - y1)
        elif y3 - y1 != 0:
            xa = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if y3 - y2 != 0 and y >= y2:
            xb = x2 + (x3 - x2) * (y - y2) // (y3 - y2)
        elif y3 - y1 != 0:
            xb = x1 + (x3 - x1) * (y - y1) // (y3 - y1)
        else:
            continue

        if xa > xb:
            xa, xb = swap(xa, xb)

        for x in range(xa, xb+1):
            # for wathing the drawing
            # sleep(.001)
            tft.line(x, y, x, y, color)

min = 40
max = 220
while True:
    # tft.fill(BLACK)
    x1 = random.randint(min, max)
    y1 = random.randint(min, max)
    x2 = random.randint(min, max)
    y2 = random.randint(min, max)
    x3 = random.randint(min, max)
    y3 = random.randint(min, max)
    red = random.randint(0, 255)
    green = random.randint(0, 255)
    blue = random.randint(0, 255)
    color = gc9a01.color565(red,green,blue)
    drawFilledTriangle(x1, y1, x2, y2, x3, y3, color)
    # slow down the drawing here
    sleep(.1)
```